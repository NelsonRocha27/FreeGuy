import time
from datetime import date

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from game import Game
from updatewebdriver import WebDriver


class WebScrape:
    games_list = []

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        try:
            driver = webdriver.Chrome('chromedriver-win32/chromedriver', chrome_options=options)
        except Exception as error:
            print("An exception occurred:", type(error).__name__, "–", error)
            WebDriver(error, "chromedriver-win32")
            driver = webdriver.Chrome('chromedriver-win32/chromedriver', chrome_options=options)
        driver.get('https://www.allkeyshop.com/blog/daily-deals/')

        delay = 10  # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//iframe")))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        iframe = driver.find_element(by=By.XPATH, value="//iframe")

        driver.switch_to.frame(iframe)

        try:
            myElem = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='splide__slide splide__slide--clone']")))
            myElem = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='splide__slide__container affiliate']")))
            myElem = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, "//img[@class='game-cover']")))
            myElem = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='free-game-type']")))
            print("Frame is ready!")
            time.sleep(5)
        except TimeoutException:
            print("Loading took too much time!")

        # games = driver.find_elements(by=By.XPATH, value="//div[@class='splide__slide splide__slide--clone']")
        games = driver.find_elements(by=By.XPATH, value="//div[@class='splide__slide']")
        games += driver.find_elements(by=By.XPATH, value="//div[@class='splide__slide is-active is-visible']")

        for i in range(len(games)):
            game = Game()
            game.AddPlatform(games[i].get_attribute('data-console'))
            game.AddProvider(games[i].get_attribute('data-drm'))

            href = games[i].find_element(by=By.XPATH, value=".//a[@class='splide__slide__container affiliate']")
            game.AddLink(href.get_attribute('href'))

            game_container = games[i].find_element(by=By.XPATH, value=".//img[@class='game-cover']")
            game.AddImage(game_container.get_attribute('src'))
            game.AddName(game_container.get_attribute('alt'))

            free_game_type = games[i].find_element(by=By.XPATH, value=".//span[@class='free-game-type']")
            game.AddStatus(free_game_type.get_attribute("innerHTML").strip())

            if not game.IsRepeated(self.games_list):
                print(game.name + " - [" + game.platform.upper() + "]")
                if game.IsFreeToKeep(free_with_prime=True) is True:
                    if game.status.lower() == "free with prime":
                        game.AddProvider("prime gaming")
                    if game.IsPCGame() is True:
                        game.AddDate(date.today().strftime("%d/%m/%Y"))
                        self.games_list.append(game)
            else:
                print("Repeated game. Ignoring...")

        pass
