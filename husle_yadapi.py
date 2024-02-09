import requests

class YandexDiskAPIClient:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_photo(self, url, file_name):
        headers = {
            'Authorization': f'OAuth {self.access_token}'
        }
        params = {
            'path': file_name,
            'url': url
        }
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers, params=params)
        response.raise_for_status()
        return response.json()


