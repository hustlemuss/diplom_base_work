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
        photo_name = f'{photo_likes}.jpg'

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

def main():
    with open('config.json') as f:
        config = json.load(f)

    vk_token = config.get('vk_token')
    vk_user_id = config.get('vk_user_id', '4957073')
    yadisk_token = config.get('yadisk_token')
    yadisk_folder = config.get('yadisk_folder', 'Photos saved')

    vk_client = VKAPIClient(vk_token)
    photos_info = vk_client.get_profile_photos_info(vk_user_id)

    save_photos_to_yadisk(photos_info, yadisk_token, yadisk_folder)


    with open('photos_info.json', 'w') as json_file:
        json.dump(photos_info, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
