import re

from playwright.sync_api import expect


class BasePage:

    def __init__(self, page):
        self.page = page

    # ---------- Navigation ----------
    def open_url(self, url):
        self.page.goto(url)

    def get_current_url(self):
        return self.page.url

    # ---------- Click ----------
    def click(self, locator):
        locator.click()

    def click_by_text(self, text):
        self.page.get_by_text(text).click()

    def click_by_role(self, role, name):
        self.page.get_by_role(role, name=name).click()

    # ---------- Input ----------
    def fill(self, locator, value):
        locator.fill(value)

    # ---------- Assertions ----------
    def verify_visible(self, locator):
        expect(locator).to_be_visible()

    def verify_text(self, locator, text):
        expect(locator).to_contain_text(text)

    def verify_url_contains(self, text):
        expect(self.page).to_have_url(re.compile(text))

    # ---------- Scroll ----------
    def scroll_to_element(self, locator):
        locator.scroll_into_view_if_needed()

    def scroll_to_top(self):
        self.page.evaluate("window.scrollTo(0, 0)")

    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    # ---------- Utility ----------
    def get_text(self, locator):
        return locator.inner_text()

    def get_count(self, locator):
        return locator.count()

    def wait(self, ms=1000):
        self.page.wait_for_timeout(ms)