import requests


url="http://127.0.0.1:8000/api/v1/users/"

params ={
    "username__contains":"k",
    "dob_gte":"1900-01-01"
}
response=requests.get(url,params=params)
print(response.status_code)
print(response.json())

