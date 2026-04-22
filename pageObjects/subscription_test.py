import allure

from pageObjects.base_page import BasePage
from utils.test_data_helper import get_test_emails


class Subscription(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.input_box = self.page.get_by_role("textbox", name="Your email address")
        self.submit_btn = self.page.locator("#subscribe")
        self.success_msg = self.page.get_by_text("You have been successfully subscribed!", exact=True)

    def scroll_to_subscription(self):
        self.scroll_to_element(self.page.locator(".footer-widget"))

    def get_validation_message(self):
        return self.input_box.evaluate("el => el.validationMessage").lower()

    def verify_subscription_flow(self, email):
        with allure.step(f"Verify subscription flow for '{email}'"):
            self.scroll_to_subscription()

            self.fill(self.input_box, "")
            self.fill(self.input_box, email)
            self.click(self.submit_btn)

            validation = self.get_validation_message()

            # Empty email
            if email == "":
                assert "fill in this field" in validation.lower()
                print("Empty email validation shown")
                return

            # Invalid email
            if "@" not in email:
                assert "include an '@'" in validation.lower()
                print(f"Invalid email validation for {email}")
                return

            # Valid email
            self.verify_visible(self.success_msg)
            print(f"Success for email: {email}")
