########################################################################
#
# File:   regions.py
# Author: Matt Zucker
# Date:   January 2012 (Updated February 2021)
#
# Written for ENGR 27 - Computer Vision
#
########################################################################
#
# This file shows how to do connected component analysis with OpenCV.

import cv2
import numpy
import sys

# width/color pairs for drawing white over black outlines
DRAW_OUTLINED = [ (3, (0, 0, 0)), (1, (255, 255, 255)) ]

######################################################################
# Our main function

def main():

    # Get an image from the command line and load it.
    if len(sys.argv) < 2:
        print('supply an image filename (e.g. screws_thresholded.png '
              'or ellipses.png)')
        sys.exit(1)

    image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

    # Create an RGB display image which to show the different regions.
    display = numpy.zeros((image.shape[0], image.shape[1], 3),
                          dtype='uint8')

    # Get the list of contours in the image. See OpenCV docs for
    # information about the arguments.
    contours, hierarchy = cv2.findContours(image, cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)

    print('found', len(contours), 'contours')

    # Loop through to draw contours:
    for j in range(len(contours)):

        # Choose a color
        u = float(j) / (len(contours)-1)
        i = int(round(u * (len(CONTOUR_COLORS)-1)))

        # Draw the contour as a colored region on the display image.
        cv2.drawContours( display, contours, j, CONTOUR_COLORS[i], -1 )

        
    # Loop through again to draw labels
    for contour in contours:

        # Compute some statistics about this contour.
        info = get_contour_info(contour)

        # Mean location, area, and basis vectors can be useful.
        area = info['area']
        mu = info['mean']
        b1 = info['b1']
        b2 = info['b2']

        # Annotate the display image with mean and basis vectors.
        for width, color in DRAW_OUTLINED:

            cv2.circle( display, make_point(mu), 3, color,
                        width, cv2.LINE_AA )

            cv2.line( display, make_point(mu), make_point(mu+b1),
                      color, width, cv2.LINE_AA )

            cv2.line( display, make_point(mu), make_point(mu+b2),
                      color, width, cv2.LINE_AA )

        draw_outlined_text(display, 'Area: {:.0f} px'.format(area), mu + (-5 -10))

    draw_outlined_text(image, 'Original', (10, image.shape[0]-10))
    draw_outlined_text(display, 'Connected components', (10, image.shape[0]-10))
        
    cv2.imshow('Regions', image)
    while cv2.waitKey(5) < 0: pass
        
    # Display the output image and wait for a keypress.
    cv2.imshow('Regions', display)
    while cv2.waitKey(5) < 0: pass

######################################################################
# Construct a tuple of ints from a numpy array

def make_point(arr):
    return tuple(numpy.round(arr).astype(int).flatten())

######################################################################
# Draw outlined text

def draw_outlined_text(img, text, location):
    
    for width, color in DRAW_OUTLINED:

        cv2.putText( img, text, make_point(location), 
                     cv2.FONT_HERSHEY_PLAIN,
                     0.8, color, width, cv2.LINE_AA )

######################################################################
#
# Compute moments and derived quantities such as mean, area, and
# basis vectors from a contour as returned by cv2.findContours.
#
# Feel free to use this function with attribution in your project 1
# code.
#
# Returns a dictionary.

def get_contour_info(c):

    # For more info, see
    #  - https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html
    #  - https://en.wikipedia.org/wiki/Image_moment

    m = cv2.moments(c)

    s00 = m['m00']
    s10 = m['m10']
    s01 = m['m01']
    c20 = m['mu20']
    c11 = m['mu11']
    c02 = m['mu02']

    if s00 != 0:

        mx = s10 / s00
        my = s01 / s00

        A = numpy.array( [
                [ c20 / s00 , c11 / s00 ],
                [ c11 / s00 , c02 / s00 ] 
                ] )

        W, U, Vt = cv2.SVDecomp(A)

        ul = 2 * numpy.sqrt(W[0,0])
        vl = 2 * numpy.sqrt(W[1,0])

        ux = ul * U[0, 0]
        uy = ul * U[1, 0]

        vx = vl * U[0, 1]
        vy = vl * U[1, 1]

        mean = numpy.array([mx, my])
        uvec = numpy.array([ux, uy])
        vvec = numpy.array([vx, vy])

    else:
        
        mean = c[0].astype('float')
        uvec = numpy.array([1.0, 0.0])
        vvec = numpy.array([0.0, 1.0])

    return {'moments': m, 
            'area': s00, 
            'mean': mean,
            'b1': uvec,
            'b2': vvec}

######################################################################
# A list of RGB colors useful for drawing segmentations of binary
# images with cv2.drawContours

CONTOUR_COLORS = [
    (255,   0,   0),
    (255,  63,   0),
    (255, 127,   0),
    (255, 191,   0),
    (255, 255,   0),
    (191, 255,   0),
    ( 63, 255,   0),
    (  0, 255,   0),
    (  0, 255,  63),
    (  0, 255, 127),
    (  0, 255, 191),
    (  0, 255, 255),
    (  0, 191, 255),
    (  0, 127, 255),
    (  0,  63, 255),
    (  0,   0, 255),
    ( 63,   0, 255),
    (127,   0, 255),
    (191,   0, 255),
    (255,   0, 255),
    (255,   0, 191),
    (255,   0, 127),
    (255,   0,  63),
]



if __name__ == '__main__':
    main()
