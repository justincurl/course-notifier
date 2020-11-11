from apscheduler.schedulers.blocking import BlockingScheduler
from notifier import notify

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def update_notifier():
 	notify(False)

@sched.scheduled_job('cron', day_of_week='mon-sun', hour='19', timezone='America/New_York')
def update_notifier_true():
 	notify(True)

sched.start()