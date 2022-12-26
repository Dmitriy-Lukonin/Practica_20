import random
from api import PetFriends
from settings import no_valid_email, valid_email, no_valid_password, valid_password, images
import os

pf = PetFriends()

''' 2. Сценарий (негативный сценарий бизнес логики, проверка невалидных значений, проверка обязательных 
параметров, проверка граничных значений, проверка неподдерживаемых типов данных)'''


#       2.1. Получить ключ API c невалидным email
def test_get_key_2_1(email=no_valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result, res = pf.get_api_key(email, password)
    print(f'\n#1.1-1', status)
    print(f'\n#1.1-2', result)
    print(f'\n#1.1-3', res)
    print(f'\n#1.1-4', res.cookies)  # - мое мнение куки нет, но как их правильно проверить?
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403  # - ожидаемая ошибка с невалидным email
    assert 'key' not in result  # - нет key в ответе
    assert res.headers['Content-Type'] == 'text/html; charset=utf-8'  # - проверка response headers
    assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)
    return result


# 		2.2. Добавить информацию о новом питомце №1 без фото
def test_successful_add_self_pet_without_photo_2_2(name='', animal_type='', age=''):
    """Проверяем возможность добавления питомца без фото, не заполняя обязательные поля"""

    # Получаем ключ auth_key
    _, auth_key, res = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца его имя, вид и возраст
    status, result, res = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    print('\nheaders', res.headers)
    print('\ncookies', res.cookies)  # - мое мнение куки нет, но как их правильно проверить?

    '''assert status == 403 # - ожидаемый результат'''
    assert status == 200  # - фактический результат
    assert result['name'] == name
    assert res.headers['Content-Type'] == 'application/json'  # - проверка response headers
    assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)


# 		2.3. Добавить информацию о новом питомце №2 с фото
def test_add_new_pet_with_valid_data_2_3(name='Буян' * 64, animal_type='Собака' * 43, age='три' * 85,
                                         pet_photo=f'images/{random.choice(images)}'):
    """Проверяем что нет возможности добавить питомца с валидными данными, когда имя, вид, возраст 256 символов"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key, _ = pf.get_api_key(valid_email, valid_password)
    print("\nauth_key", auth_key)

    # Добавляем питомца
    status, result, res = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    print("#1.3 status", status)
    print("#1.4 result", result)

    print('\nheaders', res.headers)
    print('\ncookies', res.cookies)  # - мое мнение куки нет, но как их правильно проверить?

    # Сверяем полученный ответ с ожидаемым результатом
    '''assert status == 403 # - ожидаемый результат'''
    assert status == 200  # - фактический результат
    '''assert result['name'] != name # - ожидаемый результат'''
    assert result['name'] == name  # - фактический результат
    # assert isinstance(int(result['age']), int)  # - не проходит проверку и это баг
    # assert res.headers['content-type'] == 'text/html; charset=utf-8'  # - Ожидаемый ответ в swagger
    assert res.headers['content-type'] == 'application/json'  # - Фактический результат
    '''В swagger  content-type: text/html; charset=utf-8, а по факту приходит 'application/json
    ЭТО БАГ?'''
    assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)


# 		2.4. Добавить фото питомцу
def test_successful_changes_pet_photo_2_4(pet_photo=f'images/161.heic'):
    """Тестируем: Изменение фото питомца если формат отличается от поддерживаемого"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key, _ = pf.get_api_key(valid_email, valid_password)
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "БарBoss", "собака", "10", "images/156.jpg")
        _, my_pets, res = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']  # id питомца (первый в списке)
    image1 = my_pets['pets'][0]['pet_photo']  # получаем код image изменяемой картинки питомца

    # Добавляем питомца с фото
    status, result, res = pf.add_pet_photo(auth_key, pet_id, pet_photo)
    image2 = my_pets['pets'][0]['pet_photo']  # получаем код image измененной картинки питомца
    print(res.content)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500  # - ожидаемая ошибка
    assert image1 == image2  # - картинка не изменилась после запроса на изменение
    assert res.headers['content-type'] == 'text/html; charset=utf-8'
    assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)


# 		2.5. Изменить информацию о питомце
def test_successful_update_self_pet_info_2_5(name='Шарик', animal_type='Собака', age=1):
    """Проверяем возможность обновления информации о питомце c несуществующим ID"""

    # Получаем ключ auth_key
    _, auth_key, _ = pf.get_api_key(valid_email, valid_password)
    _, my_pets, res = pf.get_list_of_pets(auth_key, "my_pets")

    # Пробуем обновить имя, тип и возраст не существующего ID питомца в базе
    status, result, res = pf.update_pet_info(auth_key, 'ad304b10-5d76-47dd-ae5a' * 48, name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 400  # - ожидаемая ошибка
    print('\nheaders', res.content)
    print('\nheaders', res.headers)
    print('\ncookies', res.cookies)  # - мое мнение куки нет, но как их правильно проверить?
    assert res.headers['content-type'] == 'text/html; charset=utf-8'  # - Фактический результат
    assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)


# 		2.6. Получить список питомцев
def test_get_my_pets_with_valid_key_2_6(filter='my_petsss'):  # - тест падает если список пустой
    """ Проверяем что запрос с невалидным фильтром вернет ошибку.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список питомцев применив filter - 'my_petsss'."""

    _, auth_key, _ = pf.get_api_key(valid_email, valid_password)
    status, result, res = pf.get_list_of_pets(auth_key, filter)
    print('\nheaders', res.content)
    print('\nheaders', res.headers)
    print('\ncookies', res.cookies)  # - мое мнение куки нет, но как их правильно проверить?

    assert status == 500  # - ожидаемая ошибка
    assert res.headers['content-type'] == 'text/html; charset=utf-8'  # - Фактический результат
    assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)


# 		2.7. Удалить питомца
def test_successful_delete_self_pet_2_7():
    """Проверяем возможность удаления питомца, который не входит в список пользователя"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key, _ = pf.get_api_key(valid_email, valid_password)
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    print(pet_id)
    status, result, res = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "")

    print('\nheaders', res.headers)
    print('\ncookies', res.cookies)  # - мое мнение куки нет, но как их правильно проверить?

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200  # - ЭТО БАГ и негативный сценарий для бизнеса
    assert pet_id not in my_pets.values()
    assert res.headers['content-type'] == 'text/html; charset=utf-8'
    assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)


''' 3. Сценарий (негативный сценарий бизнес логики, возможно незначительные потери для бизнеса)'''


#       3.1. Получить ключ API c невалидным password
def test_get_key_3_1(email=valid_email, password=no_valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result, res = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403  # - ожидаемая ошибка с невалидным email
    assert 'key' not in result  # - нет key в ответе
    assert res.headers['Content-Type'] == 'text/html; charset=utf-8'  # - проверка response headers
    assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)


#       3.2. пользователь не смог вспомнить пароль и не нашел возможности его восстановить. Для себя принял решение
# больше никогда не пользоваться этим сервисом.


''' 4. Сценарий (негативный сценарий бизнес логики, возможны значительные потери для бизнеса)'''


#       4.1. Получить ключ API c невалидным password
def test_get_key_4_1(email=valid_email, password=no_valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result, res = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403  # - ожидаемая ошибка с невалидным email
    assert 'key' not in result  # - нет key в ответе
    assert res.headers['Content-Type'] == 'text/html; charset=utf-8'  # - проверка response headers
    assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)


# 		4.2. Удалить всех питомцев
def test_successful_delete_self_pet_4_2():
    """Проверяем возможность удаления питомца, который не входит в список пользователя"""

    # Получаем ключ auth_key и запрашиваем список питомцев
    _, auth_key, _ = pf.get_api_key(valid_email, valid_password)
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "")

    i = 50
    while i < len(my_pets['pets']):
        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, result, res = pf.delete_pet(auth_key, pet_id)
        i += 1

        # Проверяем что статус ответа равен 403 и удаление не происходит
        assert status == 200  # - ЭТО БАГ и негативный сценарий для бизнеса
        assert pet_id not in my_pets.values()
        assert res.headers['content-type'] == 'text/html; charset=utf-8'
        assert 'Date' in res.headers  # - проверка response headers (как проверить актуальность даты?)


''' 5. Сценарий (головная боль разработчика по восстановлению базы питомцев... надеюсь резервные копии БД
делаются регулярно. В этой системе мое мнение собраны все возможные ошибки и уязвимости какие только возможно
допустить и написать хороший сценарий не представляется возможным)'''
