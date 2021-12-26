from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import argparse

SLEEP_SECONDS = 1
MAX_WAIT_TIME = 60
EMAIL = "@uwaterloo.ca"
POST = "li[data-pats='post_group_item']"
CLOSED_BUCKET = "div[id^='bucket_'].start_closed"


def wait_for_load(drv):
	WebDriverWait(drv, MAX_WAIT_TIME).until_not(
		ec.presence_of_element_located((By.CLASS_NAME, "activityIndicator")))


def wait_for_id(drv, eid):
	WebDriverWait(drv, MAX_WAIT_TIME).until(
		ec.presence_of_element_located((By.ID, eid)))


def get_posts(drv, even_read=True):
	return drv.find_elements(By.CSS_SELECTOR, POST + ("" if even_read else ".unread"))


parser = argparse.ArgumentParser(description='Autoclicker for Piazza to read all posts')
parser.add_argument('-a', '--click-all', action='store_true',
                    help='Click all posts (not just unread)')
parser.add_argument('-u', '--uid', help='UWaterloo UserID')
parser.add_argument('link', help='URL of Piazza class (https://piazza.com/class/<id>)')
args = parser.parse_args()

driver = webdriver.Chrome()
driver.get(args.link)
try:
	wait_for_id(driver, "login-form")
	ef = driver.find_element(By.ID, "email_field")
	ef.click()
	if args.uid:
		ef.send_keys(args.uid + EMAIL)
		driver.find_element(By.ID, "password_field").click()
	wait_for_id(driver, "question_feed_questions")
	try:
		driver.find_element(By.ID, "loadMoreButton").click()
		wait_for_load(driver)
	except NoSuchElementException:
		pass
	try:
		closed_buckets = driver.find_elements(By.CSS_SELECTOR, CLOSED_BUCKET)
		for bucket in closed_buckets:
			bucket.click()
	except NoSuchElementException:
		pass
	# input("Login, expand all weeks and press Enter to continue...")
	count = len(get_posts(driver, args.click_all))
	print(f"Found {count} posts to click.")
	while True:
		wait_for_id(driver, "question_feed_questions")
		posts = get_posts(driver, args.click_all)
		if len(posts) == 0 or (args.click_all and count == 0):
			break
		posts[(count := count - 1) if args.click_all else 0].click()
		# wait_for_load(driver)
		sleep(SLEEP_SECONDS)
finally:
	driver.close()
print("Done!")
