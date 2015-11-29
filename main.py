import random
def init_group(length, count):
    """Init Group of count DNA and each length is length"""
    group = []
    lit = list(range(1, length))
    for i in range(0, count):
        tmp = lit[:]
        random.shuffle(tmp)
        tmp.insert(0, 0)
        group.append(tmp)
    return group

print(init_group(10, 5))
