import cv2
import numpy as np
import draw
from sklearn.metrics import pairwise
import masks

lower_contours_size = 20
higher_contours_size = 90

"""
Count the fingers being held up.
The idea is this:
1)Find the extrem points in the hand
2)Then use their intersection to estimate the center of the hand.
3)Calculate the distance for the point further away from the center
4)Using that distance to create circle(Any points that are outside of the circle,those should be extended fingers)
Return the number of the fingers and procedures frames.
"""


def count_fingers(frame, thresholded, hand_segment):
    # Find the top, bottom, left , and right in the hand_segment with the extream points
    top = tuple(hand_segment[hand_segment[:, :, 1].argmin()][0])
    bottom = tuple(hand_segment[hand_segment[:, :, 1].argmax()][0])
    left = tuple(hand_segment[hand_segment[:, :, 0].argmin()][0])
    right = tuple(hand_segment[hand_segment[:, :, 0].argmax()][0])

    # Center of the hand is going to be halfway between the top and bottom and halfway between the left and right
    center_x = (left[0] + right[0]) // 2
    center_y = (top[1] + bottom[1]) // 2 + 20

    # Calculate the distance from the center to all the extreme points
    distance = pairwise.euclidean_distances([(center_x, center_y)], Y=[left, right, top, bottom])[0]
    max_distance = distance.max()

    # Create a circle with a 70% percent radius of the max in distance.(i found work wall on my hand)
    radius = int(0.65 * max_distance)

    # create mask
    circular_roi = masks.for_fingers_count(thresholded, center_x, center_y, radius)

    # Grab all the contours in this circular region of interest.
    contours, hierarchy = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    counter = 0

    for cnt in contours:

        # Grab the bounding box of the contour.
        (x, y, w, h) = cv2.boundingRect(cnt)

        limit_points1 = cnt.shape[0] < higher_contours_size
        limit_points2 = cnt.shape[0] > lower_contours_size

        # Check if the contour region is in the right range
        out_of_wrist = (center_y + center_y * 0.20) > y + h

        if out_of_wrist and limit_points1 and limit_points2:
            counter += 1
        if counter > 5:
            counter = 5

    # Visual the data(for debug use)
    visual_threshold = draw.visual_data(thresholded, radius, center_x, center_y)
    frame = cv2.flip(frame, 1)
    visual_color = draw.visual_data(frame, radius, center_x, center_y)
    return (counter, visual_threshold, visual_color)