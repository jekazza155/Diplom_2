import requests
import allure

from data.ingredients import Ingredients
from data.text_response import TextResponse
from data.urls import URL, Endpoints
from data.status_code import StatusCode


class TestCreateOrder:

    @allure.title('Создание заказа авторизованным пользователем')
    @allure.description('''
                        Тест проверяет возможность создания заказа авторизованным пользователем:
                        1. Создание нового пользователя;
                        2. Отправка запроса на создание заказа с использованием токена авторизации;
                        3. Проверка успешного ответа;
                        4. Удаление пользователя после завершения теста.
                        ''')
    def test_create_order_with_auth(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers, data=Ingredients.correct_ingredients_data)
        assert response.status_code == StatusCode.OK and response.json().get("success") == True

    @allure.title('Создание заказа без авторизации')
    @allure.description('''
                        Тест проверяет возможность создания заказа без авторизации:
                        1. Отправка запроса на создание заказа без передачи токена авторизации;
                        2. Проверка успешного ответа.
                        ''')
    def test_create_order_without_auth(self):
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, data=Ingredients.correct_ingredients_data)
        assert response.status_code == StatusCode.OK and response.json().get("success") == True

    @allure.title('Попытка создания заказа без передачи ингредиентов')
    @allure.description('''
                        Тест проверяет невозможность создания заказа без передачи ингредиентов:
                        1. Создание нового пользователя;
                        2. Отправка запроса на создание заказа без указания ID ингредиентов;
                        3. Проверка ответа на соответствие статусу "Ошибка запроса";
                        4. Удаление пользователя после завершения теста.
                        ''')
    def test_create_order_without_ingredients(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers, data=Ingredients.incorrect_ingredients_data_without_filling)
        assert response.status_code == StatusCode.BAD_REQUEST and response.json().get("success") == False

    @allure.title('Попытка создания заказа с невалидным хэшем ингредиентов')
    @allure.description('''
                        Тест проверяет обработку ошибки при создании заказа с невалидным хэшем ингредиентов:
                        1. Создание нового пользователя;
                        2. Отправка запроса на создание заказа с невалидным хэшем ингредиентов;
                        3. Проверка ответа на соответствие статусу "Ошибка сервера";
                        4. Удаление пользователя после завершения теста.
                        ''')
    def test_create_order_incorrect_hash(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers, data=Ingredients.incorrect_ingredients_data_hash)
        assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR and TextResponse.SERVER_ERROR in response.text