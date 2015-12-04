import random
import Distance
import csv


def get_orders(filename, date):
    "从文件中读取order"
    order_list = []
    with open(filename) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for row in f_csv:
            if row[0] == date:
                order = {'id': row[1], 'lng': round(float(row[3]), 6), 'lat': round(float(row[4]), 6)}
                order_list.append(order)
    return order_list


def init_group(length, count):
    """
    产生长度为length的count个初始群体
    """
    group = []
    lit = list(range(1, length + 1))
    for i in range(0, count):
        tmp = lit[:]
        random.shuffle(tmp)
        group.append(tmp)
    return group


def get_end_index_list(all_orders, path, condition, params):
    """
    :type all_orders: list
    :type path: list
    :type condition: dict
    :type params: dict
    """
    assert len(all_orders) - 1 == len(path)
    end_index_list = []

    start = all_orders[0]
    v = params['velocity']
    stay_time = params['stay_time']

    path_time = 0
    path_len = len(path)
    i = 0
    pre = start
    while i < path_len:
        curr_node = all_orders[path[i]]
        distance = Distance.get_distance(pre['lat'], pre['lng'], curr_node['lat'], curr_node['lng'])
        time = distance / v
        if path_time + time > condition["time"]:
            #重置迭代变量
            if pre == start:
                raise RuntimeError("经纬度{}离原点{}太远".format(curr_node, pre))
            path_time = 0
            pre = start
            end_index_list.append(i - 1)
        else:
            pre = curr_node
            path_time += time + stay_time
            i += 1

    end_index_list.append(i)
    return end_index_list


#def get_distance(point1, point2):

if __name__ == '__main__':


    #原饭盟的仓库地址为：经度：116.282381；维度：39.643378
    o = {'lng': 116.212842, 'lat': 39.898777, 'id': 'O'}
    # print(Distance.get_distance(40.030979, 116.411018, 40.015311000, 116.422638000))
    orders = get_orders('/home/wb/workspace/order-allocation/src/main/resources/data/order.csv', '2015/9/20')
    print("orders len is", len(orders))
    group = init_group(len(orders), 200)
    orders.insert(0, o)
    print(orders)
    condition = {'time': 240}
    params = {'velocity': 500, 'stay_time': 10}
    min_vcount = len(orders)
    for path in group:
        end_index_list = get_end_index_list(orders, path, condition, params)
        min_vcount = min(min_vcount, len(end_index_list))
        print(end_index_list)
    print("min vehicle is: ", min_vcount)