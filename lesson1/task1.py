import requests
import json

url = "https://api.github.com/users/"
username = input('Enter username: ')

a = requests.get(f"{url}{username}/repos")
data = json.loads(a.content)
with open('task1.json', 'w') as f:
    json.dump(data, f, indent=4)
