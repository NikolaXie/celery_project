# coding=utf-8
# coding=utf-8
import requests
from pyquery import PyQuery as pq
import re
import json
import datetime
from threading import Thread, Lock


class AKspider(object):

    def time_format(self, date_time):
        info = re.split(' |/', date_time)
        new_info = info[2] + info[0] + info[1] + info[3]
        return new_info.replace(':', '')

    def search(self, data):
        # date_time = '2018-10-28'
        data_list = self.get_date_list(data['finsh_date'])
        # return
        # url = 'https://booking.airasia.com/Flight/Select?o1=PEK&d1=PEN&culture=zh-CN&dd1=2018-10-26&ADT=1&s=true&mon=true&cc=CNY&c=false'
        for date_ in data_list:
            url = 'https://booking.airasia.com/Flight/Select?o1=%s&d1=%s&culture=zh-CN&dd1=%s&ADT=1&s=true&mon=true&cc=CNY&c=false' % \
                  (data['depAirport'], data['arrAirport'], date_)
            result = requests.get(url).text
            pq_content = pq(result)

            flight_list = pq_content('input[id*="trip_"]')
            if not flight_list:
                pass
            else:
                self.parse(flight_list)

    def get_date_list(self, date_time):
        datestart = datetime.datetime.today()
        dateend = datetime.datetime.strptime(date_time, '%Y-%m-%d')
        date_list = []
        while datestart < dateend:
            datestart += datetime.timedelta(days=1)
            date_list.append(datestart.strftime('%Y-%m-%d'))
        print(date_list)
        return date_list

    def parse(self, flight_list):
        with open('item.json', 'a') as f:
            for flight in flight_list:
                try:
                    flight = pq(flight)
                    sell_key = flight.val()
                    print(sell_key)
                    left_info, right_info = sell_key.split('|')
                    left_info_list = left_info.split('~')
                    right_info_list = re.split(r'[~]+ *', right_info)
                    cabin = left_info_list[1]
                    arrAirport = right_info_list[-3]
                    arrTime = self.time_format(right_info_list[4])
                    carrier = right_info_list[0]
                    depAirport = right_info_list[3]
                    depTime = self.time_format(right_info_list[-2])
                    flightNumber = right_info_list[1]
                    flight_info_json = flight.attr('data-json')
                    currency = flight.attr('data-cur')
                    price_info = json.loads(flight_info_json)
                    price = float(price_info[0]['price'])
                    item = {
                        "arrAirport": arrAirport,
                        "arrTime": arrTime,
                        "cabin": cabin,
                        "carrier": carrier,
                        "depAirport": depAirport,
                        "depTime": depTime,
                        "flightNumber": flightNumber,
                        "currency":currency,
                        "price":price
                    }
                    print(item)
                    f.write(str(item))
                except:
                    pass



if __name__ == '__main__':
    data = {
        'arrAirport': 'JHB',
        'depAirport': 'KUL',
        'finsh_date': '2018-11-01'
    }
    akspider = AKspider()
    akspider.search(data)