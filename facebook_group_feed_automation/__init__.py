from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)

celery_app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'tasks.start_saving_process',
        'schedule': crontab(minute=1),
        # 'args': (16, 16),
    },
}
