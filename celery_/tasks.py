# coding=utf-8
import celery
from celery import Celery
from celery.utils.log import get_task_logger
import time
logger = get_task_logger(__name__)
app = Celery('tasks',broker='redis://47.98.126.208:6379/0',backend='redis://47.98.126.208:6379/0')
@app.on_after_configure.connect
def set_schdule(sender, **kwargs):
    sender.add_periodic_task(20.0, xssum.s(2,3), name='add every 11',queue='feed')
    sender.add_periodic_task(20.0, xsum.s(2,3), name='add every 10',queue='feeds')
    app.send_task('celery_.tasks.xsum',args=(3,4))



@app.task
def send_email(a,b):
    logger.info('adding {0} + {1}'.format(a,b))
    return a+b

@app.task(bind=True,name='celery_.tasks.hello', queue='hello')
def hello(self, a, b):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(1)
    print('hello world: %i' % (a+b))
    return a+b

@app.task(name='celery_.tasks.xsum')
def xsum(a,b):
    print(a+b)
    return a+b

@app.task(name='celery_.tasks.xssum', queue='feed')
def xssum(a,b):
    print(a+b)
    return a+b

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'celery_.tasks.xsum',
        'schedule': 15.0,
        'args': (16, 16),
        'options':{'queue':'feeds'}
    },
}
app.conf.task_default_queue = 'default'
app.conf.task_routes = {'celery_.app.xsum': {'queue': 'feeds'}}

if __name__ == '__main__':
    result = send_email.delay(4,4)
    if 1:
        print('hello')
    if 2:
        print('sdfsd')