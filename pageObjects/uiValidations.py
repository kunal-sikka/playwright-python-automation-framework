import allure

from pageObjects.base_page import BasePage
from pageObjects.home_page import Homepage
from utils.test_data_helper import get_random_subject, get_random_message, get_random_file


class uiValidations(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.page.on("dialog", lambda dialog: dialog.accept())

    def contact_us(self, userName, userEmail, subject, message, file_path):
        with allure.step(f"Submit Contact Us form for '{userName}'"):
            self.click_by_text("Contact us")
            self.verify_visible(self.page.locator(":text('GET IN TOUCH')"))

            self.fill(self.page.locator("[name='name']"), userName)
            self.fill(self.page.locator("[name='email']"), userEmail)
            self.fill(self.page.get_by_placeholder("Subject", exact=True), subject)
            self.fill(self.page.get_by_placeholder("Your Message Here"), message)

            self.page.locator("[name='upload_file']").set_input_files(file_path)

            self.click(self.page.locator("[name='submit']"))

    def verify_contact_success(self):
        with allure.step("Verify Contact Us form submitted successfully"):
            success = self.page.locator(".status.alert.alert-success")
            success.wait_for(state="visible", timeout=10000)
            self.verify_text(success, "Success! Your details have been submitted successfully.")

    def go_to_test_cases(self):
        with allure.step("Navigate to Test Cases page"):
            self.click(self.page.locator("button").filter(has_text="Test Cases").last)
            self.verify_url_contains("test_cases")
