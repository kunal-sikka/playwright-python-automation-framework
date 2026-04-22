import re

import allure

from pageObjects.base_page import BasePage


class CategoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def verify_categories_visible(self):
        with allure.step("Verify categories sidebar is visible"):
            self.verify_visible(self.page.locator(".left-sidebar"))

    def select_women_category(self):
        with allure.step("Select Women category"):
            self.click_by_role("link", "Women")

    def select_women_subcategory(self, subcategory):
        with allure.step(f"Select Women subcategory '{subcategory}'"):
            self.click_by_role("link", subcategory)

    def verify_category_page(self, main_category, subcategory):
        with allure.step(f"Verify category page for {main_category} > {subcategory}"):
            title = self.page.locator(".title")
            self.verify_text(title, re.compile(main_category, re.IGNORECASE))
            self.verify_text(title, re.compile(subcategory, re.IGNORECASE))

    def select_men_category(self):
        with allure.step("Select Men category"):
            #self.page.pause()
            self.click(self.page.locator("//a[normalize-space()='Men']"))

    def select_men_subcategory(self, subcategory):
        with allure.step(f"Select Men subcategory '{subcategory}'"):
            self.click(self.page.locator(".left-sidebar").get_by_role("link", name=subcategory))
