import csv
import json
from urllib import request, parse


def get_orders(filename, date):
    "从文件中读取order"
    car_list = {}
    with open(filename) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for row in f_csv:
            if row[0] == date:
                order = {'id': row[1], 'longitude': round(float(row[3]), 6), 'latitude': round(float(row[4]), 6)}
                if row[5] not in car_list.keys():
                    car_list[row[5]] = []
                car_list[row[5]].append(order)
    return car_list


def write_csv(filename, rows):
    # headers = ['Symbol','Price','Date','Time','Change','Volume']
    # rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
    #          ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
    #         ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
    #         ]

    with open(filename,'at') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(rows)


if __name__ == '__main__':
    date = '2015/10/01'
    car_list = get_orders('./resource/order_data/order2.csv', '2015/10/01')
    # print(car_list)
    maxl = 0
    headers = [['日期', '用户ID', '经度', '纬度', '距离', '时间']]
    wf = './resource/order_data/result.csv'
    write_csv(wf, headers)
    for car_num in car_list:
        maxl = max(maxl, len(car_list[car_num]))
        car_list[car_num].insert(0, {'longitude': 116.212842, 'latitude': 39.898777, 'id': 'O'})
        print(car_num, "->", car_list[car_num])
        params = {"points": json.dumps(car_list[car_num]), "isBack": False}
        querystring = parse.urlencode(params)
        url = "http://localhost:8080/allocat/getMinPath?" + querystring
        with request.urlopen(url) as resp:
            for line in resp:
                line = line.decode('utf-8')  # Decoding the binary data to text.
                json_data = json.loads(json.loads(line))
                data = []
                dis = 0
                time = 0
                for row in json_data:
                    dis += row['distance']
                    time += row['time']
                    line2 = [date, row['node']['id'], row['node']['longitude'], row['node']['latitude'], row['distance'],
                             row['time']]
                    data.append(line2)
                data.append(['本车合计', '', '', '', dis, time])
                write_csv(wf, data)
        # break
    print(maxl)