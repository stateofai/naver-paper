from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

import requests
import uuid
import re
import rsa
import lzstring
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def naver_style_join(elements):
    """Join elements in Naver's specific format."""
    return "".join([chr(len(s)) + s for s in elements])


def encrypt(key_str, user_id, user_password):
    """Encrypt user credentials using RSA encryption."""
    session_key, key_name, e_str, n_str = key_str.split(",")
    e, n = int(e_str, 16), int(n_str, 16)

    message = naver_style_join([session_key, user_id, user_password]).encode()
    pubkey = rsa.PublicKey(e, n)
    encrypted = rsa.encrypt(message, pubkey)

    return key_name, encrypted.hex()


def get_encryption_key():
    """Retrieve the encryption key from Naver."""
    try:
        response = requests.get("https://nid.naver.com/login/ext/keys.nhn")
        response.raise_for_status()
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        raise ConnectionError("Failed to retrieve encryption key.") from e


def encrypt_account(user_id, user_password):
    """Encrypt user account credentials."""
    key_str = get_encryption_key()
    return encrypt(key_str, user_id, user_password)


def session(user_id, user_password):
    """Create and return a Naver session using Selenium."""
    try:
        # Set up Chrome options for Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        # Initialize Chrome driver (make sure the path is correct)
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open Naver login page
        driver.get("https://nid.naver.com/nidlogin.login")

        # Enter username and password
        username = driver.find_element(By.ID, "id")
        password = driver.find_element(By.ID, "pw")

        username.send_keys(user_id)
        password.send_keys(user_password)

        # Click the login button
        login_button = driver.find_element(By.ID, "log.login")
        login_button.click()

        # Wait for page load or for any redirects
        time.sleep(5)

        # Here, you could add additional steps to verify successful login
        # or to navigate to a specific page after login

        # Return the driver object for further use
        return driver

    except Exception as e:
        raise ConnectionError("Failed to create Naver session.") from e
