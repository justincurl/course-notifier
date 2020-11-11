from apscheduler.schedulers.blocking import BlockingScheduler
from notifier import notify

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def update_notifier():
 	notify()

sched.start()