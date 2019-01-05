
# Video hand control
Control the speed of a video with the number of fingers that being held up.

# Demo
soon

# The main idea

● Store the video frames

● Iteration over the frames

● Count how many fingers are being held up

# Store the video frames
Take a video as input and breaking the video into frames and simultaneously store that frames in a list.

# Iteration over the frames
After getting list of frames we perform iteration over the frames, and control the index of the list with the 
number of fingers that being held up.

# Finger-counting
Count how many fingers are being held up

![video1545480416](https://user-images.githubusercontent.com/40145410/50406760-26164b80-07d3-11e9-8bee-ccc3980f445a.gif) 


![capture](https://user-images.githubusercontent.com/40145410/50406794-dd12c700-07d3-11e9-86da-fada81684e47.PNG)


# Motion Region of Interest
Background Extraction from a Video Background extraction comes important in object tracking. If you already have an image with constant background, then it is simple. But in the wild, background we be noisy, so one has to estimate the background across time. That is were we use Running Average implemented by ​cv2.accumulateWeighted(). We keep feeding each frame to this function, and the function keep finding the averages of all frames. We found that it achieves good results for 60 frames. 0.02 = α This results in an estimated background model learnt over time.


# Hand Segmentation
For each frame in time - The estimated background is substracted from the current image. The object left after subtraction are presumably the foreground objects. We had to blur the frames using ​Gaussian blur ​and morphology operations (​opening​) to ​achieve better results. Finally we can find the external contours from the Hand Segment.

# Count the fingers being held up 
We follow the steps bellow: 


● Find the extrema Locations in the hand segment

![1](https://user-images.githubusercontent.com/40145410/50377346-54a1f400-0624-11e9-9669-133a7a101086.PNG)

●  Use Extrema to calculate the hand center

![capture](https://user-images.githubusercontent.com/40145410/50377348-7307ef80-0624-11e9-8847-f5b047dfec78.PNG)


● Calculate the distance for the point further away from the center 

![capture](https://user-images.githubusercontent.com/40145410/50377359-93d04500-0624-11e9-9354-8dec40f4dcac.PNG)


● Using that distance to create circle (Any points that are outside of the circle,those should be extended fingers) 

![capture](https://user-images.githubusercontent.com/40145410/50377366-b06c7d00-0624-11e9-9ae9-a7a359aaffbe.PNG)



● Return the number of the fingers and procedures frames. 

















