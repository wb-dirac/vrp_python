import random
import Distance


def init_group(length, count):
    """产生长度为length的count个初始群体"""
    group = []
    lit = list(range(1, length + 1))
    for i in range(0, count):
        tmp = lit[:]
        random.shuffle(tmp)
        group.append(tmp)
    return group


def get_end_index_list(all_orders, path, condition, params):
    end_index_list = []
    start = all_orders[0]
    pre = start
    v = params['velocity']
    path_time = 0
    for i in range(0, len(path)):
        curr_node = all_orders[path[i]]
        distance = Distance.get_distance(pre, curr_node)
        time = distance / v
        if(path_time + time > condition["time"]):
            #重置迭代变量
            path_time = 0
            pre = start
            end_index_list.append(i - 1)
        else:
            pre = curr_node
            path_time += time

    end_index_list.append(len(path) - 1)
    return end_index_list


#def get_distance(point1, point2):


print(Distance.get_distance(40.030979, 116.411018, 40.015311000, 116.422638000))
