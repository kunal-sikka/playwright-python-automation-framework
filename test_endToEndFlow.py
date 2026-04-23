import time
import allure
import pytest
from playwright.sync_api import expect

from utils.data_loader import load_json
from utils.test_data_helper import get_random_subject, get_random_message, get_random_file

users_data = load_json("data/users.json")
payments_data = load_json("data/payment.json")
search_data = load_json("data/search.json")
products_data = load_json("data/products.json")
pq_data = load_json("data/product_qty.json")
multi_data = load_json("data/multi_products.json")
cart_data = load_json("data/cart_actions.json")
category_data = load_json("data/categories.json")
brand_data = load_json("data/brands.json")
search_cart_data = load_json("data/search_cart.json")
review_data = load_json("data/reviews.json")
recommended_data = load_json("data/recommended_products.json")


@allure.feature("Authentication")
@allure.story("Register New User")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("user", users_data["new_users"])
def test_register_user(pages, user):

    import time
    user["email"] = f"{user['userName']}{int(time.time())}@test.com"

    pages.auth.navigate_to_site()
    pages.auth.signUp(user)


@allure.feature("Authentication")
@allure.story("Register with Existing Email")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("user", users_data["new_users"])
def test_register_existing_user(pages, user):

    pages.auth.navigate_to_site()

    import time
    user["email"] = f"{user['userName']}{int(time.time())}@test.com"

    # Step 1: Create user
    pages.auth.signUp(user)

    # Step 2: Logout
    pages.auth.logout()

    # Step 3: Try same email again
    pages.auth.register_with_existing_user(user)


@allure.feature("UI Validations")
@allure.story("Contact Us Form")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("user", users_data["new_users"])
def test_uiValidation(pages, user):

    pages.auth.navigate_to_site()

    import time
    userEmail = f"{user['userName']}{int(time.time())}@test.com"

    subject = get_random_subject()
    message = get_random_message()
    file_path = get_random_file()

    pages.ui.contact_us(
        user["userName"],
        userEmail,
        subject,
        message,
        file_path
    )

    pages.ui.verify_contact_success()

    pages.home.verify_homepage_loaded()

    pages.ui.go_to_test_cases()


@allure.feature("Products")
@allure.story("Search Products")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("keyword", search_data["keywords"])
def test_search_products(pages, keyword):

    pages.auth.navigate_to_site()

    pages.products.search_product(keyword)

    pages.products.verify_search_results(keyword)


@allure.feature("Subscription")
@allure.story("Subscribe from Homepage")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("email", users_data["emails"])
def test_subscription_in_homepage(pages, email):

    pages.auth.navigate_to_site()

    pages.subscription.verify_subscription_flow(email)


@allure.feature("Subscription")
@allure.story("Subscribe from Cart Page")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("email", users_data["emails"])
def test_subscription_in_cart(pages, email):

    pages.auth.navigate_to_site()

    # Navigate to cart
    pages.cart.navigate_to_cart()

    # Verify subscription
    pages.subscription.verify_subscription_flow(email)


@allure.feature("Cart")
@allure.story("Add Products to Cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("indices", [products_data["product_indices"]])
def test_add_products_to_cart(pages, indices):

    pages.auth.navigate_to_site()
    pages.products.open_products()

    expected_total = 0

    for i, index in enumerate(indices):
        price = pages.products.get_product_price_by_index(index)
        expected_total += price

        pages.products.add_product_by_index(index)

        # Click Continue Shopping except last item
        if i < len(indices) - 1:
            pages.products.click_continue_shopping()

    pages.products.click_view_cart()

    # Validations
    pages.cart.verify_products_in_cart_count(len(indices))
    pages.cart.verify_cart_total(expected_total)


@allure.feature("Cart")
@allure.story("Verify Product Quantity in Cart")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("data", pq_data["test_cases"])
def test_verify_product_quantity(pages, data):

    pages.auth.navigate_to_site()

    index = data["index"]
    qty = data["quantity"]

    # Open product
    pages.product_details.open_product_by_index(index)
    pages.product_details.verify_product_page_opened()

    # Capture price
    price = pages.product_details.get_product_price()

    # Set quantity
    pages.product_details.set_quantity(qty)

    # Add to cart
    pages.product_details.add_to_cart()
    pages.product_details.click_view_cart()

    # Validate
    pages.cart.verify_price_with_quantity(price, qty)


@allure.feature("Cart")
@allure.story("Add Multiple Products and Validate Total")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("data", multi_data["test_cases"])
def test_add_multiple_products_and_validate_total(pages, data):

    pages.auth.navigate_to_site()
    pages.products.open_products()

    indices = data["indices"]
    total_expected = 0

    for i, index in enumerate(indices):
        price = pages.products.get_product_price_by_index(index)

        pages.products.add_product_by_index(index)

        total_expected += price

        # Navigation control
        if i < len(indices) - 1:
            pages.products.click_continue_shopping()
        else:
            pages.products.click_view_cart()

    pages.cart.verify_cart_total(total_expected)


@allure.feature("Checkout")
@allure.story("Place Order - Register During Checkout")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("user", users_data["new_users"])
@pytest.mark.parametrize("payment", payments_data["valid_cards"])
def test_place_order_register_during_checkout(pages, user, payment):

    pages.auth.navigate_to_site()

    # Add product
    pages.products.add_product_and_go_to_cart()
    pages.cart.proceed_to_checkout()

    # Register during checkout
    pages.cart.click_register_login()

    import time
    user["email"] = f"{user['userName']}{int(time.time())}@test.com"

    pages.auth.signUp(user)

    # Back to checkout
    pages.cart.navigate_to_cart()
    pages.cart.proceed_to_checkout()

    pages.checkout.verify_checkout_page()
    pages.checkout.enter_comment_and_place_order()

    # Payment
    pages.checkout.enter_payment_details(
        payment["name"],
        payment["card"],
        payment["cvc"],
        payment["month"],
        payment["year"]
    )

    pages.checkout.confirm_order()
    pages.checkout.verify_order_success()

    pages.auth.delete_account()


@allure.feature("Checkout")
@allure.story("Place Order - Register Before Checkout")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("user", users_data["new_users"])
@pytest.mark.parametrize("payment", payments_data["valid_cards"])
def test_place_order_register_before_checkout(pages, user, payment):

    pages.auth.navigate_to_site()

    # Create dynamic email
    import time
    user["email"] = f"{user['userName']}{int(time.time())}@test.com"

    # Register BEFORE checkout
    pages.auth.signUp(user)

    # Add product & checkout
    pages.products.add_product_and_go_to_cart()
    pages.cart.proceed_to_checkout()

    pages.checkout.verify_checkout_page()
    pages.checkout.enter_comment_and_place_order()

    # Payment
    pages.checkout.enter_payment_details(
        payment["name"],
        payment["card"],
        payment["cvc"],
        payment["month"],
        payment["year"]
    )

    pages.checkout.confirm_order()
    pages.checkout.verify_order_success()

    pages.auth.delete_account()


@allure.feature("Checkout")
@allure.story("Place Order - Login Before Checkout")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("user", users_data["valid_users"])
@pytest.mark.parametrize("payment", payments_data["valid_cards"])
def test_place_order_login_before_checkout(pages, user, payment):

    pages.auth.navigate_to_site()

    pages.auth.login_with_correct_credentials(
        user["email"],
        user["password"],
        user["userName"]
    )

    pages.products.add_product_and_go_to_cart()
    pages.cart.proceed_to_checkout()

    pages.checkout.verify_checkout_page()
    pages.checkout.enter_comment_and_place_order()

    pages.checkout.enter_payment_details(
        payment["name"],
        payment["card"],
        payment["cvc"],
        payment["month"],
        payment["year"]
    )
    pages.checkout.confirm_order()
    pages.checkout.verify_order_success()


@allure.feature("Cart")
@allure.story("Remove Product from Cart")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("data", cart_data["remove_test_cases"])
def test_remove_products_from_cart(pages, data):

    pages.auth.navigate_to_site()
    pages.products.open_products()

    indices = data["indices"]

    # Add products
    for i, index in enumerate(indices):
        pages.products.add_product_by_index(index)

        if i < len(indices) - 1:
            pages.products.click_continue_shopping()
        else:
            pages.products.click_view_cart()

    pages.cart.navigate_to_cart()

    # Remove product
    pages.cart.remove_product_by_index(data["remove_index"])

    # Validate
    expected_remaining = len(indices) - 1
    pages.cart.verify_product_removed(expected_remaining)


@allure.feature("Products")
@allure.story("View Category Products")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("data", category_data["test_cases"])
def test_view_category_products(pages, data):

    pages.auth.navigate_to_site()

    # Verify sidebar
    pages.category.verify_categories_visible()

    # Women → Subcategory
    pages.category.select_women_category()
    pages.category.select_women_subcategory(data["women"])

    pages.category.verify_category_page("Women", data["women"])

    # Men → Subcategory
    pages.category.select_men_category()
    pages.category.select_men_subcategory(data["men"])

    pages.category.verify_category_page("MEN", data["men"])


@allure.feature("Products")
@allure.story("View Brand Products")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("data", brand_data["test_cases"])
def test_view_and_cart_brand_products(pages, data):

    pages.auth.navigate_to_site()

    pages.brand.open_products()

    # Verify sidebar
    pages.brand.verify_brands_visible()

    # First brand
    pages.brand.select_brand(data["first_brand"])
    pages.brand.verify_brand_page(data["first_brand"])

    # Second brand
    pages.brand.select_brand(data["second_brand"])
    pages.brand.verify_brand_page(data["second_brand"])


@allure.feature("Cart")
@allure.story("Search and Verify Cart After Login")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("user", users_data["valid_users"])
@pytest.mark.parametrize("keyword", search_data["keywords"])
def test_search_products_and_verify_cart_after_login(pages, user, keyword):

    # Step 1–2: Launch + Navigate
    pages.auth.navigate_to_site()

    # Step 3–4: Open Products
    pages.products.open_products()
    expect(pages.auth.page).to_have_url("https://automationexercise.com/products")

    # Step 5: Search
    pages.products.search_product(keyword)

    # Step 6–7: Verify search results
    pages.products.verify_searched_products_visible()

    # Step 8: Add all to cart
    pages.products.add_all_search_results_to_cart()

    # Step 9: Verify cart before login
    pages.cart.verify_products_in_cart_count(
        pages.cart.page.locator(".cart_description").count()
    )

    # Step 10: Login
    pages.auth.login_with_correct_credentials(
        user["email"],
        user["password"],
        user["userName"]
    )

    # Step 11: Go to cart again
    pages.cart.navigate_to_cart()

    # Step 12: Verify persistence
    pages.cart.verify_products_in_cart_count(
        pages.cart.page.locator(".cart_description").count()
    )


@allure.feature("Products")
@allure.story("Add Review on Product")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("data", review_data["test_cases"])
def test_add_review_on_product(pages, data):

    pages.auth.navigate_to_site()

    # Step 3–5
    pages.product_details.open_products()
    pages.product_details.open_first_product()

    # Step 6
    pages.product_details.verify_review_section_visible()

    # Step 7–8
    pages.product_details.submit_review(
        data["name"],
        data["email"],
        data["review"]
    )

    # Step 9
    pages.product_details.verify_review_success()


@allure.feature("Cart")
@allure.story("Add Recommended Product to Cart")
@allure.severity(allure.severity_level.NORMAL)
def test_add_to_cart_from_recommended_items(pages):

    # Step 1–2
    pages.auth.navigate_to_site()

    # Step 3
    pages.home.scroll_to_recommended_items()

    # Step 4
    pages.home.verify_recommended_items_visible()

    # Step 5
    pages.home.add_first_recommended_product_to_cart()

    # Step 6
    pages.home.click_view_cart()

    # Step 7
    pages.cart.verify_products_in_cart_count(1)


@allure.feature("Checkout")
@allure.story("Verify Address Details at Checkout")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("user", users_data["new_users"])
def test_verify_address_details_in_checkout(pages, user):

    # Step 1–3
    pages.auth.navigate_to_site()

    # Step 4–6 (Signup)
    import time
    user["email"] = f"{user['userName']}{int(time.time())}@test.com"

    pages.auth.signUp(user)

    # Step 7
    # Already validated inside signup method

    # Step 8
    pages.products.add_product_and_go_to_cart()

    # Step 9–10
    pages.cart.navigate_to_cart()

    # Step 11
    pages.cart.proceed_to_checkout()

    # Step 12
    pages.checkout.verify_address_details(user)

    # Step 13
    pages.checkout.verify_billing_address_details(user)

    # Step 14–15
    pages.auth.delete_account()


@allure.feature("Checkout")
@allure.story("Download Invoice After Purchase")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("user", users_data["new_users"])
@pytest.mark.parametrize("payment", payments_data["valid_cards"])
def test_download_invoice_after_purchase(pages, user, payment):

    # Step 1–3
    pages.auth.navigate_to_site()

    # Step 4
    pages.products.add_product_and_go_to_cart()

    # Step 5–6
    pages.cart.navigate_to_cart()

    # Step 7
    pages.cart.proceed_to_checkout()

    # Step 8
    pages.cart.click_register_login()

    # Step 9–10
    import time
    user["email"] = f"{user['userName']}{int(time.time())}@test.com"

    pages.auth.signUp(user)

    # Step 11 already validated in signup

    # Step 12–13
    pages.cart.navigate_to_cart()
    pages.cart.proceed_to_checkout()

    # Step 14
    pages.checkout.verify_checkout_page()

    # Step 15
    pages.checkout.enter_comment_and_place_order()

    # Step 16
    pages.checkout.enter_payment_details(
        payment["name"],
        payment["card"],
        payment["cvc"],
        payment["month"],
        payment["year"]
    )

    # Step 17
    pages.checkout.confirm_order()

    # Step 18
    pages.checkout.verify_order_success()

    # Step 19 (Download + Validate)
    file_path = pages.checkout.download_invoice()

    # Optional extra validation
    assert file_path.endswith(".txt") or file_path.endswith(".pdf")

    # Step 20
    pages.auth.page.get_by_role("link", name="Continue").click()

    # Step 21–22
    pages.auth.delete_account()


@allure.feature("UI Validations")
@allure.story("Scroll Up using Arrow Button")
@allure.severity(allure.severity_level.MINOR)
def test_verify_scroll_up_and_down(pages):

    # Step 1–3
    pages.auth.navigate_to_site()
    pages.home.verify_homepage_loaded()

    # Step 4
    pages.home.scroll_to_bottom()

    # Step 5
    pages.home.verify_subscription_visible()

    # Step 6
    pages.home.click_scroll_up_arrow()

    # Step 7
    pages.home.verify_top_banner_visible()


@allure.feature("UI Validations")
@allure.story("Scroll Up without Arrow Button")
@allure.severity(allure.severity_level.MINOR)
def test_verify_scroll_without_arrow(pages):

    # Step 1–3
    pages.auth.navigate_to_site()
    pages.home.verify_homepage_loaded()

    # Step 4
    pages.home.scroll_to_bottom()

    # Step 5
    pages.home.verify_subscription_visible()

    # Step 6 (NO arrow — direct scroll)
    pages.home.scroll_to_top()

    # Step 7
    pages.home.verify_top_banner_visible()


@allure.feature("Authentication")
@allure.story("Login with Invalid Credentials")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("email,password", [("wrong@test.com", "wrong123"), ("", "password123"), ("test@test.com", ""),])
def test_login_empty_fields(pages, email, password):

    pages.auth.navigate_to_site()

    pages.auth.page.get_by_role("link", name="Signup / Login").click()

    email_input = pages.auth.page.locator("form input").nth(1)
    password_input = pages.auth.page.get_by_placeholder("Password")

    email_input.fill(email)
    password_input.fill(password)

    pages.auth.page.get_by_role("button", name="Login").click()

    # Check browser validation
    if email == "":
        validation = email_input.evaluate("el => el.validationMessage")
        assert "fill" in validation.lower()

    elif password == "":
        validation = password_input.evaluate("el => el.validationMessage")
        assert "fill" in validation.lower()


@allure.feature("Products")
@allure.story("Search with No Results")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.parametrize("keyword", ["zzzz123", "@@@@", "noProductFound"])
def test_search_no_results(pages, keyword):

    pages.auth.navigate_to_site()

    pages.products.search_product(keyword)

    pages.products.verify_no_product_matches(keyword)

@pytest.mark.skip
@allure.feature("Products")
@allure.story("Add Product with Zero Quantity")
@allure.severity(allure.severity_level.MINOR)
def test_add_product_with_zero_quantity(pages):

    pages.auth.navigate_to_site()

    pages.product_details.open_product_by_index(0)

    pages.product_details.set_quantity(0)
    pages.product_details.add_to_cart()
    pages.product_details.click_view_cart()

    # Expect system to default to 1 OR reject
    qty = pages.cart.page.locator(".cart_quantity button").inner_text()

    assert int(qty) >= 1
