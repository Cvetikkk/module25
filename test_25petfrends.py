import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    yield
    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    print('Start test')
    pytest.driver.find_element(By.ID, 'email').send_keys("cccc@mail.ru")
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # неявное ожидания
    pytest.driver.implicitly_wait(10)
    heading_all_pets = pytest.driver.find_element(By.XPATH, "//body/div[1]/div[1]/div[1]")
    print("Неявное ожидание заголовка:", heading_all_pets.text)
    pytest.driver.find_element(By.CSS_SELECTOR, "div#navbarNav > ul > li > a").click()
    explicit_wait = WebDriverWait(pytest.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div#navbarNav > ul > li > a")))
    print("Наше явное ожидание прошло успешно, такой элемен есть ", explicit_wait.text)

    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    print(len(names))
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
    pet = pytest.driver.find_element(By.CSS_SELECTOR, 'div.task3>div:nth-child(1)').text
    print('pets' + str(pet))
    count_pets = pet.split('\n')
    print('count_pets' + str(count_pets))
    count_pets = count_pets[1].replace('Питомцев: ', '')
    print('count_pets' + count_pets)
    count_pets = int(count_pets)
    row_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Ожидаем что можем удалить животных и такой элемент есть
    explicit_wait1 = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[4]')))
    print("Наше явное ожидание прошло успешно, такой элемен есть ", explicit_wait1.text)
    # Ожидаем что есть элемент выйти
    explicit_wait2 = WebDriverWait(pytest.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//body/nav[1]/div[2]/button[1]')))
    print("Наше явное ожидание прошло успешно, такой элемен есть ", explicit_wait2.text)
    # неявное ожидания, что есть кнопка в боди PetFriends
    pytest.driver.implicitly_wait(10)
    petFriends = pytest.driver.find_element(By.XPATH, "//body/nav[1]/a[1]")
    print("Неявное ожидание кнопки PetFriends:", petFriends.text)

    # Ищем количество фотографий всех наших питомцев
    count_img = len(pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img'))
    # Ищем уникальные имена животных
    pets_name = set(map(lambda row: row.find_elements(By.TAG_NAME, 'td')[0].text, row_pets))
    # Ищем не повторяющиеся породы животных
    pets_breed = set(map(lambda row: row.find_elements(By.TAG_NAME, 'td')[1].text, row_pets))
    # Ищем уникальный возвраст животных
    pets_age = set(map(lambda row: row.find_elements(By.TAG_NAME, 'td')[2].text, row_pets))
    print("имена", pets_name)
    print("возвраст", pets_age)
    print("порода", pets_breed)
    assert len(row_pets) == count_pets
    assert count_img > count_img / 2
    assert len(pets_name) == count_pets



