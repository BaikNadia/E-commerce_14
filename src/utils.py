import json
from typing import List

from src.classes import Category, Product


def load_data_from_json() -> List[Category]:
    """
    Загружает данные из файла data/products.json и создаёт объекты классов Product и Category.
    """
    with open("data/products.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []

    for category_data in data:
        products = []
        for product_data in category_data["products"]:
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=float(product_data["price"]),
                quantity=int(product_data["quantity"]),
            )
            products.append(product)

        category = Category(
            name=category_data["name"],
            description=category_data["description"],
            products=products,
        )
        categories.append(category)

    return categories
