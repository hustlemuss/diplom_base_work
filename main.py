import json
from datetime import datetime
import requests


class VKAPIClient:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_profile_photos_info(self, user_id, quantity=5):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'count': quantity,
            'extended': 1,
            'photo_sizes': 1,
            'access_token': self.access_token,
            'v': '5.199'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()['response']['items']


def save_photos_to_yadisk(photo_info_list, yadisk_token, yadisk_folder):
    files_info = []
    for photo_info in photo_info_list:
        photo_url = max(photo_info['sizes'], key=lambda x: x['width'] * x['height'])['url']
        photo_likes = photo_info['likes']['count']
        photo_date = datetime.fromtimestamp(photo_info['date']).strftime('%Y-%m-%d_%H-%M-%S')
        photo_name = f'{photo_likes}-{photo_date}.jpg'

        headers = {
            'Authorization': f'OAuth {yadisk_token}'
        }
        params = {
            'path': f'{yadisk_folder}/{photo_name}',
            'url': photo_url
        }
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers, params=params)
        response.raise_for_status()

        print(f"Uploaded {photo_name} to Yandex.Disk")

        files_info.append({
            "file_name": photo_name,
            "size": "z"
        })


    with open('photos_info.json', 'w', encoding='utf-8') as json_file:
        json.dump(files_info, json_file, ensure_ascii=False, indent=4)


def main():
    vk_token = input('Введите токен ВКонтакте: ')
    target_profile = input('Введите ID или screen name целевого профиля ВКонтакте: ')
    try:
        quantity = int(input('Введите количество загружаемых фотографий: '))
    except ValueError:
        print('Ошибка: Введите число')
        return


    with open('config.json') as config_file:
        config = json.load(config_file)
    yadisk_token = config['yadisk_token']
    yadisk_folder = config['yadisk_folder']


    vk_user_id = target_profile
    if not target_profile.isdigit():

        params = {
            'screen_name': target_profile,
            'access_token': vk_token,
            'v': '5.199'
        }
        response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params=params)
        response.raise_for_status()
        vk_user_id = response.json()['response']['object_id']

    vk_client = VKAPIClient(vk_token)
    photos_info = vk_client.get_profile_photos_info(vk_user_id, quantity)

    save_photos_to_yadisk(photos_info, yadisk_token, yadisk_folder)


if __name__ == "__main__":
    main()
