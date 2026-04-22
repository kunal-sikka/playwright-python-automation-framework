import os

import allure

from pageObjects.base_page import BasePage


class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def verify_checkout_page(self):
        with allure.step("Verify checkout page loaded"):
            self.verify_visible(self.page.locator(":text('Address Details')"))
            self.verify_visible(self.page.locator(":text('Review Your Order')"))

    def enter_comment_and_place_order(self):
        with allure.step("Enter order comment and place order"):
            self.fill(self.page.locator("textarea[name='message']"), "Test order")
            self.click_by_text("Place Order")

    def enter_payment_details(self, name, card, cvc, month, year):
        with allure.step("Enter payment details"):
            self.fill(self.page.locator("[name='name_on_card']"), name)
            self.fill(self.page.locator("[name='card_number']"), card)
            self.fill(self.page.locator("[name='cvc']"), cvc)
            self.fill(self.page.locator("[name='expiry_month']"), month)
            self.fill(self.page.locator("[name='expiry_year']"), year)

    def confirm_order(self):
        with allure.step("Confirm and submit order"):
            with self.page.expect_navigation(url="**/payment_done/*"):
                self.click(self.page.locator("button[data-qa='pay-button']"))

    def verify_order_success(self):
        with allure.step("Verify order placed successfully"):
            self.verify_text(self.page.locator("body"), "order")

    def verify_address_details(self, user):
        with allure.step("Verify delivery address details"):
            address_block = self.page.locator("#address_delivery")
            address_block.wait_for()
            assert user["firstName"] in address_block.inner_text()
            assert user["lastName"] in address_block.inner_text()
            assert user["address1"] in address_block.inner_text()
            if user["address2"]:
                assert user["address2"] in address_block.inner_text()
            assert user["city"] in address_block.inner_text()
            assert user["state"] in address_block.inner_text()
            assert user["zipcode"] in address_block.inner_text()
            assert user["country"] in address_block.inner_text()
            assert user["mobile"] in address_block.inner_text()

    def verify_billing_address_details(self, user):
        with allure.step("Verify billing address details"):
            address_block = self.page.locator("#address_invoice")
            address_block.wait_for()
            assert user["firstName"] in address_block.inner_text()
            assert user["lastName"] in address_block.inner_text()
            assert user["address1"] in address_block.inner_text()
            if user["address2"]:
                assert user["address2"] in address_block.inner_text()
            assert user["city"] in address_block.inner_text()
            assert user["state"] in address_block.inner_text()
            assert user["zipcode"] in address_block.inner_text()
            assert user["country"] in address_block.inner_text()
            assert user["mobile"] in address_block.inner_text()

    def download_invoice(self, download_path="downloads"):
        with allure.step("Download order invoice"):
            with self.page.expect_download() as download_info:
                self.click_by_role("link", "Download Invoice")

            download = download_info.value
            os.makedirs(download_path, exist_ok=True)
            file_path = os.path.join(download_path, download.suggested_filename)
            download.save_as(file_path)
            assert os.path.exists(file_path), "Invoice not downloaded"

            with open(file_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=download.suggested_filename,
                    attachment_type=allure.attachment_type.TEXT
                )

            print(f"Invoice downloaded at: {file_path}")
            return file_path
