from celery import Celery

app = Celery('passgage', broker='redis://redis:6379/0')

import tasks