import requests


url = 'http://127.0.0.1:8000/get_form/'

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

payload = [
    "sometest=THISISTEXT&"
    "othertest=22.11.2020&"
    "number=%2B7999999999",
    "user_name=Ivan&"
    "user_mail=mail@test.ru&"
    "user_phone=%2b79999998877&"
    "date_of_birth=02.02.1985&"
    "over_form=somedata",
    "customer_name=Igor&"
    "customer_mail=somemail@ya.ru&"
    "customer_phone=%2b79999998866&"
    "date_of_order=2020-21-03"
]

for el in payload:
    response = requests.post(url, headers=headers, data=el)
    print(response.text)
