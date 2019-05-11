
# **Controlling video speed with hand gestures 
Controlling the speed of a video with the number of fingers that are held up.**

1 for backward.

2 fingers for forward.

0 fingers for stop.

4/5 fingers for normal speed.

**hand wave left for previous channel**

**hand wave right for next channel**




# Demo

![ezgif com-video-to-gif 4](https://user-images.githubusercontent.com/40145410/50739674-39baac80-11ec-11e9-9215-46bb1a86fd92.gif)

![channels](https://user-images.githubusercontent.com/40145410/57572426-db643b80-7422-11e9-9d8e-01d6c982efc7.gif)




# The main idea

● Store the video frames

● Iteration over the frames

● Count how many fingers are being held up

# Store the video frames
Take a video as input and break the video into frames and simultaneously store those frames in a list.

# Iteration over the frames
After getting a list of frames we perform iteration over the frames, and control the index of the list with the number of fingers that are being held up.

# Count how many fingers are being held up

![video1545480416](https://user-images.githubusercontent.com/40145410/50406760-26164b80-07d3-11e9-8bee-ccc3980f445a.gif) 


![capture](https://user-images.githubusercontent.com/40145410/50406794-dd12c700-07d3-11e9-86da-fada81684e47.PNG)


# Motion Region of Interest
Background Extraction from a video. Background extraction comes important in object tracking. If you already have an image with constant background, then it is simple. But in the real world, the backround we see is noisy, so one has to estimate the background over time. That is where we use Running Average implemented by ​cv2.accumulateWeighted(). We keep feeding each frame to this function, and the function keeps finding the averages of all frames. 0.02 = α We found that it achieves good results for 60 frames. This results in an estimated background model learnt over time.


# Hand Segmentation
For each frame in time - The estimated background is substracted from the current image. The objects left after subtraction are presumably the foreground objects. We had to blur the frames using ​Gaussian blur ​and morphology operations (​opening​) to ​achieve better results. Finally we can find the external contours from the Hand Segment.

# Count the fingers being held up 
We follow the steps bellow: 


● Find the extrema locations in the hand segment

![1](https://user-images.githubusercontent.com/40145410/50377346-54a1f400-0624-11e9-9669-133a7a101086.PNG)

●  Use the extrema locations to calculate the hand center

![capture](https://user-images.githubusercontent.com/40145410/50377348-7307ef80-0624-11e9-8847-f5b047dfec78.PNG)


● Calculate the distance between the center and the point that is the farthest from the center

![capture](https://user-images.githubusercontent.com/40145410/50377359-93d04500-0624-11e9-9354-8dec40f4dcac.PNG)


● Use that distance to create a circle (any points that are outside of the circle are the extended fingers) 

![capture](https://user-images.githubusercontent.com/40145410/50377366-b06c7d00-0624-11e9-9ae9-a7a359aaffbe.PNG)



● Return the number of the fingers. 

















