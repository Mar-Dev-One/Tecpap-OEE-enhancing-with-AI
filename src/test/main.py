import requests

url = "http://127.0.0.1:8000/users/"  # make sure trailing slash matches FastAPI route

payload = {
    "email": "mar.aalahyane@test.com",
    "username": "MarfooKinooo",
    "password": "Marouane.al55"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status code:", response.status_code)
