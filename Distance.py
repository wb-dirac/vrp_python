import math


def rad(d):
    return d * math.pi / 180.0


def get_distance(lat1, lng1, lat2, lng2):
    radlat1 = rad(lat1)
    radlat2 = rad(lat2)
    a = radlat1 - radlat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(
        math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radlat1) * math.cos(radlat2) * math.pow(math.sin(b / 2), 2)))
    earth_radius = 6378137
    s *= earth_radius
    #s = round(s)
    if s < 0:
        return -s
    else:
        return s


if __name__ == "__main__":
    print(get_distance(40.030979, 116.411018, 40.015311000, 116.422638000))
