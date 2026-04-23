import allure
from playwright.sync_api import expect

from pageObjects.base_page import BasePage


class ProductsPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def verify_products_list_visible(self):  # TEST CASE 8
        with allure.step("Verify all products list is visible"):
            self.click_by_role("link", " Products")
            self.verify_url_contains("automationexercise.com/products")
            products = self.page.locator(".product-image-wrapper")
            self.verify_visible(products.first)
            assert products.count() > 0
            self.click(self.page.locator("a[href='/product_details/1']"))
            self.verify_url_contains("product_details/1")
            details = [self.page.locator("div[class='product-information'] h2"),
                       self.page.get_by_text("Category: Women > Tops"),
                       self.page.get_by_text("Rs. 500"),
                       self.page.get_by_text("Availability:", exact=True),
                       self.page.get_by_text("Condition:", exact=True),
                       self.page.get_by_text("Brand:", exact=True)]
            for item in details:
                self.verify_visible(item)

    def search_product(self, keyword):
        with allure.step(f"Search for '{keyword}'"):
            self.open_products()
            self.fill(self.page.get_by_role("textbox", name="Search Product"), keyword)
            self.click(self.page.locator("#submit_search"))
            self.wait(1000)

    def verify_search_results(self, keyword):
        with allure.step(f"Verify search results for '{keyword}'"):
            products = self.page.locator(".productinfo p")
            count = products.count()
            print(f"Total products found for '{keyword}': {count}")
            return

    def open_products(self):
        with allure.step("Open Products page"):
            self.click_by_role("link", " Products")

    def click_continue_shopping(self):
        self.click_by_role("button", "Continue Shopping")

    def click_view_cart(self):
        self.click_by_role("link", "View Cart")

    def add_product_and_go_to_cart(self, index=0):
        with allure.step(f"Add product at index {index} to cart and go to cart"):
            self.open_products()
            self.add_product_by_index(index)
            self.click_view_cart()

    def add_product_by_index(self, index):
        with allure.step(f"Add product at index {index} to cart"):
            product = self.page.locator(".product-image-wrapper").nth(index)
            product.hover()
            self.click(product.locator("text=Add to cart").first)

    def add_product_to_cart_by_id(self, product_id):
        with allure.step(f"Add product ID {product_id} to cart"):
            product = self.page.locator(f".product-image-wrapper:has(a[href='/product_details/{product_id}'])")
            product.hover()
            self.click(product.locator("text=Add to cart"))

    def get_product_price_by_index(self, index):
        product = self.page.locator(".product-image-wrapper").nth(index)
        price_el = product.locator(".productinfo h2")
        self.verify_visible(price_el)
        price_text = price_el.inner_text()
        return int(price_text.replace("Rs. ", ""))

    def get_searched_products(self):
        return self.page.locator(".product-image-wrapper")

    def add_all_search_results_to_cart(self):
        with allure.step("Add all search results to cart"):
            products = self.get_searched_products()
            count = products.count()
            assert count > 0, "No products found to add"
            for i in range(count):
                product = products.nth(i)
                product.hover()
                self.click(product.get_by_text("Add to cart").first)
                if i < count - 1:
                    self.click_continue_shopping()
                else:
                    self.click_view_cart()
            return count

    def verify_no_product_matches(self, keyword):
        with allure.step(f"Verify no products match '{keyword}'"):
            products = self.page.locator(".productinfo p")
            for i in range(products.count()):
                name = products.nth(i).inner_text().lower()
                assert keyword.lower() not in name

    def verify_searched_products_visible(self):
        with allure.step("Verify searched products are visible"):
            products = self.page.locator(".product-image-wrapper")
            expect(products.first).to_be_visible(timeout=5000)
            assert products.count() > 0, "No products visible after search"

    def verify_no_products_found(self):
        with allure.step("Verify no products found message"):
            assert self.page.locator("text=No products found").is_visible()