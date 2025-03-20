class Ingredients:
    """Класс для хранения данных, необходимых для создания заказов."""

    # Корректные данные ингредиентов
    correct_ingredients_data = {
        "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
    }

    # Некорректные данные ингредиентов (невалидный хэш)
    incorrect_ingredients_data_hash = {
        "ingredients": ["60d3b41abdacsdf6a733c6", "609646e4dcsfdf0276b2870"]
    }

    # Некорректные данные ингредиентов (пустой список)
    incorrect_ingredients_data_without_filling = {
        "ingredients": []
    }