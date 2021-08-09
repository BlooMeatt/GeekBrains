import requests
import json

url = "https://api.spotify.com/v1/"
headers = {
    'Authorization': 'Bearer {token}'.format(token='BQCm-oJZKWhY6PUBeyIOMNC3LFQCswYQKWj65hc3xPubfTWB9ML1e5AFEXlwNFUlA1ONJAbgQH0QNLzAg6Fz4VlbqHlK3pXq1egpxh1aAubLYLsYdLcq6EIcW0wYH_n22MufyLwmOjnoGeKErw_CBgwJg770lvQCCYIaWC10HMb7h2_EAPym7w')
}
tracks = requests.get(f"{url}me/tracks",headers=headers)
data = json.loads(tracks.content)
with open('task2.json', 'w') as f:
    json.dump(data, f, indent=4)