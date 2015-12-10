import csv
import json
from urllib import request, parse
import random


def index():
    date = '2015/10/01'
    filename = './resource/order_data/order2.csv'
    car_list = get_orders(filename, date)
    return car_list


def get_orders(filename, date):
    """
    从文件中读取order, 车辆编号为key的字典，value是order list
    :param filename:
    :param date:
    :return:
    """
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


def get_orders_from_group_api():
    url = 'http://172.16.1.146:8086/order/allocat/groupOrder'
    car_list = {}
    with request.urlopen(url) as resp:
        for line in resp:
            line = line.decode('utf-8')  # Decoding the binary data to text.
            json_data = json.loads(json.loads(line))
            for car in json_data:
                car_num = car['areaNum']
                car_list[car_num] = []
                orders = car['orders']
                car_list[car_num] = [{'id': order['userId'], 'longitude': order['lngLats'][0],
                                      'latitude': order['lngLats'][1]} for order in orders]
    return car_list


def write_csv(filename, rows):
    with open(filename, 'at') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(rows)


def path_rounting(car_list, date, start):
    """
    根据某个订单文件中某天的分车结果计算起最优路径
    :param car_list:
    :param date:
    :return:
    """

    # print(car_list)
    maxl = 0
    headers = [['日期', '用户ID', '经度', '纬度', '车辆编号', '距离', '时间']]
    wf = ''.join(['./resource/order_data/result', str(random.random()), ".csv"])
    write_csv(wf, headers)
    for car_num in car_list:
        maxl = max(maxl, len(car_list[car_num]))
        car_list[car_num].insert(0, start)
        print(car_num, "->", car_list[car_num])
        params = {"points": json.dumps(car_list[car_num]), "isBack": False}
        querystring = parse.urlencode(params)
        url = "http://172.16.1.146:8086/order/allocat/getMinPath?" + querystring
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
                    line2 = [date, row['node']['id'], row['node']['longitude'], row['node']['latitude'], car_num,
                             row['distance'],
                             row['time']]
                    data.append(line2)
                data.append(['本车合计', '', '', '', car_num, dis, time])
                write_csv(wf, data)
        # break
    print(maxl)


def calulate_sum_distance():
    filename = './resource/order_data/result2.csv'
    total = 0
    car_count = 0
    with open(filename) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for row in f_csv:
            if row[1] == '':
                car_count += 1
                total += int(row[5])
    return {'distance': total, 'car_count': car_count}

if __name__ == '__main__':
    date = '2015/10/01'
    filename = './resource/order_data/order2.csv'
    start = {'longitude': 116.282381, 'latitude': 39.643378, 'id': 'O'}
    # print(json.dumps(index()))
    car_list = get_orders_from_group_api()
    path_rounting(car_list, date, start)
    # tocal = calulate_sum_distance()
    # print(tocal)
