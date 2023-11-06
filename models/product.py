class Product:
    """Represents a product in the computer store.

    Attributes:
        sku (str): The stock-keeping unit identifier for the product.
        name (str): The name of the product.
        price (float): The price of the product.
    """

    def __init__(self, sku: str, name: str, price: float):
        """Initializes a new instance of the Product class.

        Args:
            sku (str): The stock-keeping unit identifier for the product.
            name (str): The name of the product.
            price (float): The price of the product.
        """
        self.sku = sku
        self.name = name
        self.price = price
