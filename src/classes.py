from abc import ABC
from typing import Any, Dict, Optional, List

class BaseProduct(ABC):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity


class LogMixin:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name=name, description=description, price=price, quantity=quantity)
        print(f"{self.__class__.__name__}({name}, {description}, {price}, {quantity})")

class Product(LogMixin, BaseProduct):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)
        self.__price = price if price > 0 else 0


    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

    @classmethod
    def new_product(cls, data: Dict[str, Any]) -> "Product":
        required_fields = {
            "name": str,
            "description": str,
            "price": (int, float, str),
            "quantity": (int, str)
        }

        for field, field_type in required_fields.items():
            if field not in data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")

            value = data[field]

            if not isinstance(value, field_type):
                try:
                    data[field] = int(value) if field == "quantity" else float(value)
                except (ValueError, TypeError):
                    raise TypeError(f"Поле '{field}' должно быть числом или строкой, представляющей число")

        if data["quantity"] < 0:
            raise ValueError("Количество товара не может быть отрицательным")
        if data["price"] < 0:
            raise ValueError("Цена товара не может быть отрицательной")

        return cls(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"]
        )

    def __str__(self) -> str:
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только товары и их наследников")
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одного типа")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, efficiency: str, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = int(memory)
        self.color = str(color)

    def __str__(self) -> str:
        base = super().__str__()
        parts = base.split(" шт.")
        return f"{parts[0]} шт., модель: {self.model}, память: {self.memory} ГБ, цвет: {self.color}"


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = str(color)

    def __str__(self) -> str:
        base = super().__str__()
        parts = base.split(" шт.")
        return f"{parts[0]} шт., страна: {self.country}, срок прорастания: {self.germination_period}, цвет: {self.color}"


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
        self.name = name
        self.description = description
        self._products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self._products)

    def middle_price(self) -> float:
        """Возвращает среднюю цену товаров в категории"""
        if not self._products:
            return 0
        try:
            total = sum(product.price for product in self._products)
            return total / len(self._products)
        except ZeroDivisionError:
            return 0

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[str]:
        return [str(product) for product in self._products]

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self._products)
        return f"{self.name}, общее количество товаров: {total_quantity} шт."
