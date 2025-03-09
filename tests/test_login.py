import allure
import requests

from helpers.helpers import Person
from data.status_code import StatusCode
from data.urls import URL, Endpoints


class TestCreateUser:

    @allure.title('Авторизация существующего пользователя')
    @allure.description('''
                        Тест проверяет возможность авторизации под существующим пользователем:
                        1. Создание нового пользователя;
                        2. Авторизация с использованием данных созданного пользователя;
                        3. Проверка успешного ответа;
                        4. Удаление пользователя после завершения теста.
                        ''')
    def test_login_user(self, create_new_user):
        response = create_new_user
        login = requests.post(URL.main_url + Endpoints.LOGIN, data=response[0])
        assert login.status_code == StatusCode.OK and login.json().get("success") == True

    @allure.title('Попытка авторизации несуществующего пользователя')
    @allure.description('''
                        Тест проверяет невозможность авторизации под несуществующим пользователем:
                        1. Попытка авторизации с некорректными данными пользователя;
                        2. Проверка ответа на соответствие статусу "Неавторизован".
                        ''')
    def test_login_under_none_user(self):
        login = requests.post(URL.main_url + Endpoints.LOGIN, data=Person.create_data_incorrect_user_without_name())
        assert login.status_code == StatusCode.UNAUTHORIZED and login.json().get("success") == False