import sys
import os
from flask import Flask
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler

from entrypoint import audio_player_job

app = Flask(__name__)

morning_scheuler = CronTrigger(hour=7, minute=30, second=00)
sunday_kendra_schedular = CronTrigger(hour=10, minute=0, second=0, day_of_week='sun')
test1_trigger = CronTrigger(hour=0, minute=31, second=00)
test2_trigger = CronTrigger(hour=0, minute=27, second=00)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(audio_player_job, trigger=morning_scheuler)
scheduler.add_job(audio_player_job, trigger=sunday_kendra_schedular)
# scheduler.add_job(audio_player_job, trigger=test1_trigger)
# scheduler.add_job(audio_player_job, trigger=test2_trigger)
scheduler.start()


@app.route("/home")
def home():
    """ Function for test purposes. """
    return "Welcome Home :) !"


if __name__ == "__main__":
    app.run()
