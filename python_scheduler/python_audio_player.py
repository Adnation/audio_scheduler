import os
import vlc
import sys
import time
import random
import logging
import calendar
from datetime import date, datetime
from logger_utility import log_message


logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__file__)


class TimeToStopError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class AudioScheduler:

    def __init__(self):
        self.folder_path = "/home/pi/vlc_scheduler/audio_content/general"
        self.pooling_duration = 60
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
                    # log_message("Skipping {} ".format(selected_bhavgeet), 'debug')
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
            return []
        random_index = random.randint(0, (len(stotras)-1))
        selected_stotra = stotras[random_index]
        return os.path.join(stotra_day_path, selected_stotra)

    def play_file(self, file_path):
        p = vlc.MediaPlayer("file://{}".format(file_path))
        ret = p.play()
        time.sleep(self.pooling_duration)
        while p.is_playing():
            # log_message("Playing", 'info')
            time.sleep(self.pooling_duration + 60)
            # break
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

    def select_sunday_bhavgeets(self, number_of_bhavegeets_to_play=5):
        bhavgeet_root_path = "/home/pi/vlc_scheduler/audio_content/bhavgeet"
        all_bhavgeet_folders = os.listdir(bhavgeet_root_path)
        selected_folders = random.choices(all_bhavgeet_folders, number_of_bhavegeets_to_play)
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

    def play_sunday_file(self, file_path):
        p = vlc.MediaPlayer("file://{}".format(file_path))
        ret = p.play()
        time.sleep(self.pooling_duration)
        today = date.today()
        break_time = datetime(
            year=today.year, 
            month=today.month,
            day=today.day,
            hour=10,
            minute=25,
            second=00
        )
        if datetime.now() < break_time:
            raise TimeToStopError("Time to start Kendra")
        while p.is_playing():
            # log_message("Playing", 'info')
            time.sleep(self.pooling_duration)
            if datetime.now() < break_time:
                raise TimeToStopError("Time to start Kendra")
        log_message("Finishing the play", 'info')
        p.release()

    def play_sunday_playlist(self,):
        for file_ in self.select_sunday_bhavgeets():
            _, file_extension = os.path.splitext(file_)
            file_path = os.path.join(self.folder_path, file_)
            if file_extension.lower() in ['.mp3', '.wav']:
                log_message("Now started playing {} ".format(file_path), 'info')
                try:
                    self.play_sunday_file(file_path)
                except TimeToStopError as e:
                    log_message("Time to stop the player ", "info")
                    break
                except Exception as e:
                    log_message("Ran into error {} while playing {}".format(str(e), file_path), 'error')
                    continue
            else:
                log_message("Skipping {} since it is not an MP3".format(file_path), 'warning')
