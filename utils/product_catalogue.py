import json
from pathlib import Path

from models.product import Product

PRODUCT_CATALOGUE_PATH = (
    Path(__file__).parent.parent / 'config' / 'products.json'
)


def load_product_catalogue() -> dict:
    """Load the product catalog from the external JSON configuration file.

    Returns:
        dict: A dictionary with SKUs as keys and Product instances as values.
    """
    try:
        with open(PRODUCT_CATALOGUE_PATH, 'r') as config_file:
            product_data = json.load(config_file)

        for sku, details in product_data.items():
            if 'name' not in details or 'price' not in details:
                raise ValueError(f"Product {sku} must contain 'name' and 'price'.")

        return {
            sku: Product(
                sku, info['name'], info['price']
                ) for sku, info in product_data.items()
            }

    except json.JSONDecodeError as json_error:
        print(f"Error: The product catalog file contains invalid JSON. {json_error}")
        raise
    except ValueError as value_error:
        print(f"Error in product configuration: {value_error}")
        raise
