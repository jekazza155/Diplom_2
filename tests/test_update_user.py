import pytest
import requests
import allure

from data.text_response import TextResponse
from helpers.helpers import Person
from data.status_code import StatusCode
from data.urls import URL, Endpoints


class TestChangeUserData:

    @allure.title('Изменение данных пользователя с авторизацией')
    @allure.description('''
                        Тест проверяет возможность изменения данных пользователя с авторизацией:
                        1. Создание нового пользователя;
                        2. Изменение данных пользователя с использованием токена авторизации;
                        3. Проверка успешного ответа;
                        4. Удаление пользователя после завершения теста.
                        ''')
    @pytest.mark.parametrize('data', [
        Person.create_data_correct_user()["name"],
        Person.create_data_correct_user()["password"],
        Person.create_data_correct_user()["email"]
    ])
    def test_change_person_data(self, create_new_user, data):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.patch(URL.main_url + Endpoints.DATA_CHANGE, headers=headers, data=data)
        assert response.status_code == StatusCode.OK and response.json().get("success") == True

    @allure.title('Изменение данных пользователя без авторизации')
    @allure.description('''
                        Тест проверяет невозможность изменения данных пользователя без авторизации:
                        1. Попытка изменения данных пользователя без передачи токена авторизации;
                        2. Проверка ответа на соответствие статусу "Неавторизован".
                        ''')
    @pytest.mark.parametrize('data', [
        Person.create_data_correct_user()["name"],
        Person.create_data_correct_user()["password"],
        Person.create_data_correct_user()["email"]
    ])
    def test_change_person_data_without_auth(self, data):
        response = requests.patch(URL.main_url + Endpoints.DATA_CHANGE, data=data)
        assert response.status_code == StatusCode.UNAUTHORIZED and (
            response.json().get("message") == TextResponse.UNAUTHORIZED
        )