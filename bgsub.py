########################################################################
#
# File:   bgsub.py
# Author: Matt Zucker
# Date:   February 2020 (Updated February 2021)
#
# Written for ENGR 27 - Computer Vision
#
########################################################################
#
# This file shows how to do background subtraction given two frames.

import numpy as np
import cv2
import sys

def main():

    # Read in two frames
    bg = cv2.imread('cat_background.png')
    frame = cv2.imread('cat_foreground.png')

    # Take their absolute difference
    diff = cv2.absdiff(bg, frame)

    # Convert to intensity image
    diff_gray = diff.max(axis=2) # per-pixel RGB -> single intensity

    # Threshold!
    _, mask = cv2.threshold(diff_gray, 35, 255, cv2.THRESH_BINARY)

    # Display results
    e27_show_image(bg, 'Background')
    e27_show_image(frame, 'Frame 100')
    e27_show_image(diff, 'cv2.absdiff(bg, frame)')
    e27_show_image(diff_gray, 'max of diff along RGB')
    e27_show_image(mask, 'Thresholded')

######################################################################
# Helper function stolen from tutorial.py code

_win = None

# show an image with a caption
def e27_show_image(img, text):

    display = img.copy()

    h = img.shape[0]

    for txtcolor, txtsize in [(0, 4), (255, 1)]:

        cv2.putText(display, text=text,
                    org=(4, h-8),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(txtcolor, txtcolor, txtcolor),
                    thickness=txtsize,
                    lineType=cv2.LINE_AA)

    global _win

    if _win is None:
        print()
        print('Click in the window and hit any key to continue,')
        print('or hit ESCAPE to quit this program.')
        print()
        _win = 'Display'
        cv2.namedWindow(_win)
    
    cv2.imshow(_win, display)

    while True:
        k = cv2.waitKey(5)
        if k == 27:
            print('ESCAPE hit, quitting!')
            sys.exit(0)
        elif k >= 0:
            break

if __name__ == '__main__':
    main()
