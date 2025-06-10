import os 
import shutil
import datetime
import time
import schedule 
import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication, QMessageBox,QDesktopWidget,QHBoxLayout,QFormLayout,QLabel,QPushButton,QLineEdit,QVBoxLayout,QWidget, QSizePolicy
from PyQt5.QtCore import Qt
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QPixmap,QPalette,QBrush
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class BackupSignals(QObject):
    message_signal = pyqtSignal(str, str)  # (title, message)

signals = BackupSignals()

def copy_folder_to_directory(source, dest):
    today = datetime.date.today() 
    dest_dir = os.path.join(dest, str(today))
    try:
        shutil.copytree(source, dest_dir)
        signals.message_signal.emit("Backup successful", f"Folder copied to: {dest_dir}")
    except FileExistsError:
        signals.message_signal.emit("Backup failed", f"Folder already exists in: {dest}")
    except Exception as e:
        signals.message_signal.emit("Backup Error", str(e))
    
def launch_backup():
    global source_dir, destination_dir, timeb
    source_dir = source.text()
    destination_dir = destination.text()
    t_string = timeb.text()
    if not source_dir or not destination_dir:
        QMessageBox.warning(window, "Input Error", "Please enter both source and destination paths.", QMessageBox.Ok)
        return

    def schedule_thread():
        schedule.every().day.at(t_string).do(lambda: copy_folder_to_directory(source_dir, destination_dir))
        while True:
            schedule.run_pending()
            time.sleep(60)

    Thread(target=schedule_thread).start()
    QMessageBox.information(window, "Backup Scheduled", f"Backup scheduled daily at {t_string}, please dont close the program!", QMessageBox.Ok)

source_dir = r""
destination_dir = r""
timeb =""
app = QApplication(sys.argv)
window = QWidget()
pixmap = QPixmap("guiwallpaper.jpg")
window.setWindowTitle("Automated-file-backup")
center_point = QDesktopWidget().availableGeometry().center()
n=1
image_size = (736//n,488//n)
window.setGeometry(int(center_point.x()-image_size[0]//2), int(center_point.y()-image_size[1]//2), int(image_size[0]), int(image_size[1]))  # Default size

palette = QPalette()
palette.setBrush(QPalette.Window, QBrush(pixmap))
window.setAutoFillBackground(True)
window.setPalette(palette)

def resize_background(event):
    scaled_pixmap = pixmap.scaled(window.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
    window.setPalette(palette)
window.resizeEvent = resize_background

source = QLineEdit()
source.setPlaceholderText("Enter your source path directory")
source.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
source.setMinimumWidth(200)  # Minimum width instead of fixed

sourcestring = QLabel("Source:")
sourcestring.setStyleSheet("color: white;")
sourcestring.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

launch = QPushButton("Launch Backup")
launch.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
launch.setMinimumWidth(500)  # Minimum width instead of fixed
    

destination = QLineEdit()
destination.setPlaceholderText("Enter your destination path directory")
destination.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
destination.setMinimumWidth(500)  # Minimum width instead of fixed
destinationstring = QLabel("Destination:")
destinationstring.setStyleSheet("color:white;")
destinationstring.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

timeb = QLineEdit()
timeb.setPlaceholderText("Enter the time of backup, eg, 17:06")
timeb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
timeb.setMinimumWidth(500)  # Minimum width instead of fixed
timebstring = QLabel("time:")
timebstring.setStyleSheet("color:white;")
timebstring.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

# Minimum height instead of fixed height
source.setMinimumHeight(40)
sourcestring.setMinimumHeight(40)
destination.setMinimumHeight(40)
destinationstring.setMinimumHeight(40)
timeb.setMinimumHeight(40)
timebstring.setMinimumHeight(40)
launch.setMinimumHeight(40)

style = """
QLineEdit , QComboBox {
    background-color:  rgba(252,249,210,0.6);
    color: color;
    border: 2px solid black;
    border-radius: 10px;
    padding: 10px 15px;
    font-size: 18px;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    selection-background-color: #00c6ff;
}

QLineEdit:focus {
    border: 2px solid black ;
    background-color: rgba(252,249,210,0.6);
}
QLabel{
    background-color: rgba(252,249,210,0.66);  
    color: black;
    border: 2px solid black;
    padding: 8px;
    border-radius: 8px;
    
}
QPushButton {
    background-color: rgba(113,143,151,255);  
    color: black;
    border: 2px solid black;
    padding: 8px;
    border-radius: 8px;
}
QPushButton:hover {
    background-color: rgba(113,143,151,0.7);  
}
"""
for i in [source,sourcestring,destination,timeb,timebstring,destinationstring,launch]:
    i.setStyleSheet(style)

flayout = QFormLayout()
flayout.setSpacing(10)
flayout.addRow(sourcestring, source)
flayout.addRow(destinationstring, destination)
flayout.addRow(timebstring, timeb)
form_container = QWidget()
form_container.setLayout(flayout)
form_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

form_layout = QVBoxLayout()
form_layout.setSpacing(10)
form_layout.addStretch(1)
form_layout.addWidget(form_container)
form_layout.addWidget(launch, alignment=Qt.AlignCenter)
form_layout.addStretch(1)

Final_layout = QHBoxLayout()
Final_layout.addStretch(1)
Final_layout.addLayout(form_layout)
Final_layout.addStretch(1)

window.setLayout(Final_layout)
def show_message(title, message):
    if "success" in title.lower():
        QMessageBox.information(window, title, message, QMessageBox.Ok)
    else:
        QMessageBox.warning(window, title, message, QMessageBox.Ok)

signals.message_signal.connect(show_message)
launch.clicked.connect(launch_backup)
window.show()
sys.exit(app.exec_())
