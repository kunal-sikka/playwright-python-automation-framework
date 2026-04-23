![CI](https://github.com/kunal-sikka/playwright-python-automation-framework/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10-blue)
![Playwright](https://img.shields.io/badge/playwright-automation-green)
![Pytest](https://img.shields.io/badge/tested%20with-pytest-yellow)
![Allure](https://img.shields.io/badge/reporting-allure-orange)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen)

# 🚀 Playwright Python Automation Framework

A scalable end-to-end test automation framework built using **Playwright (Python)**, designed with industry best practices such as **Page Object Model (POM)**, **data-driven testing**, and **CI/CD integration**.

---

## 🔥 Key Highlights

* ✅ Playwright with Python (fast, reliable browser automation)
* ✅ Page Object Model (clean, maintainable structure)
* ✅ Data-driven testing using JSON
* ✅ Reusable BasePage architecture
* ✅ Pytest framework with fixtures
* ✅ Allure reporting (rich test reports)
* ✅ CI/CD integration using GitHub Actions
* ✅ Automatic report deployment via GitHub Pages

---

## 📂 Project Structure

```
├── pageObjects/        # Page Object classes
├── utils/              # Helper utilities & data loaders
├── data/               # Test data (JSON files)
├── test_data/          # Files/images for upload testing
├── tests/              # Test cases
├── .github/workflows/  # CI pipeline
├── conftest.py         # Fixtures & setup
├── requirements.txt    # Dependencies
```

---

## 🧪 Test Coverage

The framework includes end-to-end scenarios such as:

* User authentication (login/signup)
* Product search & filtering
* Add to cart & checkout flow
* UI validations
* Form submissions (Contact Us, Subscription)
* Negative test scenarios
* Cart persistence after login

---

## ⚙️ Setup & Installation

### 1. Clone repository

```
git clone https://github.com/kunal-sikka/playwright-python-automation-framework.git
cd playwright-python-automation-framework
```

### 2. Install dependencies

```
pip install -r requirements.txt
playwright install
```

---

## ▶️ Run Tests

```
pytest --alluredir=allure-results
```

---

## 📊 Generate Allure Report (Local)

```
allure serve allure-results
```

---

## 🌐 Live Test Report

👉 https://kunal-sikka.github.io/playwright-python-automation-framework/

---

## 📌 What This Project Demonstrates

This project showcases a **production-style QA automation framework**, including:

- End-to-end UI automation using Playwright
- Clean architecture using Page Object Model (POM)
- Data-driven testing strategy
- CI/CD pipeline with GitHub Actions
- Live reporting with Allure

---

## ⚡ CI/CD Integration

* GitHub Actions runs tests on every push
* Generates Allure report automatically
* Deploys report to GitHub Pages

---

## 💡 Why This Project Matters

This is not just a demo project.

It demonstrates how automation is actually implemented in real-world teams:

- Writing maintainable and scalable test frameworks
- Handling CI/CD execution differences (local vs pipeline)
- Stabilizing flaky tests with proper waits and retries
- Generating meaningful test reports for stakeholders

---

## 🧠 Key Design Decisions

* **POM + BasePage** → reduces duplication, improves readability
* **Data-driven approach** → reusable & scalable tests
* **Headless CI execution** → stable automation in pipeline
* **Flexible assertions** → avoids flaky tests
* **Retries in CI** → improves reliability

---

## 📌 Future Enhancements

* Parallel test execution
* Docker support
* Cross-browser matrix in CI
* API + UI integration tests

---

## 👨‍💻 Author

**Kunal Sikka**
QA Automation Engineer | Project Manager

* Expertise: QA, Automation, SaaS Testing, Agile
* Experience: 7+ years

---

## ⭐ Final Note

This project demonstrates a **real-world automation framework setup**, focusing on scalability, maintainability, and CI/CD integration — similar to production-grade QA systems.

---

## 🤝 How I Can Help

If you're building or scaling automation for your product, I can help with:

- Setting up Playwright/Pytest frameworks from scratch
- Improving existing flaky test suites
- CI/CD integration and reporting
- End-to-end test strategy for SaaS products

---
