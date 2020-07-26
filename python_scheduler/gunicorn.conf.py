bind = "127.0.0.1:5000"
daemon = True
workers = 1
accesslog = "logs/audio_player_access.log"
errorlog = "logs/audio_player.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
