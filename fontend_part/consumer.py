import requests


url="http://127.0.0.1:8000/api/v1/users/?username__contains=k&dob_gte=2000-01-01"

params ={
    "username__contains":"k",
    "dob_gte":"1900-01-01"
}
response=requests.get(url)
print(response.status_code)
print(response.json())

