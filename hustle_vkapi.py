import requests

class VKAPIClient:
    BASE_URL = 'https://api.vk.com/method'

    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id

    def build_request_url(self, method):
        return f'{self.BASE_URL}/{method}'

    def prepare_request_params(self):
        return {
            'access_token': self.access_token,
            'v': '5.199'
        }

    def fetch_profile_photos(self):
        method = 'photos.get'
        params = self.prepare_request_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile'})
        response = requests.get(self.build_request_url(method), params=params)
        return response.json()

    def get_photo_likes_count(self, photo_id):
        method = 'likes.getList'
        params = self.prepare_request_params()
        params.update({'type': 'photo', 'owner_id': self.user_id, 'item_id': photo_id})
        response = requests.get(self.build_request_url(method), params=params)
        return response.json().get('response', {}).get('count', 0)
