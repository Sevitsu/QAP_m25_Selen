# python -m pytest -v --driver Edge --driver-path D:\edgedriver\microsoftwebdriver.exe test_selenium_petfriends.py
# python -m pytest -v --driver Edge --driver-path E:\webdriver\msedgedriver.exe test_selenium_petfriends.py
# python -m pytest -v --driver Chrome --driver-path E:\webdriver\chromedriver test_selenium_petfriends.py
import collections
import time
import pytest
from settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_petfriends_login(web_browser):
    # Open PetFriends base page:
    web_browser.get("https://petfriends.skillfactory.ru/")
    time.sleep(0)
    web_browser.implicitly_wait(10)
    # Find the field for search text input:
    # WebDriverWait(web_browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Зарегистрироваться")))
    btn_new_user = web_browser.find_element_by_xpath("//button[@onclick=\"document.location=\'/new_user';\"]")
    btn_new_user.click()

    # WebDriverWait(web_browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "У меня уже есть аккаунт")))
    btn_exist_acc = web_browser.find_element_by_link_text(u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    field_email = web_browser.find_element_by_id("email")
    field_email.click()
    field_email.clear()
    field_email.send_keys(valid_email)

    field_pass = web_browser.find_element_by_id("pass")
    field_pass.click()
    field_pass.clear()
    field_pass.send_keys(valid_password)

    btn_submit = web_browser.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

    # Make the screenshot of browser window:
    assert web_browser.current_url == 'https://petfriends.skillfactory.ru/all_pets', "login error"


def test_show_my_pets(testing):
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    # Enter email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)

    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
    # Enter password
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)

    # Submit button
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "nav-link")))
    pytest.driver.find_element_by_css_selector('a[href="/my_pets"]').click()
    # Checking main user page
    assert pytest.driver.find_element_by_tag_name('a').text == "PetFriends"

    table_rows_qty = pytest.driver.find_elements_by_tag_name('tbody > tr')
    my_pets_qty = pytest.driver.find_element_by_css_selector('div[class=".col-sm-4 left"]').text
    my_pets_qty = my_pets_qty.split('\n')
    my_pets_qty = (':'.join(my_pets_qty))
    my_pets_qty = my_pets_qty.split(':')
    pos = my_pets_qty.index('Питомцев')
    pos = int(str(pos)) + 1
    my_pets_qty = int(my_pets_qty.pop(pos))
    assert len(table_rows_qty) == my_pets_qty, 'Some pets are missed on the Page'


def test_check_images_my_pets(test_login):
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))
    images = pytest.driver.find_elements_by_tag_name('tbody > tr > th > img')
    image_qty = 0
    for i in range(len(images)):
        assert images[i].get_attribute('src') != '', 'No image'
        image_qty = image_qty + 1

    my_pets_qty = pytest.driver.find_element_by_css_selector('div[class=".col-sm-4 left"]').text
    my_pets_qty = my_pets_qty.split('\n')
    my_pets_qty = (':'.join(my_pets_qty))
    my_pets_qty = my_pets_qty.split(':')
    pos = my_pets_qty.index('Питомцев')
    pos = int(str(pos)) + 1
    my_pets_qty = int(my_pets_qty.pop(pos))
    assert image_qty >= int(my_pets_qty/2), 'Some images are missed on the Page'


def test_check_name_breed_age_my_pets(test_login):
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))
    table_rows_qty = pytest.driver.find_elements_by_tag_name('tbody > tr')
    name_breed_age = pytest.driver.find_elements_by_xpath('//tbody/tr[1]/td')
    for i in range(len(table_rows_qty)):
        for j in range(len(name_breed_age)):
            name_breed_age = str(pytest.driver.find_elements_by_tag_name('tbody > tr[i] > td[j]'))
            assert name_breed_age != '', 'Empty cell'


def test_check_equal_names_my_pets(test_login):
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))
    names_count = pytest.driver.find_elements_by_xpath('//tr/td[1]')
    names_count_text = []
    for i in range(len(names_count)):
        names_count_text.append(list(names_count)[i].text)
    names_count_unique = collections.Counter(names_count_text)  # Creates dictionary with equal names count
    assert len(names_count_text) == len(names_count_unique), 'Some pet names are not unique'


def test_check_duplicated_pets_my_pets(test_login):
    pytest.driver.implicitly_wait(10)
    names_count = pytest.driver.find_elements_by_xpath('//tr/td[1]')
    breeds_count = pytest.driver.find_elements_by_xpath('//tr/td[2]')
    ages_count = pytest.driver.find_elements_by_xpath('//tr/td[3]')
    names_count_text = []
    breeds_count_text = []
    ages_count_text = []
    n = 1
    for i in range(len(names_count)):
        names_count_text.append(list(names_count)[i].text)
        breeds_count_text.append(list(breeds_count)[i].text)
        ages_count_text.append(list(ages_count)[i].text)
    for i in range(len(names_count)-1):
        for j in range(i+1, len(names_count)):
            if names_count_text[i] == names_count_text[j] and breeds_count_text[i] == breeds_count_text[j] \
                    and ages_count_text[i] == ages_count_text[j]:
                n += 1
                break

    assert n == 1, f'Duplicated pets qty {n}'
