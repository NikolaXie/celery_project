# coding=utf-8
from celery_.tasks import send_email

if __name__ == '__main__':
    result = send_email.delay(4,4)
    if 1:
        print('hello')
