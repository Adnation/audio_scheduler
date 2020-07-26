import os
import vlc
import sys
import time
import random
import logging
import calendar
import simpleaudio as sa
from datetime import date
from logger_utility import log_message


logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__file__)


class AudioScheduler:

    def __init__(self):
        self.folder_path = "/home/pi/vlc_scheduler/audio_content/general"
        self.pooling_duration = 30
        self.max_bhavgeets = 2
        self.max_stotras = 1
        self.debug = True if os.getenv("AUDIO_SCHEDULER_DEBUG") is not None else False

    def retrieve_bhavgeet_paths(self):
        bhavgeet_root_path = "/home/pi/vlc_scheduler/audio_content/bhavgeet"
        all_bhavgeet_folders = os.listdir(bhavgeet_root_path)
        total_bhavgeet_folder = len(all_bhavgeet_folders)
        selected_folders = random.choices(all_bhavgeet_folders, k=self.max_bhavgeets)
        selected_bhavgeets = []
        for folder in selected_folders:
            all_bhavgeets = os.listdir(os.path.join(bhavgeet_root_path, folder))
            total_bhavgeets = len(all_bhavgeets)
            while True:
                random_index = random.randint(0, (total_bhavgeets-1))
                selected_bhavgeet = all_bhavgeets[random_index]
                if '_skip' in selected_bhavgeet.lower():
                    log_message("Skipping {} ".format(selected_bhavgeet), 'debug')
                    continue
                else:
                    selected_bhavgeets.append(os.path.join(bhavgeet_root_path, folder, selected_bhavgeet))
                    break
        return selected_bhavgeets
        
    
    def retrieve_stotra_path(self):
        stotras_root_path = "/home/pi/vlc_scheduler/audio_content/stotras"
        day_of_week = calendar.day_name[date.today().weekday()].lower()
        stotra_day_path = os.path.join(stotras_root_path, day_of_week)
        if not os.path.exists(stotra_day_path):
            log_message("Stotra path {} could not be found".format(
                stotra_day_path), 'warning')
            return []
        stotras = os.listdir(stotra_day_path)
        if len(stotras) <= 0:
            log_message("Stotra folder {} is empty".format(stotra_day_path), 'warning')
        random_index = random.randint(0, (len(stotras)-1))
        selected_stotra = stotras[random_index]
        return os.path.join(stotra_day_path, selected_stotra)

    def play_file(self, file_path):
        p = vlc.MediaPlayer("file://{}".format(file_path))
        ret = p.play()
        time.sleep(self.pooling_duration)
        while p.is_playing():
            log_message("Playing", 'info')
            time.sleep(self.pooling_duration)
            break
        log_message("Finishing the play", 'info')
        p.release()
        return
    
    def start_playlist(self):
        playlist = [self.retrieve_stotra_path()] + self.retrieve_bhavgeet_paths()
        log_message("Today date {}, playlist: {}".format(date.today(), playlist), 'info')
        for file_ in playlist:
            filename, file_extension = os.path.splitext(file_)
            file_path = os.path.join(self.folder_path, file_)
            if file_extension.lower() in ['.mp3', '.wav']:
                log_message("Now started playing {} ".format(file_path), 'info')
                try:
                    self.play_file(file_path)
                    # pass
                except Exception as e:
                    log_message("Ran into error {} while playing {}".format(str(e), file_path), 'error')
                    continue
            else:
                log_message("Skipping {} since it is not an MP3".format(file_path), 'warning')
