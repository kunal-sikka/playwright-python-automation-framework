import allure

from pageObjects.base_page import BasePage


class Homepage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def verify_homepage_loaded(self):
        with allure.step("Verify homepage is loaded"):
            self.click(self.page.get_by_alt_text("Website for automation practice"))
            self.verify_visible(self.page.locator("#slider:visible"))

    def scroll_to_bottom(self):
        self.scroll_to_element(self.page.locator(".footer-widget"))

    def scroll_to_recommended_items(self):
        with allure.step("Scroll to recommended items section"):
            self.scroll_to_element(self.page.locator(".footer-widget"))

    def verify_recommended_items_visible(self):
        with allure.step("Verify recommended items are visible"):
            self.verify_visible(self.page.get_by_text("recommended items", exact=False))

    def add_first_recommended_product_to_cart(self):
        with allure.step("Add first recommended product to cart"):
            products = self.page.locator(".recommended_items .product-image-wrapper")
            assert products.count() > 0, "No recommended products found"
            product = products.first
            product.hover()
            self.click(product.locator("text=Add to cart"))

    def click_view_cart(self):
        self.click_by_role("link", "View Cart")

    def verify_subscription_visible(self):
        with allure.step("Verify subscription section is visible"):
            self.verify_visible(self.page.get_by_text("Subscription", exact=False))

    def click_scroll_up_arrow(self):
        self.click(self.page.locator("#scrollUp"))

    def verify_top_banner_visible(self):
        with allure.step("Verify top banner is visible after scroll up"):
            self.verify_visible(
                self.page.locator("h2").filter(has_text="Full-Fledged practice website for Automation Engineers").first
            )
