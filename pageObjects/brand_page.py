import re

import allure

from pageObjects.base_page import BasePage


class BrandPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def open_products(self):
        with allure.step("Open Products page"):
            self.click_by_role("link", "Products")

    def verify_brands_visible(self):
        with allure.step("Verify brands sidebar is visible"):
            self.verify_visible(self.page.locator(".brands_products"))

    def select_brand(self, brand_name):
        with allure.step(f"Select brand '{brand_name}'"):
            self.click(self.page.locator(".brands_products").get_by_role("link", name=brand_name))

    def verify_brand_page(self, brand_name):
        with allure.step(f"Verify brand page for '{brand_name}'"):
            title = self.page.locator(".title")
            self.verify_text(title, re.compile(brand_name, re.IGNORECASE))
            products = self.page.locator(".product-image-wrapper")
            assert products.count() > 0
