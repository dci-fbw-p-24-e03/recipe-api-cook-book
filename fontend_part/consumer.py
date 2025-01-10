import requests


url="http://127.0.0.1:8000/api/v1/users/"


response=requests.get(url)
print(response.status_code)
print(response.json())

post_data={
    "username": "jawidtheamazingchef123",
    "first_name": "jawid",
    "last_name": "jawid",
    "email": "jawid1@api.com",
    "sex": "M",
    "birthdate": "1997-06-12",
    "bio": "I am better than chef before me"
}

requests.post(url,data=post_data)