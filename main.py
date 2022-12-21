from urllib.request import urlretrieve
import urllib.request as req
import pandas as pd
import math
import os
import time
import vk
from datetime import date, datetime
from dateutil.parser import parse
from itertools import groupby
from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt
from dotenv import load_dotenv

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def is_full_date(string):
    try:
        is_full = len((string).split('.')) == 3
        if is_full:
            parse(string)
            return True
        else:
            raise ValueError
    except ValueError:
        return False


def is_get_city(person):
    try:
        city = person['city']
        return True
    except Exception:
        return False


def key_func(k):
    return k['city']['title']

load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

vkapi = vk.API(
    access_token=ACCESS_TOKEN,
    v='5.81')

# #region Downloading Photos
# hse_url = 'https://vk.com/hse'
# hse_id = '-25205856'
#
# hse_albums = vkapi.photos.getAlbums(owner_id = hse_id)
# albums_count = hse_albums['count']
# albums_items = list(map(lambda x: {'id': x['id'],
#                                    'title': x['title'],
#                                    'size': x['size']}, hse_albums['items']))
#
# for album in albums_items:
#     print('------------------------------------------------------------------------')
#     album_id = album['id']
#     album_photos = vkapi.photos.getAlbums(owner_id=hse_id, album_ids=album_id)
#     # print(album)
#     photos_count = album['size']
#     album_name = album['title'].replace((" ", ":", "/"), "_")
#
#     print(album_name)
#
#     counter = 0
#     prog = 0
#     breaked = 0
#     time_now = time.time()
#
#     if not os.path.exists('saved'):
#         os.mkdir('saved')
#     photo_folder = f'saved/{album_name}'
#     if not os.path.exists(photo_folder):
#         os.mkdir(photo_folder)
#
#     for j in range(math.ceil(photos_count / 1000)):
#         photos = vkapi.photos.get(owner_id=hse_id, album_id=album_id, count=1000, offset=j * 1000)
#         for photo in photos["items"]:
#             counter += 1
#             url = photo["sizes"][0]["url"]
#             print('Загружаю фото № {} из {}. Прогресс: {} %'.format(counter, photos_count, prog))
#             prog = round(100 / photos_count * counter, 2)
#             try:
#                 # with req.urlopen(url) as d, open(photo_folder + "/" + photo['id'], 'wb') as opfile:
#                 #     data = d.read()
#                     # opfile.write(data)
#                 urlretrieve(url, photo_folder + "/" + str(photo['id']))  # Загружаем и сохраняем файл
#             except Exception as e:
#                 print(e)
#                 print('Произошла ошибка, файл пропущен.')
#                 breaked += 1
#                 continue
#     time_for_dw = time.time() - time_now
#     print(
#         "\nВ очереди было {} файлов. Из них удачно загружено {} файлов, {} не удалось загрузить. Затрачено времени: {} сек.".format(
#             photos_count, photos_count - breaked, breaked, round(time_for_dw, 1)))
# #endregion

programming_group_id = 113958919
i_am_programmer_group_id = 49131654

programming_group_members = vkapi.groups.getMembers(group_id=programming_group_id,
                                                    fields=('sex', 'city', 'contacts', 'country', 'bdate'))
i_am_programmer_group_members = vkapi.groups.getMembers(group_id=i_am_programmer_group_id,
                                                        fields=('sex', 'city', 'contacts', 'country', 'bdate'))

programming_group_total_members = programming_group_members['count']
i_am_programmer_group_total_members = i_am_programmer_group_members['count']

print(f'Всего участников в группе "Программирование / itProger" = {programming_group_total_members}')
print(f'Всего участников в группе "Я - Программист" = {i_am_programmer_group_total_members}')

print('--------------------------------------')
print('Анализируем по выборке из 1000 человек')

programming_group_members = programming_group_members['items']
i_am_programmer_group_members = i_am_programmer_group_members['items']
# region sex percent
programming_group_women_count = sum(p['sex'] == 1 for p in programming_group_members)
programming_group_women_percent = round(programming_group_women_count / len(programming_group_members), 2)
programming_group_men_count = sum(p['sex'] == 2 for p in programming_group_members)
programming_group_men_percent = round(programming_group_men_count / len(programming_group_members), 2)

print('В группе "Программирование / itProger"')
print('Процент девушек = ' + str(programming_group_women_percent) + '%')
print('Процент мужчин = ' + str(programming_group_men_percent) + '%')

i_am_programmer_group_women_count = sum(p['sex'] == 1 for p in i_am_programmer_group_members)
i_am_programmer_group_women_percent = round(i_am_programmer_group_women_count / len(i_am_programmer_group_members), 2)
i_am_programmer_group_men_count = sum(p['sex'] == 2 for p in i_am_programmer_group_members)
i_am_programmer_group_men_percent = round(i_am_programmer_group_men_count / len(i_am_programmer_group_members), 2)

print('\nВ группе "Я - Программист"')
print('Процент девушек = ' + str(i_am_programmer_group_women_percent) + '%')
print('Процент мужчин = ' + str(i_am_programmer_group_men_percent) + '%')
# endregion
# region age percent
programming_group_members_with_bdate = list(
    filter(lambda person: person.__contains__('bdate') and is_full_date(person['bdate']), programming_group_members))
programming_group_under_18_count = sum(
    calculate_age(pd.to_datetime(p['bdate'], format="%d.%m.%Y")) <= 18 for p in programming_group_members_with_bdate)
programming_group_under_30_count = sum(18 < calculate_age(pd.to_datetime(p['bdate'], format="%d.%m.%Y")) <= 30 for p in
                                       programming_group_members_with_bdate)
programming_group_under_45_count = sum(30 < calculate_age(pd.to_datetime(p['bdate'], format="%d.%m.%Y")) <= 45 for p in
                                       programming_group_members_with_bdate)

programming_group_under_18_percent = programming_group_under_18_count / len(programming_group_members_with_bdate)
programming_group_under_30_percent = programming_group_under_30_count / len(programming_group_members_with_bdate)
programming_group_under_45_percent = programming_group_under_45_count / len(programming_group_members_with_bdate)

print('\nВ группе "Программирование / itProger"')
print('Процент пользователей до 18 лет = ' + str(round(programming_group_under_18_percent * 100, 2)) + '%')
print('Процент пользователей от 18 до 30 лет = ' + str(round(programming_group_under_30_percent * 100, 2)) + '%')
print('Процент пользователей от 30 до 45 лет = ' + str(round(programming_group_under_45_percent * 100, 2)) + '%')

i_am_programmer_group_members_with_bdate = list(
    filter(lambda person: person.__contains__('bdate') and is_full_date(person['bdate']),
           i_am_programmer_group_members))
i_am_programmer_group_under_18_count = sum(calculate_age(pd.to_datetime(p['bdate'], format="%d.%m.%Y")) <= 18 for p in
                                           i_am_programmer_group_members_with_bdate)
i_am_programmer_group_under_30_count = sum(
    18 < calculate_age(pd.to_datetime(p['bdate'], format="%d.%m.%Y")) <= 30 for p in
    i_am_programmer_group_members_with_bdate)
i_am_programmer_group_under_45_count = sum(
    30 < calculate_age(pd.to_datetime(p['bdate'], format="%d.%m.%Y")) <= 45 for p in
    i_am_programmer_group_members_with_bdate)

i_am_programmer_group_under_18_percent = i_am_programmer_group_under_18_count / len(
    i_am_programmer_group_members_with_bdate)
i_am_programmer_group_under_30_percent = i_am_programmer_group_under_30_count / len(
    i_am_programmer_group_members_with_bdate)
i_am_programmer_group_under_45_percent = i_am_programmer_group_under_45_count / len(
    i_am_programmer_group_members_with_bdate)

print('\nВ группе "Я - Программист"')
print('Процент пользователей до 18 лет = ' + str(round(i_am_programmer_group_under_18_percent * 100, 2)) + '%')
print('Процент пользователей от 18 до 30 лет = ' + str(round(i_am_programmer_group_under_30_percent * 100, 2)) + '%')
print('Процент пользователей от 30 до 45 лет = ' + str(round(i_am_programmer_group_under_45_percent * 100, 2)) + '%')

# endregion
# region city count
programming_group_members_with_city = list(
    filter(lambda person: person.__contains__('city'), programming_group_members))
programming_group_members_sorted_by_city = sorted(programming_group_members_with_city, key=key_func)

programming_group_members_groupby_city = [{'city': key,
                                           'count': sum(1 for x in group)}
                                          for key, group in groupby(programming_group_members_sorted_by_city, key_func)]
programming_group_members_groupby_city = sorted(programming_group_members_groupby_city, key=itemgetter('count'),
                                                reverse=True)

print('\nВ группе "Программирование / itProger"')
print(
    f'{programming_group_members_groupby_city[0]["count"]} участников из города {programming_group_members_groupby_city[0]["city"]}')
print(
    f'{programming_group_members_groupby_city[1]["count"]} участников из города {programming_group_members_groupby_city[1]["city"]}')
print(
    f'{programming_group_members_groupby_city[2]["count"]} участников из города {programming_group_members_groupby_city[2]["city"]}')

i_am_programmer_group_members_with_city = list(
    filter(lambda person: person.__contains__('city'), i_am_programmer_group_members))
i_am_programmer_group_members_sorted_by_city = sorted(i_am_programmer_group_members_with_city, key=key_func)

i_am_programmer_group_members_groupby_city = [{'city': key,
                                               'count': sum(1 for x in group)}
                                              for key, group in
                                              groupby(i_am_programmer_group_members_sorted_by_city, key_func)]
i_am_programmer_group_members_groupby_city = sorted(i_am_programmer_group_members_groupby_city, key=itemgetter('count'),
                                                    reverse=True)

print('\nВ группе "Я - Программист"')
print(
    f'{i_am_programmer_group_members_groupby_city[0]["count"]} участников из города {i_am_programmer_group_members_groupby_city[0]["city"]}')
print(
    f'{i_am_programmer_group_members_groupby_city[1]["count"]} участников из города {i_am_programmer_group_members_groupby_city[1]["city"]}')
print(
    f'{i_am_programmer_group_members_groupby_city[2]["count"]} участников из города {i_am_programmer_group_members_groupby_city[2]["city"]}')
# endregion

programming_group_members_ids = {'name': 'Программирование / itProger',
                                 'ids': list(map(lambda x: x['id'], programming_group_members))}
i_am_programmer_group_members_ids = {'name': 'Я - Программист',
                                     'ids': list(map(lambda x: x['id'], i_am_programmer_group_members))}

# labeldict = {}
# labeldict["Программирование / itProger"] = "Программирование / itProger"
# labeldict["Я - Программист"] = "Я - Программист"
#
# graph = nx.Graph()
# graph.add_node("Программирование / itProger", size=500)
# graph.add_node("Я - Программист", size=500)
#
# # max_group = programming_group_members_ids if len(programming_group_members_ids['ids']) > len(
#     # i_am_programmer_group_members_ids['ids']) else i_am_programmer_group_members_ids
# # for id in max_group['ids']:
# #     graph.add_edge(id, max_group['name'])
# # color_map = ['purple', 'purple']
# for id in programming_group_members_ids['ids']:
#     # graph.add_node(id)
#     graph.add_edge(id, programming_group_members_ids['name'], color='red')
#     # color_map.append('blue')
#
# for id in i_am_programmer_group_members_ids['ids']:
#     # graph.add_node(id)
#     graph.add_edge(id, i_am_programmer_group_members_ids['name'])
#     # color_map.append('green')
#
# nx.draw(graph,
#         labels=labeldict,
#         with_labels=True,
#         node_size=5,
#         node_color='blue',
#         arrowsize=1,
#         pos=nx.spring_layout(graph,
#                              k=4.5/math.sqrt(graph.order())))
#
G = nx.Graph()

G.add_node("Программирование / itProger", size=500)
G.add_node("Я - Программист", size=500)

total_edges = 0
edges_colors = []

for id in programming_group_members_ids['ids']:
    G.add_edge(id, programming_group_members_ids['name'])
    edges_colors.append('#f05684')


for id in i_am_programmer_group_members_ids['ids']:
    G.add_edge(id, i_am_programmer_group_members_ids['name'])
    edges_colors.append('#af91eb')

options = {
    "node_color": "#e4b4ed",
    "edge_color": edges_colors,
    "node_size": 5,
    "arrowsize": 1,
    "width": 1,
    "edge_cmap": plt.cm.Blues,
    "with_labels": True,
}
labeldict = {}
labeldict["Программирование / itProger"] = "Программирование / itProger"
labeldict["Я - Программист"] = "Я - Программист"

nx.draw(G, pos = nx.spring_layout(G, k=4.5/math.sqrt(G.order())), labels=labeldict, **options)


plt.show()
