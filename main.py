import random
import Distance
import csv


def get_orders(filename, date):
    """
    从文件中读取order
    :param filename:
    :param date:
    :return:
    """
    order_dict = {}
    with open(filename) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for row in f_csv:
            if row[0] == date:
                key = (round(float(row[3]), 6), round(float(row[4]), 6))
                if key not in order_dict:
                    order_dict[key] = []
                order_dict[key].append(row[1])
    orders = [{"lng": latlng[0], "lat": latlng[1], "ids": order_dict[latlng]} for latlng in order_dict]

    return orders


def init_group(length, count):
    """
    产生长度为length的count个初始群体
    :param length:
    :param count:
    :return:
    """
    group = []
    lit = list(range(1, length + 1))
    for i in range(0, count):
        tmp = lit[:]
        random.shuffle(tmp)
        group.append(tmp)
    return group


def separate_path(all_orders, path, condition, params):
    """
    将一个序列分离为满足条件的车辆路径
    :type all_orders: list
    :type path: list
    :type condition: dict
    :type params: dict
    """
    assert len(all_orders) - 1 == len(path)
    separate_number_list = []

    start = all_orders[0]  # 起点
    v = params['velocity']  # 速度
    stay_time = params['stay_time']  # 停留时间

    path_time = 0  # 记录每车的总时间
    path_len = len(path)  # 路径长度，不包括起点
    i = 0  # 路径中 node 的指针
    pre = start
    total_distance = 0
    while i < path_len:
        curr_node = all_orders[path[i]]
        distance = Distance.get_distance(pre['lat'], pre['lng'], curr_node['lat'], curr_node['lng'])
        time = distance / v
        if path_time + time > condition["time"]:
            # 重置迭代变量
            if pre == start:
                raise RuntimeError("经纬度{}离原点{}太远".format(curr_node, pre))
            path_time = 0
            pre = start
            separate_number_list.append(i)
        else:
            pre = curr_node
            path_time += time + stay_time
            total_distance += distance
            i += 1

    separate_number_list.append(i)
    return {"separate_number_list": separate_number_list, "distance": total_distance}


def main():
    """
    原饭盟的仓库地址为：经度：116.282381；维度：39.643378
    Let's go!
    :return:
    """
    o = {'lng': 116.282381, 'lat': 39.643378, 'ids': 'O'}
    # print(Distance.get_distance(40.030979, 116.411018, 40.015311000, 116.422638000))
    orders = get_orders('./resource/order_data/order.csv', '2015/9/26')
    print("orders len is", len(orders))
    group = init_group(len(orders), 200)
    orders.insert(0, o)
    print(orders)
    condition = {'time': 240}
    params = {'velocity': 500, 'stay_time': 10}
    min_vcount = len(orders)

    min_dis = 2 ** 30
    for path in group:
        separate_info = separate_path(orders, path, condition, params)
        min_vcount = min(min_vcount, len(separate_info["separate_number_list"]))
        if min_dis > separate_info['distance']:
            min_dis = separate_info["distance"]
            min_path = path
            min_separate_info = separate_info
            # print(separate_info)
    cars = []
    start_number = 0
    for separate_number in min_separate_info["separate_number_list"]:
        cars.append(min_path[start_number:separate_number])
        start_number = separate_number
    print("min vehicle is: ", min_vcount)
    print("min path is: ", min_path)
    print("min min_sep is: ", min_separate_info)
    print("cars is: ", cars)
    print("min distance is: ", min_dis)


if __name__ == '__main__':
    main()
    # orders = get_orders('./resource/order_data/order.csv', '2015/9/26')
    # print(orders)
