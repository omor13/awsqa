import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Remote

devicefarm_client = boto3.client("devicefarm", region_name="us-west-2")

testgrid_url_response = devicefarm_client.create_test_grid_url(
    projectArn="arn:aws:devicefarm:us-west-2:339712888957:testgrid-project:e046f915-f887-4d5c-ac28-08d7533295f4",
    expiresInSeconds=600
)

options = webdriver.ChromeOptions()

driver = Remote(
    command_executor=testgrid_url_response["url"],
    options=options
)

wait = WebDriverWait(driver, 10)

try:
    driver.get("https://getbootstrap.com/docs/5.0/examples/checkout/")

    wait.until(EC.element_to_be_clickable((By.ID, "firstName"))).send_keys("hello")
    wait.until(EC.element_to_be_clickable((By.ID, "lastName"))).send_keys("hi")
    wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys("myusername")
    wait.until(EC.element_to_be_clickable((By.ID, "email"))).send_keys("someemail@example.com")
    wait.until(EC.element_to_be_clickable((By.ID, "address"))).send_keys("1234 main st")

    Select(wait.until(EC.element_to_be_clickable((By.ID, "country")))).select_by_visible_text("United States")
    Select(wait.until(EC.element_to_be_clickable((By.ID, "state")))).select_by_visible_text("California")

    wait.until(EC.element_to_be_clickable((By.ID, "zip"))).send_keys("345678")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".needs-validation > .form-check:nth-child(3) > .form-check-label"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-check:nth-child(4) > .form-check-label"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-check:nth-child(2) > .form-check-label"))).click()

    wait.until(EC.element_to_be_clickable((By.ID, "cc-name"))).send_keys("fadfadf")
    wait.until(EC.element_to_be_clickable((By.ID, "cc-number"))).send_keys("fadfasd")
    wait.until(EC.element_to_be_clickable((By.ID, "cc-expiration"))).send_keys("05/2024")
    wait.until(EC.element_to_be_clickable((By.ID, "cc-cvv"))).send_keys("123")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".w-100"))).click()

finally:
    driver.quit()
