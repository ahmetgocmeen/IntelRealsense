import pyrealsense2 as rs
import cv2 as cv
import numpy as np
import pandas as pd
import os

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)


pipeline.start(config)


while True:
    frames = pipeline.wait_for_frames()
    depthFrame = frames.get_depth_frame()
    colorFrame = frames.get_color_frame()

    if not depthFrame or not colorFrame:
        continue
    
    colorImage = np.asanyarray(colorFrame.get_data())
    depthImage = np.asanyarray(depthFrame.get_data())

    cv.namedWindow('RealSense', cv.WINDOW_AUTOSIZE)
    cv.imshow('RealSense', colorImage)

    if cv.waitKey(1) & 0xFF == ord('s'):
        cv.imwrite("Screenshots/SS" + str(len(os.listdir("./ScreenShots")) // 2 + 1) + ".png", colorImage)
        distanceArray = []
        for y in range(480):
            yArray = []
            for x in range(640):
                yArray += [depthImage[y, x]]
            distanceArray += [yArray]
        df = pd.DataFrame(np.array(distanceArray))
        df.to_excel("Screenshots/SS" + str(len(os.listdir("./ScreenShots")) // 2 + 1) + "Distances.xlsx", index=False)
        

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
        
pipeline.stop()