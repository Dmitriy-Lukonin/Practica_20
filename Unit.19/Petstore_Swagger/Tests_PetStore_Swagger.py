from unittest import TestCase
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json


class TestClass(TestCase):
    def test(self):
        self.assertTrue(True)


# Задание 19.3.3
# Попробуйте использовать свободное API для написания запросов GET, POST, DELETE, PUT.
# Ваша задача — выполнить все запросы и напечатать при помощи команды print ответы запросов
# https://petstore.swagger.io/


URL = "https://petstore.swagger.io/v2/"

'''Данные питомца NEW'''

pet_id = 9223372036854583768
pet_name = 'Gav'
pet_status = 'available'

'''Данные питомца Update'''

pet_new_name = 'Barsik'
pet_new_status = 'sold'

'''Данные питомца Update через форму магазина'''

pet_form_new_name = 'Bobik'
pet_form_new_status = 'pending'

'''Данные нового пользователя'''

username = 'Bandit'
firstName = 'Woldemar'
lastName = 'Godfather'
email = 'krmlin@yo.yo'
password = '123123'
phone = '+7902000003'

'''Данные пользователя Update'''

username_update = 'Mr. Evil'
firstName_update = 'Woldemar'
lastName_update = 'Godfather'
email_update = 'krmlin@yo.yo'
password_update = '123123'
phone_update = '+7902000003'


'''POST/pet/{petId}/uploadImage Uploads an image (загружает изображение)'''
'''FAIL'''
def test_add_photo():

        data = MultipartEncoder(
            fields={
                'photo': (photo, open(photo, 'rb'), 'image/jpeg')
            })

        headers = {'accept': 'application/json', 'Content-Type': data.content_type}

    res = requests.post(f"{URL}{pet_id}/uploadImage", headers=headers, data=data)
    print(res.status_code)
    print(res.text)

    response = requests.post(f"{URL}{pet_id}/uploadImage", headers=headers, data=data)
    print(response.status_code)
    print(response.text)



'''POST/pet Add a new pet to the store (добавление нового питомца в магазин)'''
'''PASSED'''


def test_pet_add():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "id": pet_id,
        "category": {
            "id": 0,
            "name": "dog"
        },
        "name": pet_name,
        "photoUrls": [
            "none"
        ],
        "tags": [
            {
                "id": 0,
                "name": "Gav-Gav"
            }
        ],
        "status": pet_status
    }

    response_post_add = requests.post(f"{URL}pet", headers=headers, data=json.dumps(data))
    res_json = json.loads(response_post_add.text)
    assert data == res_json

    print(" ")
    print('#1', response_post_add.status_code, response_post_add.text)

    response_get = requests.get(f'{URL}pet/{data["id"]}')

    print('# 2', response_get.status_code, response_get.text)

    assert response_get.status_code == 200
    assert json.loads(response_get.text) == data


'''PUT/pet Update an existing pet (обновление существующего животного)'''
'''PASSED'''


def test_pet_update():
    """Обновляет существующего питомца. Или добавляет нового - это баг или фича?"""
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "id": pet_id,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": pet_new_name,
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": pet_new_status
    }

    response = requests.put(f"{URL}pet", headers=headers, data=json.dumps(data))

    response.json = json.loads(response.text)

    print()
    print(response.status_code, response.text)

    assert response.status_code == 200


'''GET /pet/findByStatus Finds pets by status (находит домашних животных по статусу)'''
'''PASSED'''


def test_pet_status_available():
    """PASSED"""
    status = "available"
    res = requests.get(f"{URL}pet/findByStatus?status={status}",
                       headers={'accept': 'application/json'})
    print(" ")
    print(res.status_code, res.text)
    print(list(json.loads(res.text)))

    assert res.status_code == 200


def test_pet_status_pending():
    """PASSED"""
    status = 'pending'
    res = requests.get(f"{URL}pet/findByStatus?status={status}",
                       headers={'accept': 'application/json'})
    print("#1", res.status_code)
    print("#2", res.text)

    assert res.status_code == 200


def test_pet_status_sold():
    """PASSED"""
    status = 'sold'
    res = requests.get(f"{URL}pet/findByStatus?status={status}",
                       headers={'accept': 'application/json'})
    print(" ")
    print(res.status_code, res.text)

    assert res.status_code == 200


'''GET/pet/{petId} Find pet by ID (найти питомца по ID)'''
'''PASSED'''


def test_pet_find_id():
    response_get = requests.get(f'{URL}pet/{pet_id}')
    print()
    print(response_get.status_code, response_get.text)

    assert response_get.status_code == 200


'''POST/pet/{petId} Updates a pet in the store form data (Обновление питомца в магазине данными формы)'''
'''PASSED'''


def test_pet_update_form():
    data = {
        'integer': f'{pet_id}',
        'name': f'{pet_new_name}',
        'status': f'{pet_form_new_status}'
    }

    response = requests.post(f"{URL}pet/{pet_id}", data=data)
    print()
    print(response.text)

    assert response.status_code == 200


'''POST/pet/{petId} Updates a not pet in the store form data 
(Обновление несуществующего питомца в магазине данными формы'''
'''Code 404 Error: response status is 404'''
'''PASSED'''


def test_pet_update_form_404():
    pet_id = 1111111111111111111111111111111111111111111111
    name = 'Bobi'
    status = 'available'

    data = {
        'integer': f'{pet_id}',
        'name': f'{name}',
        'status': f'{status}'
    }

    response = requests.post(f"https://petstore.swagger.io/v2/pet/{pet_id}",
                             data=json.dumps(data))

    print(f'\n', response.text)

    assert response.status_code == 404


'''DELETE/pet/{petId} Delete a pet (Удаляет домашнее животное)'''
'''PASSED'''


def test_pet_id_delete():
    apy_key = 'abc123'

    headers = {'accept': 'application/json', 'api_key': f'{apy_key}'}

    response = requests.delete(f"{URL}pet/{pet_id}", headers=headers)

    print()
    print(response, response.text)
    assert response.status_code == 200


def test_pet_id_delete_1():
    """Удаляет без apy_key - это баг"""
    headers = {'accept': 'application/json'}

    response = requests.delete(f"{URL}pet/{pet_id}", headers=headers)

    print()
    print(response, response.text)
    assert response.status_code == 200


'''POST/user/createWithArray Creates list ofusers with given input array
(создает список пользователей с заданным входным массивом'''
'''PASSED'''


def test_user_array():
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    data = [
        {
            "id": 1,
            "username": "AAA",
            "firstName": "Alex",
            "lastName": "string",
            "email": "string",
            "password": "aaa123",
            "phone": "string",
            "userStatus": 0
        }
    ]

    response = requests.post(f'{URL}user/createWithArray', data=json.dumps(data), headers=headers)

    print()
    print(response.text)
    print(response.json())
    assert response.status_code == 200


'''POST/user/createWithList Creates list of users with input array
(создает список пользователей с заданным входным массивом'''
'''PASSED'''


def test_user_list():
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    data = [
        {
            "id": 1,
            "username": "AAA",
            "firstName": "Alex",
            "lastName": "string",
            "email": "string",
            "password": "aaa123",
            "phone": "string",
            "userStatus": 0
        }
    ]

    response = requests.post(f'{URL}user/createWithList', data=json.dumps(data), headers=headers)
    print(response)
    print(response.text)
    print(response.json())
    assert response.status_code == 200


'''GET/user/{username} Get user by user name (получение пользователя по имени пользователя)'''
"""PASSED"""


def test_username():
    response = requests.get(f'{URL}user/{username}')

    print()
    print(response.text)

    assert response.status_code == 200


'''PUT/user/{username} Update user (обновление пользователя)'''
'''PASSED'''


def test_user_update():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "id": 0,
        "username": username_update,
        "firstName": firstName_update,
        "lastName": lastName_update,
        "email": email_update,
        "password": password_update,
        "phone": phone_update,
        "userStatus": 0
    }

    response = requests.put(f"{URL}user/{username}", data=json.dumps(data), headers=headers)

    print()
    print(response.text)

    assert response.status_code == 200


'''DELETE /user/{username} Delete user (удалить пользователя)'''
'''PASSED'''


def test_user_delete():
    response = requests.delete(f"{URL}user/{username}")

    print()
    print(response.text)

    assert response.status_code == 200


'''GET /user/login пользователь входит в систему'''
'''PASSED'''  # - независимо от username и password пользователь входит. Почему?


def test_user_login():
    """Поля принимают любые символы - это баг?"""
    response = requests.get(f'{URL}user/login?username={username}&password={password}')

    print()
    print(response.text)

    assert response.status_code == 200


'''GET/user/logout Выход из текущего сеанса вошедшего в систему пользователя'''
"""PASSED"""


def test_user_logout():
    """Параметры не передаем, а выход происходит?"""
    response = requests.get(f'https://petstore.swagger.io/v2/user/logout')

    print()
    print(response.text)

    assert response.status_code == 200


'''POST/user Create user (создать пользователя)'''
'''PASSED'''


def test_user_new():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "id": 0,
        "username": username,
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password": password,
        "phone": phone,
        "userStatus": 0
    }

    response = requests.post("https://petstore.swagger.io/v2/user", headers=headers, data=json.dumps(data))

    print()
    print(response.text)

    assert response.status_code == 200


