import sys
import os
from flask import Flask
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler

from entrypoint import audio_player_job
from logger_utility import LOGGING_DIR

app = Flask(__name__)

morning_scheuler = CronTrigger(hour=7, minute=30, second=00)
sunday_kendra_schedular = CronTrigger(hour=10, minute=0, second=0, day_of_week='sun')
test1_trigger = CronTrigger(hour=14, minute=22, second=00)
test2_trigger = CronTrigger(hour=0, minute=27, second=00)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(audio_player_job, trigger=morning_scheuler)
scheduler.add_job(audio_player_job, trigger=sunday_kendra_schedular)
# scheduler.add_job(audio_player_job, trigger=test1_trigger)
# scheduler.add_job(audio_player_job, trigger=test2_trigger)
scheduler.start()

@app.route("/logs/", defaults={'lines': 200})
@app.route("/logs/<lines>")
def retrieve_logs(lines=200):
    """ Function for test purposes. """
    fp = open(os.path.join(LOGGING_DIR, 'audio_play.logs'))
    # fp.read()
    return "<pre>{}</pre>".format(fp.read())


if __name__ == "__main__":
    app.run(debug=True)
