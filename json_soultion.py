# coding=utf-8
data = {'arrAirport': 'JHB', 'arrTime': '201810282255', 'cabin': 'ZF', 'carrier': 'AK', 'depAirport': 'KUL', 'depTime': '201810282350', 'flightNumber': '6038', 'currency': 'MYR', 'price': 218.48}
with open('item.json', 'a') as f:
    f.write(data)