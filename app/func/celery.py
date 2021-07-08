from celery import Celery

celery = Celery('func',
             broker='redis://localhost:6379/0',
             backend='rredis://localhost:6379/0',
             include=['func.fixtures_task'])

if __name__ == '__main__':
    celery.start()