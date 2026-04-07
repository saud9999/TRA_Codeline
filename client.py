import requests

r = requests.get("http://192.168.100.97:8080/")
print(r.json())