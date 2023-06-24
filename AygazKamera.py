import cv2 as cv
import os
import sys
import time
import pandas as pd
from IntelRealsense import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aygaz Kamera Kayıt")
        self.setStyleSheet("background : white;")
        self.setGeometry(100,100,1280,720)
        self.save_path = ""
        self.status = QStatusBar()
        self.available_cameras = QCameraInfo.availableCameras()
        self.status.setStyleSheet("background : white;")

        self.setStatusBar(self.status)
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)
        self.select_camera(0)

        toolbar =  QToolBar("Camera Tool Bar")
        self.addToolBar(toolbar)

        click_action = QAction("Click photo", self)
        click_action.setStatusTip("This will capture picture")
        click_action.setToolTip("Capture picture")
        click_action.triggered.connect(self.save_button)
        toolbar.addAction(click_action)

        change_folder_action = QAction("Change save location",self)
        change_folder_action.setStatusTip("Change folder where picture will be saved saved.")
        change_folder_action.setToolTip("Change save location")
        change_folder_action.triggered.connect(self.chane_location)
        toolbar.addAction(change_folder_action)

        self.show()

    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)   
        self.camera.start() 
        self.capture = QCameraImageCapture(self.camera)    
        self.currentCameraName = self.available_cameras[i].description()
        print(self.currentCameraName)
        self.save_seq = 0
                
    def save_button(self):
        
        if not self.save_path == "":

            rc = RealsenseCamera()

            ret, depth_frame, color_frame = rc.GetFrame()

            cv.imwrite(self.save_path + "/SS" + str(len(os.listdir(self.save_path)) // 2 + 1) + ".png", color_frame)
            
            distanceArray = []
            for y in range(480):
                yArray = []
                for x in range(640):
                    yArray += [depth_frame[y, x]]
                distanceArray += [yArray]
            df = pd.DataFrame(np.array(distanceArray))
            df.to_excel( self.save_path + "/SS" + str(len(os.listdir(self.save_path)) // 2 + 1) + "Distances.xlsx", index=False)

            timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
            self.capture.capture(os.path.join(self.save_path,
										"%s-%04d-%s.jpg" % (
			self.currentCameraName,
			self.save_seq,
			timestamp
		    )))
        
            self.save_seq += 1
            
        error = QErrorMessage(self)
        error.setWindowTitle("Hata")
        error.showMessage("Kaydedilecek Konum Seçilmedi!")
        

    def chane_location(self):

        path = QFileDialog.getExistingDirectory(self, "Save Location", "")
        
        if path:
            self.save_path = path
            self.save_seq = 0

    


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())
