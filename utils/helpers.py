
from selenium.webdriver.common.by import By


def login_helper(driver, usuario, password):
    
    driver.get("https://www.saucedemo.com")
    
    driver.find_element(By.ID, "user-name").send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()