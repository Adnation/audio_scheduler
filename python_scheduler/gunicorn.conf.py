bind = "127.0.0.1:5000"
daemon = True
workers = 1
accesslog = "/home/pi/vlc_scheduler/scheduler_logs/gunicorn_access.log"
errorlog = "/home/pi/vlc_scheduler/scheduler_logs/gunicorn_error.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
