# Импортируем нужные модули
from urllib.request import urlretrieve

import math
import os
import time
import vk

# Авторизация

#login = ''
#password = ''
#vk_id = ''

#session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password)
#vkapi = vk.API(session, v='5.81')

# session = vk.Session(access_token='vk1.a.xLOQtpDgGMYpJ8KdDvhGzVdndY0JpCrB-G6OcPJCxKrpdoxgvWZNJ4Sm4zdFPpd6RjPOecYDMd5q85N5PPX1VxxUbxBbfKvSbnhB0xfuJ1hBt7velqRv1eWQ_zs3_wwKqGbB4zMP_7rtjS3unl0YIq-Zfwt9aqmBP7h1J9nG6WVejc3dPJFhiwP_ILqEXyAxoF1m2M1ca4hGDXN5LWQU1A')
vkapi = vk.API(access_token='vk1.a.xLOQtpDgGMYpJ8KdDvhGzVdndY0JpCrB-G6OcPJCxKrpdoxgvWZNJ4Sm4zdFPpd6RjPOecYDMd5q85N5PPX1VxxUbxBbfKvSbnhB0xfuJ1hBt7velqRv1eWQ_zs3_wwKqGbB4zMP_7rtjS3unl0YIq-Zfwt9aqmBP7h1J9nG6WVejc3dPJFhiwP_ILqEXyAxoF1m2M1ca4hGDXN5LWQU1A', v='5.81')

url = "https://vk.com/album-132_47581240"
# Разбираем ссылку
album_id = url.split('/')[-1].split('_')[1]
owner_id = url.split('/')[-1].split('_')[0].replace('album', '')

album = vkapi.photos.getAlbums(owner_id=owner_id, album_ids=album_id)
photos_count = album["items"][0]["size"]

counter = 0 # текущий счетчик
prog = 0 # процент загруженных
breaked = 0 # не загружено из-за ошибки
time_now = time.time() # время старта

#&nbsp;Создадим каталоги
if not os.path.exists('saved'):
    os.mkdir('saved')
photo_folder = 'saved/album{0}_{1}'.format(owner_id, album_id)
if not os.path.exists(photo_folder):
    os.mkdir(photo_folder)

for j in range(math.ceil(photos_count / 1000)): # Подсчитаем&nbsp;сколько раз нужно получать список фото, так как число получится не целое - округляем в большую сторону
    photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id, count=1000, offset=j*1000) #&nbsp;Получаем список фото
    for photo in photos["items"]:
        counter += 1
        url = photo["sizes"][0]["url"] # Получаем адрес изображения
        print('Загружаю фото № {} из {}. Прогресс: {} %'.format(counter, photos_count, prog))
        prog = round(100/photos_count*counter,2)
        try:
            urlretrieve(url, photo_folder + "/" + os.path.split(url)[1]) # Загружаем и сохраняем файл
        except Exception:
            print('Произошла ошибка, файл пропущен.')
            breaked += 1
            continue

time_for_dw = time.time() - time_now
print("\nВ очереди было {} файлов. Из них удачно загружено {} файлов, {} не удалось загрузить. Затрачено времени: {} сек.". format(photos_count, photos_count-breaked, breaked, round(time_for_dw,1)))



# 'https://oauth.vk.com/authorize?client_id=51508716&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,wall,photos,docs,groups&response_type=token&v=5.21'







