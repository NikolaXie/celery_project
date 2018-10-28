# coding=utf-8
import requests

print(requests.get('https://weibo.com/?category=0').text)