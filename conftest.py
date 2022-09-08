import pytest
import uuid
from selenium import webdriver
from settings import valid_email, valid_password


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def web_browser(request, selenium):
    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):
    if request.node.rep_call.failed:
        # Make the screenshot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screenshot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass  # just ignore any errors here
    browser.quit()


@pytest.fixture(autouse=False)
def testing():
    pytest.driver = webdriver.Chrome('E:/webdriver/chromedriver.exe')
    # entering onto authorisation page
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    assert pytest.driver.find_element_by_tag_name('a').text == "PetFriends", 'Login Error'

    yield

    pytest.driver.quit()


@pytest.fixture(autouse=False)
def test_login():
    pytest.driver = webdriver.Chrome('E:/webdriver/chromedriver.exe')
    pytest.driver.implicitly_wait(10)
    # entering into authorisation page
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Enter password
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)
    # Submit button
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.find_element_by_css_selector('a[href="/my_pets"]').click()
    # Checking main user page
    assert pytest.driver.find_element_by_tag_name('a').text == "PetFriends", 'Login Error'

    yield

    pytest.driver.quit()
