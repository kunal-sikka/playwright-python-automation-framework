import os

import allure
import pytest


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome")


@pytest.fixture
def browserInstance(playwright, request):
    browser_name = request.config.getoption("--browser_name") or "chromium"

    # 🔥 Detect CI environment
    is_ci = os.getenv("CI", "false").lower() == "true"

    # Headless in CI, headed locally
    headless = True if is_ci else False

    if browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    else:
        browser = playwright.chromium.launch(
            headless=headless,
            slow_mo=100 if is_ci else 500   # No slow motion in CI (faster)
        )

    context = browser.new_context(
        java_script_enabled=True,
        bypass_csp=True
    )

    # Block ads
    context.route("**/*googlesyndication.com/**", lambda route: route.abort())
    context.route("**/*doubleclick.net/**", lambda route: route.abort())
    context.route("**/*googleads.g.doubleclick.net/**", lambda route: route.abort())

    page = context.new_page()

    yield page

    context.close()
    browser.close()

from pageObjects.home_page import Homepage
from pageObjects.products_Page import ProductsPage
from pageObjects.product_details_page import ProductDetailsPage
from pageObjects.cart_page import CartPage
from pageObjects.checkout_page import CheckoutPage
from pageObjects.brand_page import BrandPage
from pageObjects.category_page import CategoryPage
from pageObjects.register_loginUser import Register_LoginPage
from pageObjects.subscription_test import Subscription
from pageObjects.uiValidations import uiValidations


class Pages:
    def __init__(self, page):
        self.home = Homepage(page)
        self.products = ProductsPage(page)
        self.product_details = ProductDetailsPage(page)
        self.cart = CartPage(page)
        self.checkout = CheckoutPage(page)
        self.brand = BrandPage(page)
        self.category = CategoryPage(page)
        self.auth = Register_LoginPage(page)
        self.subscription = Subscription(page)
        self.ui = uiValidations(page)


@pytest.fixture
def pages(browserInstance):
    return Pages(browserInstance)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("browserInstance", None)

        if page:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )