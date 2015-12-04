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
    with open(filename,'at') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(rows)


def run(filename, date):
    car_list = get_orders(filename, '2015/10/01')
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

if __name__ == '__main__':
    date = '2015/10/01'
    filename = './resource/order_data/order2.csv'
    # run(date, filename)
    car_list = {}
    with open(filename) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for row in f_csv:
            if row[0] == date:
                car_list[row[1]] = row[5]
    headers = ['日期', '用户ID', '经度', '纬度', '车辆编号', '距离', '时间']
    wf = './resource/order_data/result2.csv'
    with open(wf, 'at') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        with open('./resource/order_data/result.csv') as r1:
            fr1_csv = csv.reader(r1)
            next(fr1_csv)
            for row in fr1_csv:
                if len(row[1]) > 1:
                    car_num = car_list[row[1]]
                else:
                    car_num = ''
                row.insert(4, car_num)
                f_csv.writerow(row)