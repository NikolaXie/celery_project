# coding=utf-8

import datetime

end = '2017-07-01'

datestart = datetime.date.today().isoformat()
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

while datestart < dateend:
    datestart += datetime.timedelta(days=1)
    print(datestart.strftime('%Y-%m-%d'))