import cv2
import numpy as np
import sys
import fire

MIN_RADIUS = 20
MAX_RADIUS = 50
PARAM1 =  154 * 0.4
PARAM2 =  154 * 0.3


def load_image(image):
    """ Load image """
    img = cv2.imread(image)
    return img

def convert2gray(image):
    # Convert to gray-scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def detect_circle(image, gray):
    """ Do circle detection """
    cimg = np.copy(image)
    # Detect circles using HoughCircles transform
    cir_len = 0
    circles = cv2.HoughCircles(gray,
                            cv2.HOUGH_GRADIENT,
                            1,
                            cimg.shape[0]/4096, 
                            param1=PARAM1, 
                            param2=PARAM2, 
                            minRadius=MIN_RADIUS, 
                            maxRadius=MAX_RADIUS
                        )

    # If at least 1 circle is detected
    if circles is not None:
        cir_len = circles.shape[1] # store length of circles found
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    else:
        cir_len = 0 # no circles detected
    
    
    text = f"Number of circle: {cir_len}"
    cv2.putText(cimg, text, (20, 500),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # Display output image
    cv2.imshow('Image', cimg) 

    # save the image
    cv2.imwrite('result.png', cimg)
    
    # Edge image for debugging
    edges = cv2.Canny(gray, PARAM1, PARAM2)
    cv2.imshow('Edges', edges)


def detect_rectangle():
    """ Do rectangle detection """
    pass


def run(image):
    """ Execution """
    img = load_image(image)
    gray = convert2gray(img)
    detect_circle(img, gray)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break

    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    fire.Fire()
    
