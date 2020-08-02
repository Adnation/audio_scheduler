from python_audio_player import AudioScheduler

def audio_player_job():
    scheduler = AudioScheduler()
    scheduler.start_playlist()

def sunday_player_job():
    scheduler = AudioScheduler()
    scheduler.play_sunday_playlist()
