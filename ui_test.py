import os
from configparser import ConfigParser
from pathlib import Path

from playwright.sync_api import Playwright, expect

## Grab data from ini file
base_dir = Path(__file__).resolve().parents[1]
config_file = os.path.join(base_dir, "config.ini")
config = ConfigParser()
config.read(config_file)
site_url = config['site']['site_url']
viewport_width = int(config["playwright"]["viewport_width"])
viewport_height = int(config["playwright"]["viewport_height"])
slow_mo = int(config["playwright"]["slow_mo"])


def test_verify_progress_bar(playwright: Playwright, headless=None) -> None:

    browser = playwright.chromium.launch(
        slow_mo=None if headless else slow_mo,
        headless=False
    )
    context = browser.new_context(viewport={"width": viewport_width, "height": viewport_height})
    page = context.new_page()
    page.goto(site_url)
    page.get_by_role("link", name="Progress Bar").click()

    heading = page.get_by_role("heading", name="Progress Bar")
    assert heading is not None, "Heading with name 'Progress Bar' not found"
    start_btn = page.locator("button.btn-primary")
    stop_btn = page.locator("button.btn-info")
    progres_bar = page.locator("div.progress-bar")
    start_btn.click()
    while True:
        value = int(progres_bar.get_attribute("aria-valuenow"))
        if value >= 75:
            break
        else:
            print(f"Percentange: {value}%")
    stop_btn.click()
    expect(progres_bar).to_have_attribute("aria-valuenow", "75")
    assert value >= 75
    print("test_verify_progress_bar")

    context.close()
    browser.close()


def test_verify_sample_app(playwright: Playwright, headless=None) -> None:
    browser = playwright.chromium.launch(
        slow_mo=None if headless else slow_mo,
        headless=False
    )
    context = browser.new_context(viewport={"width": viewport_width, "height": viewport_height})
    page = context.new_page()
    page.goto(site_url)
    page.get_by_role("link", name="Sample App").click()

    heading = page.get_by_role("heading", name="Sample App")
    assert heading is not None, "Heading with name 'Sample App' not found"
    page.get_by_placeholder("User Name").click()
    page.get_by_placeholder("User Name").fill("t")
    page.get_by_placeholder("********").click()
    page.get_by_placeholder("********").fill("pwd")
    page.get_by_role("button", name="Log In").click()
    Login = page.get_by_text("Welcome, t!")
    assert Login is not None, "Heading with name 'Login' not found"
    page.get_by_role("button", name="Log Out").click()
    Logout = page.get_by_text("User logged out.")
    assert Logout is not None, "Heading with name 'Logout' not found"
    print("test_verify_sample_app")

    context.close()
    browser.close()


def test_verify_Load_delay(playwright: Playwright, headless=None) -> None:
    browser = playwright.chromium.launch(
        slow_mo=None if headless else slow_mo,
        headless=False
    )
    context = browser.new_context(viewport={"width": viewport_width, "height": viewport_height})
    page = context.new_page()
    page.goto(site_url)
    page.get_by_role("link", name="Load Delay").click()
    heading = page.get_by_role("heading", name="Load Delays")
    assert heading is not None, "Heading with name 'Load Delays' not found"
    button = page.get_by_role("button", name="Button Appearing After Delay")
    expect(button).to_be_visible()
    button.click()
    assert button
    print("test_verify_Load_delay")

    context.close()
    browser.close()
