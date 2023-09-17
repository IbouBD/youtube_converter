import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QProgressBar, QFileDialog
from PyQt5 import QtGui
from pathlib import Path
from pytube import YouTube

class YouTubeConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Converter")
        self.setWindowIcon(QtGui.QIcon('icons8-mélanger-48.ico'))
        self.setGeometry(100, 150, 450, 150)
        self.setMaximumSize(450, 180)
        self.setMinimumSize(450, 180)

        self.initUI()

    def initUI(self):
        self.label = QLabel("Enter video URL:", self)
        self.label.move(20, 20)

        self.url_entry = QLineEdit(self)
        self.url_entry.setGeometry(150, 20, 250, 30)

        self.dir_btn = QPushButton('Browse', self)
        self.dir_btn.setGeometry(20, 65, 130, 30)
        self.dir_btn.clicked.connect(self.open_dir_dialog)
        
        self.dir_name_edit = QLineEdit(self)
        self.dir_name_edit.setGeometry(180, 65, 250, 30)
        

        self.mp3_button = QPushButton("Convert to MP3", self)
        self.mp3_button.setGeometry(20, 120, 200, 30)
        self.mp3_button.clicked.connect(self.GetUrl_mp3)

        self.mp4_button = QPushButton("Convert to MP4", self)
        self.mp4_button.setGeometry(230, 120, 200, 30)
        self.mp4_button.clicked.connect(self.GetUrl_mp4)

        self.pbar= QProgressBar(self)
        self.pbar.setGeometry(42, 160, 400, 10)

    def open_dir_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            self.dir_name_edit.setText(str(path))
            global gpath
            gpath = str(path)

    def GetUrl_mp3(self):
        try:
            url = self.url_entry.text()
            yt = YouTube(url)

            video = yt.streams.filter(only_audio=True).first()
            video.download(output_path=gpath)
            # setting for loop to set value of progress bar
            for i in range(101):
  
                # slowing down the loop
                time.sleep(0.06)
    
                # setting value to progress bar
                self.pbar.setValue(i)
            

            message = f"Video downloaded successfully!\nTitle: {yt.title}\nDuration: {yt.length} seconds"
            QMessageBox.information(self, "Success", message)
            self.pbar.setValue(0)
            self.url_entry.clear()
        
        except Exception as e:
            print(f"\nSomething Went Wrong: {str(e)}\n")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.url_entry.clear()
            

    def GetUrl_mp4(self):
        try:
            url = self.url_entry.text()
            yt = YouTube(url)

            print("Video Title:", yt.title)
            print("Video Duration:", yt.length, "seconds")

            video_stream = yt.streams.get_highest_resolution()

            print("Downloading....")
            video_stream.download(output_path=gpath)
            # setting for loop to set value of progress bar
            for i in range(101):
  
                # slowing down the loop
                time.sleep(0.075)
    
                # setting value to progress bar
                self.pbar.setValue(i)
            print("Download completed!")

            message = f"Video downloaded successfully!\nTitle: {yt.title}\nDuration: {yt.length} seconds"
            QMessageBox.information(self, "Success", message)
            self.pbar.setValue(0)
            self.url_entry.clear()

        except Exception as e:
            print(f"\nSomething Went Wrong: {str(e)}\n")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.url_entry.clear()

def main():
    app = QApplication(sys.argv)
    window = YouTubeConverter()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()