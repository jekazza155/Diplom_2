import pytest
import allure
import requests

from data.text_response import TextResponse
from helpers.helpers import Person
from data.status_code import StatusCode
from data.urls import URL, Endpoints


class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    @allure.description('''
                        Тест проверяет успешное создание уникального пользователя:
                        1. Отправка запроса на регистрацию нового пользователя;
                        2. Проверка успешного ответа;
                        3. Удаление пользователя после завершения теста.
                        ''')
    def test_create_user(self):
        payload = Person.create_data_correct_user()
        response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)

        assert response.json().get("success") is True
        assert response.status_code == StatusCode.OK



    @allure.title('Попытка создания дублирующего пользователя')
    @allure.description('''
                        Тест проверяет невозможность создания пользователя с уже существующими данными:
                        1. Создание нового пользователя;
                        2. Попытка повторной регистрации с теми же данными;
                        3. Проверка ответа на соответствие статусу "Запрещено";
                        4. Удаление пользователя после завершения теста.
                        ''')
    def test_create_double_user(self):
        payload = Person.create_data_correct_user()
        first_response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)

        assert first_response.json().get("success") is True
        assert first_response.status_code == StatusCode.OK

        response_double_register = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        assert response_double_register.status_code == StatusCode.FORBIDDEN and (
                response_double_register.json().get("message") == TextResponse.CREATE_DOUBLE_USER
        )

    @allure.title('Попытка создания пользователя с некорректными данными')
    @allure.description('''
                        Тест проверяет невозможность создания пользователя с некорректными данными:
                        1. Отправка запроса на регистрацию с отсутствующими обязательными полями;
                        2. Проверка ответа на соответствие статусу "Запрещено".
                        ''')
    @pytest.mark.parametrize('payload', [
        Person.create_data_incorrect_user_without_email(),
        Person.create_data_incorrect_user_without_name(),
        Person.create_data_incorrect_user_without_password()
    ])
    def test_create_user_incorrect_data(self, payload):
        response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        assert response.status_code == StatusCode.FORBIDDEN and response.json().get("success") is False