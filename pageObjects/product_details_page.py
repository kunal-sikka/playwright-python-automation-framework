import allure

from pageObjects.base_page import BasePage


class ProductDetailsPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def open_product_by_index(self, index):
        with allure.step(f"Open product at index {index}"):
            products = self.page.locator(".choose a")
            assert products.count() > index, "Index out of range"
            self.click(products.nth(index))

    def open_product_by_id(self, product_id):
        with allure.step(f"Open product ID {product_id}"):
            self.click(self.page.locator(f"a[href='/product_details/{product_id}']"))

    def verify_product_page_opened(self):
        with allure.step("Verify product detail page is open"):
            self.verify_visible(self.page.locator(".product-information"))

    def set_quantity(self, qty):
        with allure.step(f"Set product quantity to {qty}"):
            self.fill(self.page.locator("#quantity"), str(qty))

    def add_to_cart(self):
        with allure.step("Add product to cart"):
            self.click(self.page.locator("button:has-text('Add to cart')"))

    def click_view_cart(self):
        self.click_by_role("link", "View Cart")

    def get_product_price(self):
        price_text = self.page.locator(".product-information span span").inner_text()
        return int(price_text.replace("Rs. ", ""))

    def open_products(self):
        with allure.step("Open Products page"):
            self.click_by_role("link", "Products")

    def open_first_product(self):
        with allure.step("Open first product"):
            self.click(self.page.locator(".choose a").first)

    def verify_review_section_visible(self):
        with allure.step("Verify review section is visible"):
            self.verify_visible(self.page.get_by_text("Write Your Review"))

    def submit_review(self, name, email, review):
        with allure.step(f"Submit review by '{name}'"):
            self.fill(self.page.locator("#name"), name)
            self.fill(self.page.locator("#email"), email)
            self.fill(self.page.locator("#review"), review)
            self.click(self.page.locator("#button-review"))

    def verify_review_success(self):
        with allure.step("Verify review submitted successfully"):
            self.verify_text(self.page.locator("#review-section"), "Thank you for your review.")
