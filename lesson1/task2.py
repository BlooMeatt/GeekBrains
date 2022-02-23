import requests
import json
# Импорт данных для авторизации. Положены в отдельный файл, добавленный в .gitignore
import credentials as cd

# Получение токена
auth_url = 'https://accounts.spotify.com/api/token'
client_id = cd.client_id
client_secret = cd.client_secret

auth_response = requests.post(auth_url, {'grant_type':'client_credentials', 'client_id':client_id,'client_secret':client_secret})
auth_data = auth_response.json()
access_token = auth_data['access_token']


url = "https://api.spotify.com/v1/"
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# Les Zeppelin
artist_id = '36QJpDe2go2KgaRleHCDTp'

# Получение списка альбомов
tracks = requests.get(f"{url}artists/{artist_id}/albums",headers=headers)

# Добавление в файл
data = json.loads(tracks.content)
with open('task2.json', 'w') as f:
    json.dump(data, f, indent=4)