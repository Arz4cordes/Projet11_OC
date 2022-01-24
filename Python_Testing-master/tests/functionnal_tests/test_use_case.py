import time


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

"""
Some use cases:
1. A secretary log in,
    look at competitions he can book,
    book for a competition,
    and log out
2. A secretary look at points for each club,
    and log in,
    look at competitions he can book,
    book for a competition,
    look at points for each club,
    and try to book again for the same competition,
    there's an app warning about the limit of 12 places to book
    and finally log out
"""

CD_PATH = "tests/functionnal_tests/chromedriver_app/chromedriver"


def looking_for_dashboard_before_connect(driver):
    dashboard_link = driver.find_element(By.PARTIAL_LINK_TEXT, "dashboard")
    dashboard_link.click()
    assert "Dashboard" in driver.title
    time.sleep(5)
    return True


def registration(driver):
    email_field = driver.find_element(By.NAME, "email")
    email_field.clear()
    email_field.send_keys("john@simplylift.co")
    time.sleep(3)
    email_field.send_keys(Keys.RETURN)
    assert "Summary" in driver.title
    time.sleep(5)
    return True


def choose_competition(driver):
    comp_link = driver.find_element(By.LINK_TEXT, 'Book Places')
    if comp_link:
        comp_link.click()
        assert "Booking" in driver.title
        time.sleep(5)
        return [True, 1]
    else:
        return [True, 2]


def booking_places(driver, number_of_places):
    club_info = driver.find_element(By.ID, 'club_info')
    club_info_content = club_info.text
    club_points = int(club_info_content)
    comp_info = driver.find_element(By.ID, 'comp_info')
    comp_info_content = comp_info.text
    competition_points = int(comp_info_content)
    places_field = driver.find_element(By.NAME, "places")
    places_field.clear()
    places_field.send_keys(number_of_places)
    time.sleep(3)
    form_button = driver.find_element(By.ID, "booking")
    form_button.click()
    time.sleep(5)
    places_to_book = int(number_of_places)
    if competition_points - places_to_book < 0:
        flash_info = driver.find_element(By.ID, 'flashes_msg')
        flash_info_content = flash_info.text
        assert "There's not enough" in flash_info_content
        time.sleep(3)
        main_menu_link = driver.find_element(By.ID, 'competitions_page')
        main_menu_link.click()
        assert 'Summary' in driver.title
        time.sleep(5)
        return True
    elif club_points < places_to_book:
        flash_info = driver.find_element(By.ID, 'flashes_msg')
        flash_info_content = flash_info.text
        assert "You don't own enough" in flash_info_content
        time.sleep(3)
        main_menu_link = driver.find_element(By.ID, 'competitions_page')
        main_menu_link.click()
        assert 'Summary' in driver.title
        time.sleep(5)
        return True
    elif places_to_book > 12:
        flash_info = driver.find_element(By.ID, 'flashes_msg')
        flash_info_content = flash_info.text
        assert "You can't book" in flash_info_content
        main_menu_link = driver.find_element(By.ID, 'competitions_page')
        main_menu_link.click()
        assert 'Summary' in driver.title
        time.sleep(5)
        return True
    else:
        assert "Summary" in driver.title
        time.sleep(5)
        return True


def looking_for_dashboard_after_booking(driver):
    dashboard_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'dashboard')
    dashboard_link.click()
    assert "Dashboard" in driver.title
    time.sleep(5)
    return True


def disconnect_app(driver):
    deconnect_link = driver.find_element(By.LINK_TEXT, 'Logout')
    deconnect_link.click()
    assert "Registration" in driver.title
    time.sleep(5)
    return True


def test_feature_connect_and_book():
    feature_stages = []
    the_service = Service(executable_path=CD_PATH)
    driver = webdriver.Chrome(service=the_service)
    driver.maximize_window()
    driver.get("http://127.0.0.1:5000/")
    assert "Registration" in driver.title
    time.sleep(5)
    feature_stages.append(registration(driver))
    result = choose_competition(driver)
    if result[1] == 1:
        feature_stages.append(result[0])
        feature_stages.append(booking_places(driver, "2"))
        feature_stages.append(disconnect_app(driver))
    else:
        feature_stages.append(result[0])
        feature_stages.append(disconnect_app(driver))
    driver.close()
    time.sleep(3)
    print()
    print("######## ETAPES DU TEST FONCTIONNEL 1 ########")
    print(feature_stages)
    print()


def test_feature_dashboard_and_points_limits():
    feature_stages = []
    the_service = Service(executable_path=CD_PATH)
    driver = webdriver.Chrome(service=the_service)
    driver.maximize_window()
    driver.get("http://127.0.0.1:5000/")
    assert "Registration" in driver.title
    time.sleep(5)
    feature_stages.append(looking_for_dashboard_before_connect(driver))
    driver.get("http://127.0.0.1:5000/")
    assert "Registration" in driver.title
    feature_stages.append(registration(driver))
    result = choose_competition(driver)
    if result[1] == 1:
        feature_stages.append(result[0])
        feature_stages.append(booking_places(driver, "15"))
        result = choose_competition(driver)
        if result[1] == 1:
            feature_stages.append(result[0])
            feature_stages.append(booking_places(driver, "2"))
            feature_stages.append(looking_for_dashboard_after_booking(driver))
        else:
            feature_stages.append(result[0])
            feature_stages.append(looking_for_dashboard_after_booking(driver))
    else:
        feature_stages.append(result[0])
        feature_stages.append(looking_for_dashboard_after_booking(driver))
    assert "Dashboard" in driver.title
    time.sleep(5)
    feature_stages.append(disconnect_app(driver))
    driver.close()
    time.sleep(3)
    print()
    print("######## ETAPES DU TEST FONCTIONNEL 2 ########")
    print(feature_stages)
    print()
