import cv2
import numpy as np
""" create mask's!  """


""" create mask for fingers_count"""
def for_fingers_count(thresholded, center_x, center_y, radius):

    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
    cv2.circle(circular_roi, (center_x, center_y), radius, 255, 10)
    mask  = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)
    return mask


""" create mask for switch channel"""
def for_switch_channel(frame):
    # black image for mask
    mask = np.zeros(frame.shape, dtype="uint8")

    # draw lines on mask
    line_one_from = (1, 0)
    line_one_to = (1, mask.shape[1])
    line_two_from = (mask.shape[0] - 1, 0)
    line_two_to = (mask.shape[0] - 1, mask.shape[1])
    cv2.line(mask, line_one_from, line_one_to, 255, 4)
    cv2.line(mask, line_two_from, line_two_to, 255, 4)

    # bitwise and
    switch_channel_image = cv2.bitwise_and(frame, mask, mask=mask)

    return switch_channel_image
