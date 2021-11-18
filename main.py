from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from time import sleep

SLEEP_SECONDS = 2
MAX_WAIT_TIME = 60
PIAZZA = "https://piazza.com/class/krs4qzmknom42m"

driver = webdriver.Chrome()
driver.get(PIAZZA)
try:
	input("Login, expand all weeks and press Enter to continue...")
	WebDriverWait(driver, MAX_WAIT_TIME).until(ec.presence_of_element_located((By.ID, "question_feed_questions")))
	posts = driver.find_elements(By.CSS_SELECTOR, "li[data-pats='post_group_item']")
	count = len(posts)
	for i in range(count):
		WebDriverWait(driver, MAX_WAIT_TIME).until(ec.presence_of_element_located((By.ID, "question_feed_questions")))
		posts = driver.find_elements(By.CSS_SELECTOR, "li[data-pats='post_group_item']")
		posts[i].click()
		sleep(SLEEP_SECONDS)
finally:
	driver.close()
print("Done!")
