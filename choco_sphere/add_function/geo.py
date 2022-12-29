from geopy.distance import geodesic as GD
from geopy.geocoders import Nominatim

import config

from datetime import datetime

gn = Nominatim(user_agent='BuyiXiao')


def find_distance(address, type_place=1):
    start_address = config.START_ADDRESS
    location_1 = gn.geocode(start_address)
    w_1, h_1 = location_1.latitude, location_1.longitude
    if type_place == 1:
        location_2 = gn.geocode(address)

        w_2, h_2 = location_2.latitude, location_2.longitude
    else:
        w_2, h_2 = address.split(' - ')[0], address.split(' - ')[1]
    return GD((w_1, h_1), (w_2, h_2))


# print(find_distance("11-я Парковая ул., 36, Москва, 105077"))
# res = find_distance("11-я Парковая ул., 36, Москва, 105077")
# print(str(res).split()[0])
# print(find_distance("'11-я Парковая улица, 36'"))
# print(find_distance("Дворцовая улица, 14, Сочи"))
# print(find_distance("43.685319 - 40.200686", type_place=2))
#


