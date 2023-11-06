import unittest
from models.discount import ThreeForTwoDiscount, BulkDiscount, BundleDiscount
from models.product import Product

class TestThreeForTwoDiscount(unittest.TestCase):

    def setUp(self):
        self.apple_tv = Product('atv', 'Apple TV', 109.50)

    def test_three_for_two_discount_applies_correctly(self):
        discount = ThreeForTwoDiscount('atv')
        items = [self.apple_tv] * 3
        self.assertEqual(discount.apply(items), self.apple_tv.price)

    def test_three_for_two_discount_with_multiple_eligible_sets(self):
        discount = ThreeForTwoDiscount('atv')
        items = [self.apple_tv] * 6
        self.assertEqual(discount.apply(items), self.apple_tv.price * 2)

    def test_three_for_two_discount_does_not_apply_with_less_than_required_quantity(self):
        discount = ThreeForTwoDiscount('atv')
        items = [self.apple_tv] * 2
        self.assertEqual(discount.apply(items), 0)

    def test_three_for_two_discount_with_mixed_products(self):
        discount = ThreeForTwoDiscount('atv')
        super_ipad = Product('ipd', 'Super iPad', 549.99)
        items = [self.apple_tv] * 3 + [super_ipad] * 2
        self.assertEqual(discount.apply(items), self.apple_tv.price)


class TestBulkDiscount(unittest.TestCase):

    def setUp(self):
        self.super_ipad = Product('ipd', 'Super iPad', 549.99)

    def test_bulk_discount_applies_correctly(self):
        discount = BulkDiscount('ipd', 4, 499.99)
        items = [self.super_ipad] * 5
        expected_discount = (self.super_ipad.price * 5) - (499.99 * 5)
        self.assertEqual(discount.apply(items), expected_discount)

    def test_bulk_discount_does_not_apply_below_threshold(self):
        discount = BulkDiscount('ipd', 4, 499.99)
        items = [self.super_ipad] * 4
        self.assertEqual(discount.apply(items), 0)

    def test_bulk_discount_with_exact_threshold_quantity(self):
        discount = BulkDiscount('ipd', 4, 499.99)
        items = [self.super_ipad] * 4
        expected_discount = (self.super_ipad.price * 4) - (549.99 * 4)
        self.assertEqual(discount.apply(items), expected_discount)

    def test_bulk_discount_with_additional_products(self):
        discount = BulkDiscount('ipd', 4, 499.99)
        apple_tv = Product('atv', 'Apple TV', 109.50)
        items = [self.super_ipad] * 5 + [apple_tv]
        expected_discount = (self.super_ipad.price * 5) - (499.99 * 5)
        self.assertEqual(discount.apply(items), expected_discount)


class TestBundleDiscount(unittest.TestCase):

    def setUp(self):
        self.macbook_pro = Product('mbp', 'MacBook Pro', 1399.99)
        self.vga_adapter = Product('vga', 'VGA adapter', 30.00)

    def test_bundle_discount_applies_correctly(self):
        discount = BundleDiscount('mbp', 'vga')
        items = [self.macbook_pro, self.vga_adapter]
        self.assertEqual(discount.apply(items), self.vga_adapter.price)

    def test_bundle_discount_with_multiple_eligible_pairs(self):
        discount = BundleDiscount('mbp', 'vga')
        items = [self.macbook_pro] * 2 + [self.vga_adapter] * 2
        self.assertEqual(discount.apply(items), self.vga_adapter.price * 2)

    def test_bundle_discount_does_not_apply_without_required_product(self):
        discount = BundleDiscount('mbp', 'vga')
        items = [self.vga_adapter] * 3
        self.assertEqual(discount.apply(items), 0)

    def test_bundle_discount_excess_free_product(self):
        discount = BundleDiscount('mbp', 'vga')
        items = [self.macbook_pro, self.vga_adapter, self.vga_adapter]
        self.assertEqual(discount.apply(items), self.vga_adapter.price)

    def test_bundle_discount_with_multiple_products_and_excess_free_product(self):
        discount = BundleDiscount('mbp', 'vga')
        apple_tv = Product('atv', 'Apple TV', 109.50)
        items = [self.macbook_pro] * 2 + [self.vga_adapter] * 3 + [apple_tv]
        self.assertEqual(discount.apply(items), self.vga_adapter.price * 2)


if __name__ == '__main__':
    unittest.main()
