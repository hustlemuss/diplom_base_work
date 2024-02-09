import requests

class YandexDiskAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://cloud-api.yandex.net/v1/disk'

    def upload_file(self, file_path, destination_path):
        url = f'{self.base_url}/resources/upload'
        headers = {'Authorization': f'OAuth {self.token}'}
        params = {'path': destination_path}
        with open(file_path, 'rb') as f:
            response = requests.get(url, headers=headers, params=params)
            upload_url = response.json()['href']
            upload_response = requests.put(upload_url, data=f)
            if upload_response.status_code == 201:
                print(f"Файл {file_path} успешно загружен на Яндекс.Диск в папку {destination_path}")
            else:
                print(f"Ошибка при загрузке файла {file_path} на Яндекс.Диск")

    def create_folder(self, folder_path):
        url = f'{self.base_url}/resources'
        headers = {'Authorization': f'OAuth {self.token}'}
        params = {'path': folder_path}
        response = requests.put(url, headers=headers, params=params)
        if response.status_code == 201:
            print(f"Папка {folder_path} успешно создана на Яндекс.Диск")
        elif response.status_code == 409:
            print(f"Папка {folder_path} уже существует на Яндекс.Диск")
        else:
            print(f"Ошибка при создании папки {folder_path} на Яндекс.Диск")


