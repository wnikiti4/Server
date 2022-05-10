from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager


def get_one_temperature(date, time):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://meteoinfo.ru/archive-pogoda/russia/tomsk-area")
    Select(driver.find_element(by=By.CSS_SELECTOR, value="select#id_dt")).select_by_value(date+time)
    temperature = driver.find_element(by=By.CSS_SELECTOR, value="#div_3 tr:nth-child(3) > td:nth-child(2)").text
    driver.close()
    return temperature
