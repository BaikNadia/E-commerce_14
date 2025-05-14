class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    # Статические переменные для подсчёта
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Увеличиваем счетчики при создании категории
        Category.category_count += 1
        Category.product_count += len(self.products)

    def add_product(self, product: Product):
        self.products.append(product)
        Category.product_count += 1
