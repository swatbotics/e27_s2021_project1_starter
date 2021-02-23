########################################################################
#
# File:   resize_video.py
# Author: Matt Zucker
# Date:   February 2021
#
# Written for ENGR 27 - Computer Vision
#
########################################################################
#
# Useful program for downscaling input videos to 640 pixels wide for
# faster processing and smaller file sizes.

import sys, os
import cv2

def main():

    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print('usage: resize_video.py SOURCE') 
        print('   or: resize_video.py FRAMECOUNT')
        print('   or: resize_video.py STARTFRAME ENDFRAME')
        sys.exit(1)

    ##################################################
    # get video properties
    
    input_filename = sys.argv[1]

    if not os.path.exists(input_filename):
        print('error:', input_filename, 'does not exist')
        sys.exit(1)

    nframes, width, height, fps = get_num_frames(input_filename)

    print(input_filename, 'has', nframes, 
          f'frames of size {width}x{height} at {fps} fps')

    ##################################################
    # compute output size

    frac = 640.0/width

    if frac >= 1.0:
        print('width already <= 640, not resizing!')
        sys.exit(1)

    output_size = (int(round(width*frac)), int(round(height*frac)))

    print('will resize to {}x{}'.format(*output_size))

    ##################################################
    # deal with start/end indices

    if len(sys.argv) == 2:
        start = 0
        end = nframes
    elif len(sys.argv) == 3:
        start = 0
        end = int(sys.argv[2])
    else:
        start = int(sys.argv[2])
        end = int(sys.argv[3])

    if start < 0 or start > nframes or end < 0 or end > nframes or end < start:
        print('invalid frame indices, must have 0 <= STARTFRAME < ENDFRAME <', nframes)
        sys.exit(1)
        
    if start > 0 or end < nframes:
        print(f'will write frames {start}-{end}')
        
    ##################################################
    # create the output video
        
    basename, _ = os.path.splitext(os.path.basename(input_filename))

    fourcc, ext = (cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 'mp4')
    output_filename = basename + '_resized.' + ext

    writer = cv2.VideoWriter(output_filename, fourcc, fps, output_size)
    
    cap = cv2.VideoCapture(input_filename)
    frame_idx = 0

    while True:
        ok, frame = cap.read()
        if not ok or frame is None:
            break
        frame = cv2.resize(frame, output_size, interpolation=cv2.INTER_AREA)
        if frame_idx >= start and frame_idx < end:
            writer.write(frame)
        frame_idx += 1

    print(f'wrote {end-start} frames to {output_filename}')

######################################################################

def get_num_frames(input_filename):

    cap = cv2.VideoCapture(input_filename)

    # try the fast way
    nframes = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    if not fps > 1:
        # fps buggy sometimes
        fps = 30.0 

    if nframes > 1 and width > 1 and height > 1:
        # it worked
        return int(nframes), int(width), int(height), fps

    # the slow way
    cnt = 0
    
    while True:
        ok, frame = cap.read()
        if not ok or frame is None:
            break
        height, width = frame.shape[:2]
        cnt += 1

    return cnt, width, height, fps

######################################################################

if __name__ == '__main__':
    main()
