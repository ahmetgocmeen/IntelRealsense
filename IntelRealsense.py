import pyrealsense2 as rs
import numpy as np

class RealsenseCamera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        self.pipeline.start(config)
    
    def GetFrame(self):
        frames = self.pipeline.wait_for_frames()
        depthFrame = frames.get_depth_frame()
        colorFrame = frames.get_color_frame()

        if not depthFrame or not colorFrame:
            return False, None, None

        depthImage = np.asanyarray(depthFrame.get_data())
        colorImage = np.asanyarray(colorFrame.get_data())

        return True, depthImage, colorImage

    def Release(self):
        self.pipeline.stop()