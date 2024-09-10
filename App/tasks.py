from worker import app
from api import GetPersonalData, updateOrCreatePassgage
from celery.schedules import crontab

@app.task
def run_GetPersonalData():
    GetPersonalData()

@app.task
def run_UpdateOrCreatePassgage():
    updateOrCreatePassgage()

def setup_periodic_tasks(sender, **kwargs):
    # Dakikada bir run_GetPersonalData çalıştır
    sender.add_periodic_task(60.0, run_GetPersonalData.s(), name='run every minute')

    # Saatte bir run_UpdateOrCreatePassgage çalıştır
    sender.add_periodic_task(crontab(minute=0), run_UpdateOrCreatePassgage.s(), name='run every hour')