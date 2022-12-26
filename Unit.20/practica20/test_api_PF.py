import pytest

from conftest import valid_password, valid_email
import json
import random
from faker import Faker
import requests

base_url = "https://petfriends.skillfactory.ru/"


@pytest.fixture()
def get_key():
    header = {"accept": "application/json", "email": f"{valid_email}", "password": f"{valid_password}"}

    res_get = requests.get(url=f"{base_url}/api/key", headers=header)
    # print(f'\n#1', res_get)
    assert res_get.status_code == 200
    # print(f'#2', res_get.text)
    # print(f'#3', type(res_get.json()), res_get.json())
    dict_key = res_get.json()
    auth_key = dict_key['key']
    print(f'#4', type(dict_key['key']), dict_key['key'])
    print(f'#5', type(res_get.content), res_get.content)
    print(f'#6', res_get.headers)
    return auth_key


# @pytest.fixture()
# def get_key():
    # # переменные email и password нужно заменить своими учетными данными
    # response = requests.get(url='https://petfriends.skillfactory.ru/api/key',
    #                         headers={"email": valid_email, "password": valid_password})
    # assert response.status_code == 200, 'Запрос выполнен неуспешно'
    # # assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
    # # return response.request.headers.get('Cookie')


def test_getAllPets(get_key):
    print(get_key)
    response = requests.get(url='https://petfriends.skillfactory.ru/api/pets?filter=my_pets',
                            headers={"accept": "application/json", "auth_key": get_key})
    assert response.status_code == 200, 'Запрос выполнен неуспешно'
    # assert len(response.json().get('pets')) > 0, 'Количество питомцев не соответствует ожиданиям'


def test_add_pet():
    auth_key = "75db22cab16e47ebf79154644000e5b31c8b40f6dcdc1733c298c2b7"
    print(f'\nStart')
    # auth_key = test_auth_key()
    print(f'#7', auth_key)
    fake = Faker()
    input_pet = {
        "age": random.randint(1, 10),
        "animal_type": fake.name(),
        "name": fake.name(),
    }

    header = {"auth_key": f"{auth_key}"}

    print(header)

    res_post = requests.post(url=f"{base_url}api/create_pet_simple", data=json.dumps(input_pet),
                             headers=header)
    assert res_post.status_code == 200


def python_string_slicer(str):
    if len(str) < 50 or "python" in str:
        return str
    else:
        return str[0:50]


@pytest.fixture(scope="function", params=[
    ("Короткая строка", "Короткая строка"),
    ("Длинная строка, не то чтобы прям очень длинная, но достаточно для нашего теста, и в ней нет названия языка"
     , "Длинная строка, не то чтобы прям очень длинная, но"),
    ("Короткая строка со словом python", "Короткая строка со словом python"),
    ("Длинная строка, нам достаточно будет для проверки, и в ней есть слово python"
     , "Длинная строка, нам достаточно будет для проверки, и в ней есть слово python")
])
def param_fun(request):
    return request.param


def test_python_string_slicer(param_fun):
    (input, expected_output) = param_fun
    result = python_string_slicer(input)
    print("Входная строка: {0}\nВыходная строка: {1}\nОжидаемое значение: {2}".format(input, result, expected_output))
    assert result == expected_output


def test_say(say_hello):
    print(say_hello)
    assert say_hello == 404


@pytest.fixture()
def some_data():
    return 42


def test_some_data(some_data):
    assert some_data == 42
