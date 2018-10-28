# coding=utf-8
import requests
from pyquery import PyQuery as pq
import re
import json
# url = 'https://booking.airasia.com/Flight/Select?o1=PEK&d1=PEN&culture=zh-CN&dd1=2018-10-26&dd2=2018-10-31&r=true&ADT=1&s=true&mon=true&cc=CNY&c=false'
url = 'https://booking.airasia.com/Flight/Select?o1=PEK&d1=PEN&culture=zh-CN&dd1=2018-10-26&ADT=1&s=true&mon=true&cc=CNY&c=false'
result = requests.get(url).text
pq_content = pq(result)

flight_list = pq_content('input[id*="trip_"]')
print(type(flight_list))
print(flight_list)


def time_format(shijian):
    info = re.split(' |/',shijian)
    new_info = info[2] + info[0] + info[1] + info[3]
    return new_info.replace(':', '')

for flight in flight_list:
    flight = pq(flight)
    sell_key = flight.value
    print(sell_key)
    left_info,right_info = sell_key.split('|')
    left_info_list = left_info.split('~')
    right_info_list = re.split(r'[~]+ *', right_info)
    cabin = left_info_list[1]
    arrAirport = right_info_list[-3]
    arrTime = time_format(right_info_list[4])
    carrier = right_info_list[0]
    depAirport = right_info_list[3]
    depTime = time_format(right_info_list[-2])
    flightNumber = right_info_list[1]
    flight_info_json = flight.attr('data-json')
    currency = flight.attr('data-cur')
    price_info = json.loads(flight_info_json)
    price = float(price_info[0]['price'])
    item = {
        "arrAirport": arrAirport,
        "arrTime": arrTime,
        "cabin":cabin,
        "carrier":carrier,
        "depAirport": depAirport,
        "depTime":depTime,
        "flightNumber": flightNumber
    }
