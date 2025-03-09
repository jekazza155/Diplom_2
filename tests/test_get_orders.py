import requests
import allure

from data.ingredients import Ingredients
from data.status_code import StatusCode
from data.text_response import TextResponse
from data.urls import URL, Endpoints


class TestCreateOrder:

    @allure.title('Создание и получение заказа авторизованным пользователем')
    @allure.description('''
                        Тест проверяет возможность создания и получения заказа авторизованным пользователем:
                        1. Создание нового пользователя;
                        2. Создание заказа с использованием авторизации;
                        3. Получение данных о заказе пользователя;
                        4. Проверка корректности данных заказа;
                        5. Удаление пользователя после завершения теста.
                        ''')
    def test_get_order_with_auth(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response_create_order = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers, data=Ingredients.correct_ingredients_data)
        response_get_order = requests.get(URL.main_url + Endpoints.GET_ORDERS, headers=headers)
        assert response_get_order.status_code == StatusCode.OK and (
            response_create_order.json()["order"]["number"] == response_get_order.json()["orders"][0]["number"]
        )

    @allure.title('Попытка получения заказа неавторизованным пользователем')
    @allure.description('''
                        Тест проверяет невозможность получения заказа без авторизации:
                        1. Попытка получения данных о заказе без передачи токена авторизации;
                        2. Проверка ответа на соответствие статусу "Неавторизован".
                        ''')
    def test_get_order_without_auth(self):
        response_get_order = requests.get(URL.main_url + Endpoints.GET_ORDERS)
        assert response_get_order.status_code == StatusCode.UNAUTHORIZED and (
            TextResponse.UNAUTHORIZED in response_get_order.text
        )