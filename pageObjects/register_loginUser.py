import allure

from pageObjects.base_page import BasePage


class Register_LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def navigate_to_site(self):
        with allure.step("Navigate to automationexercise.com"):
            self.open_url("https://automationexercise.com/")
            self.verify_visible(self.page.locator("#slider:visible"))

    def signUp(self, user):
        with allure.step(f"Register new user '{user['userName']}'"):
            self.click_by_role("link", "Signup / Login")
            self.verify_visible(self.page.get_by_text("New User Signup!"))

            self.fill(self.page.get_by_role("textbox", name="Name"), user["userName"])
            self.fill(self.page.locator("//input[@data-qa='signup-email']"), user["email"])

            self.click_by_role("button", "Signup")
            self.verify_visible(self.page.locator("b:has-text('ENTER ACCOUNT INFORMATION')"))

            self.click(self.page.get_by_role("radio", name="Mr."))
            self.fill(self.page.get_by_role("textbox", name="Password *"), user["password"])

            self.page.locator("#days").select_option(user["day"])
            self.page.locator("#months").select_option(user["month"])
            self.page.locator("#years").select_option(user["year"])

            self.page.get_by_role("checkbox", name="Sign up for our newsletter!").check()
            self.page.get_by_role("checkbox", name="Receive special offers from our partners!").check()

            self.fill(self.page.get_by_label("First name *"), user["firstName"])
            self.fill(self.page.get_by_label("Last name *"), user["lastName"])
            self.fill(self.page.locator("#company"), user["company"])
            self.fill(self.page.locator("#address1"), user["address1"])
            self.fill(self.page.locator("#address2"), user["address2"])
            self.page.locator("#country").select_option(user["country"])
            self.fill(self.page.locator("#state"), user["state"])
            self.fill(self.page.locator("#city"), user["city"])
            self.fill(self.page.locator("#zipcode"), user["zipcode"])
            self.fill(self.page.locator("#mobile_number"), user["mobile"])

            self.click_by_text("Create Account")

            self.verify_visible(self.page.locator("//b[normalize-space()='Account Created!']"))

            self.click_by_text("Continue")

            self.verify_visible(self.page.get_by_text(f"Logged in as {user['userName']}"))

    def login_with_correct_credentials(self, userEmail, userPassword, userName):  # TEST CASE 2 & 4
        with allure.step(f"Login as '{userName}'"):
            self.click_by_role("link", "Signup / Login")
            self.verify_visible(self.page.get_by_text("Login to your account"))
            self.fill(self.page.locator("form").locator("input").nth(1), userEmail)
            self.fill(self.page.get_by_placeholder("Password"), userPassword)
            self.click_by_role("button", "Login")
            self.verify_visible(self.page.get_by_text(f"Logged in as {userName}"))

    def login_with_incorrect_credentials(self):  # TEST CASE 3
        with allure.step("Attempt login with incorrect credentials"):
            self.click_by_role("link", "Signup / Login")
            self.verify_visible(self.page.get_by_text("Login to your account"))
            self.fill(self.page.locator("form").locator("input").nth(1), "wrong@test.com")
            self.fill(self.page.get_by_placeholder("Password"), "wrong123")
            self.click_by_role("button", "Login")
            self.verify_visible(self.page.get_by_text("Your email or password is incorrect!"))

    def register_with_existing_user(self, user):
        with allure.step(f"Attempt to register with existing email '{user['email']}'"):
            self.click_by_role("link", "Signup / Login")
            self.verify_visible(self.page.get_by_text("New User Signup!"))
            self.fill(self.page.get_by_role("textbox", name="Name"), user["userName"])
            self.fill(self.page.locator("//input[@data-qa='signup-email']"), user["email"])
            self.click_by_role("button", "Signup")
            self.verify_visible(self.page.get_by_text("Email Address already exist!"))

    def delete_account(self):
        with allure.step("Delete user account"):
            self.click_by_role("link", "Delete Account")
            self.verify_visible(self.page.get_by_text("Account Deleted!"))
            self.click_by_text("Continue")

    def logout(self):
        with allure.step("Logout from account"):
            self.click_by_role("link", "Logout")
