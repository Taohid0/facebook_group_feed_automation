from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)

# CELERY_BEAT_SCHEDULE = {
#     'task-number-one': {
#         'task': 'read_feed.tasks.test',
#         'schedule': crontab(minute="*/1")
#     },
# }

celery_app.conf.beat_schedule = {
    'start_saving_process': {
        'task': 'read_feed.tasks.start_saving_process',
        'schedule': crontab(minute="*/1"),
    },
}
