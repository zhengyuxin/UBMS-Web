import os
import sys
import time

from celery import Celery


app = Celery('test', broker='amqp://guest@localhost//')
app.config_from_object('celeryconfig')



@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
