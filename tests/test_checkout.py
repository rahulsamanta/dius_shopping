import unittest
from models.checkout import Checkout
from models.discount import ThreeForTwoDiscount, BulkDiscount, BundleDiscount
from utils.product_catalogue import load_product_catalogue

class TestCheckout(unittest.TestCase):

    def setUp(self):
        self.product_catalogue = load_product_catalogue()
        self.pricing_rules = [
            ThreeForTwoDiscount('atv'),
            BulkDiscount('ipd', 4, 499.99),
            BundleDiscount('mbp', 'vga')
        ]
        self.checkout = Checkout(self.pricing_rules)

    def test_scan_valid_product(self):
        self.checkout.scan('atv')
        scanned_item_skus = [item.sku for item in self.checkout.items]
        self.assertIn('atv', scanned_item_skus)

    def test_scan_invalid_product(self):
        with self.assertRaises(ValueError):
            self.checkout.scan('blah')

    def test_total_with_no_discounts(self):
        self.checkout.scan('vga')
        expected_total = self.product_catalogue['vga'].price
        self.assertEqual(self.checkout.total(), expected_total)

    def test_total_with_bulk_discount(self):
        for _ in range(5):
            self.checkout.scan('ipd')
        expected_total = 5 * 499.99
        self.assertEqual(self.checkout.total(), expected_total)

    def test_total_with_three_for_two_discount(self):
        for _ in range(3):
            self.checkout.scan('atv')
        expected_total = 2 * self.product_catalogue['atv'].price
        self.assertEqual(self.checkout.total(), expected_total)

    def test_total_with_bundle_discount(self):
        self.checkout.scan('mbp')
        self.checkout.scan('vga')
        expected_total = self.product_catalogue['mbp'].price
        self.assertEqual(self.checkout.total(), expected_total)

    def test_clear_items(self):
        self.checkout.scan('mbp')
        self.checkout.clear()
        self.assertEqual(len(self.checkout.items), 0)


if __name__ == '__main__':
    unittest.main()
