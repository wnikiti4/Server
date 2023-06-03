from datetime import datetime, timedelta

from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import UnexpectedAlertPresentException
from time import sleep


def get_temperature():
    start_date = datetime.strptime("13.03.2023", "%d.%m.%Y")
    end_date = datetime.strptime("23.03.2023", "%d.%m.%Y")
    listTime = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    with open("temperature.csv", "w") as f:
        f.write("Date, Time, Temperature\n")
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("no-sandbox")
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        chrome_options.add_argument("--window-size=800,600")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options= chrome_options)
        driver.implicitly_wait(5) # implicitly wait for 5 seconds for each element
        for current_date in daterange(start_date, end_date):
            for time in listTime:
                while True: # loop until the temperature value is parsed successfully
                    try:
                        driver.get("https://meteoinfo.ru/archive-pogoda/russia/tomsk-area")
                        Select(driver.find_element(by=By.CSS_SELECTOR, value="select#id_dt")).select_by_visible_text(
                            current_date.strftime("%Y-%m-%d") + " " + time)
                        temperature = driver.find_element(by=By.CSS_SELECTOR,
                                                          value="#div_3 tr:nth-child(3) > td:nth-child(2)").text
                        f.write(current_date.strftime("%Y-%m-%d") + "," + time + "," + temperature + "\n")
                        break # exit the while loop
                    except UnexpectedAlertPresentException:
                        print("Encountered unexpected alert pop-up, waiting and retrying...")
                        sleep(2)  # Wait for 2 seconds and retry
                    except:
                        print("Error occurred while retrieving data for " + current_date.strftime(
                            "%Y-%m-%d") + " " + time)
                        f.write(current_date.strftime("%Y-%m-%d") + "," + time + "," + "None" + "\n")
                        break # exit the while loop
        driver.quit()

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def get_next_temperature(city):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("no-sandbox")
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    chrome_options.add_argument("--window-size=1000,800")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get("https://meteoinfo.ru")
    driver.find_element(by=By.CSS_SELECTOR, value="#select2-sel_search-container").click()
    driver.find_element(by=By.CSS_SELECTOR, value="body > span > span > span.select2-search.select2-search--dropdown > input").send_keys(""+city)
    driver.find_element(by=By.CSS_SELECTOR, value="body > span > span > span.select2-search.select2-search--dropdown > input").send_keys(Keys.ENTER)
    answer = driver.find_element(by=By.CSS_SELECTOR, value="#div_print_0  tr:nth-child(3)").text
    return answer
