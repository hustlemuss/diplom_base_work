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
