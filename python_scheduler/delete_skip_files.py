import os
import sys

bhavgeet_path = "/home/pi/vlc_scheduler/audio_content/bhavgeet"

for folder in os.listdir(bhavgeet_path):
    full_folder_path = os.path.join(bhavgeet_path, folder)
    for file in os.listdir(full_folder_path):
        full_bhavgeet_path = os.path.join(full_folder_path, file) 
        if 'skip' in full_bhavgeet_path.lower():
            print("Deleting {} ".format(full_bhavgeet_path))
            os.remove(full_bhavgeet_path)
