import allure

from pageObjects.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def navigate_to_cart(self):
        with allure.step("Navigate to cart"):
            self.click_by_role("link", "Cart")
            self.verify_url_contains("view_cart")
            self.scroll_to_element(self.page.locator(".footer-widget"))

    def verify_products_in_cart_count(self, expected_count):
        with allure.step(f"Verify cart has at least {expected_count} product(s)"):
            products = self.page.locator(".cart_description")
            actual_count = products.count()
            assert actual_count >= expected_count, \
                f"Expected at least {expected_count}, but found {actual_count}"

    def verify_price_quantity_total(self):
        with allure.step("Verify price × quantity = total for all cart rows"):
            rows = self.page.locator("#cart_info_table tbody tr")
            assert rows.count() > 0
            for i in range(rows.count()):
                price = rows.nth(i).locator(".cart_price").inner_text().replace("Rs. ", "")
                quantity = rows.nth(i).locator(".cart_quantity button").inner_text()
                total = rows.nth(i).locator(".cart_total").inner_text().replace("Rs. ", "")
                expected_total = int(price) * int(quantity)
                assert expected_total == int(total)

    def verify_price_with_quantity(self, expected_price, expected_qty):
        with allure.step(f"Verify price {expected_price} × qty {expected_qty} in cart"):
            price = self.page.locator(".cart_price").first.inner_text().replace("Rs. ", "")
            quantity = self.page.locator(".cart_quantity button").first.inner_text()
            total = self.page.locator(".cart_total").first.inner_text().replace("Rs. ", "")

            price = int(price)
            quantity = int(quantity)
            total = int(total)

            print(f"Price: {price}, Qty: {quantity}, Total: {total}")

            assert quantity == expected_qty
            assert total == price * quantity
            assert total == expected_price * expected_qty

    def verify_cart_total(self, expected_total):
        with allure.step(f"Verify cart grand total is {expected_total}"):
            rows = self.page.locator("#cart_info_table tbody tr")
            total = 0
            for i in range(rows.count()):
                row_total = rows.nth(i).locator(".cart_total").inner_text().replace("Rs. ", "")
                total += int(row_total)
            print(f"Expected Total: {expected_total}, Actual Total: {total}")
            assert total == expected_total

    def proceed_to_checkout(self):
        with allure.step("Proceed to checkout"):
            self.page.locator("a.btn.btn-default.check_out").click()

    def click_register_login(self):
        self.click_by_role("link", "Register / Login")

    def click_signup_login(self):
        self.click_by_role("link", "Signup / Login")

    def remove_product_by_index(self, index):
        with allure.step(f"Remove product at index {index} from cart"):
            rows = self.page.locator("#cart_info_table tbody tr")
            assert rows.count() > index, "Invalid index to remove"
            self.click(rows.nth(index).locator(".cart_quantity_delete"))

    def verify_product_removed(self, expected_count):
        with allure.step(f"Verify cart now has {expected_count} product(s)"):
            rows = self.page.locator("#cart_info_table tbody tr")
            self.wait(1000)
            assert rows.count() == expected_count

    def clear_cart(self):
        with allure.step("Clear all items from cart"):
            self.navigate_to_cart()
            rows = self.page.locator("#cart_info_table tbody tr")
            count = rows.count()
            for i in range(count):
                self.click(self.page.locator(".cart_quantity_delete").first)
                self.wait(500)
