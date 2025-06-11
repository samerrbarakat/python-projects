from pytubefix import YouTube
from pytubefix.cli import on_progress
import tkinter as tk 
from tkinter import filedialog

def download_video(url, save_path):
    try: 
        yt = YouTube(url, on_progress_callback=on_progress)
        print("Downloading:", yt.title)
        
        ys = yt.streams.get_highest_resolution()
        ys.download(output_path=save_path)  
        print(f"Video saved to: {save_path}")
    except Exception as e:
        print("Error:", e) 

url = "hhttps://youtu.be/LsyviHWrNB4?si=a7ppckVRARP8--Ch"
save_path = r"Downloads"  
download_video(url, save_path)