from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import argparse

def find_naver_campaign_links(source_urls, visited_urls_file='visited_urls.txt'):
    # Read Source URLs from file
    if source_urls == []:
        return

    # Read visited URLs from file
    try:
        with open(visited_urls_file, 'r') as file:
            visited_urls = set(file.read().splitlines())
    except FileNotFoundError:
        visited_urls = set()

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    naver_links = []
    for base_url in source_urls:
      # Send a request to the base URL
      response = requests.get(base_url, verify=False)
      soup = BeautifulSoup(response.text, 'html.parser')

      if base_url.startswith("https://www.clien.net"):
        # Find all span elements with class 'list_subject' and get 'a' tags
        list_subject_links = soup.find_all('span', class_='list_subject')
        for span in list_subject_links:
          a_tag = span.find('a', href=True)
          if a_tag and '네이버' in a_tag.text:
            if a_tag['href'].startswith(base_url):
              full_link = a_tag['href']
            else:
              full_link = urljoin(base_url, a_tag['href'])
            naver_links.append(full_link)
      elif base_url.startswith("https://damoang.net"):
        # Find all <a> elements 
        list_subject_links = soup.find_all('a')
        for a_tag in list_subject_links:
          if a_tag and '네이버' in a_tag.text and a_tag['href'].startswith(base_url):
            if a_tag['href'].startswith(base_url):
              full_link = a_tag['href']
            else:
              full_link = urljoin(base_url, a_tag['href'])
            naver_links.append(full_link)
 
    print(naver_links)

    # Initialize a list to store campaign links
    campaign_links = []

    # Check each Naver link
    for link in naver_links:
      if link in visited_urls:
        continue  # Skip already visited links

      res = requests.get(link, verify=False)
      inner_soup = BeautifulSoup(res.text, 'html.parser')

      # Find all links that start with the campaign URL
      for a_tag in inner_soup.find_all('a', href=True):
        if a_tag['href'].startswith("https://campaign2-api.naver.com") or a_tag['href'].startswith("https://ofw.adison.co"):
          campaign_links.append(a_tag['href'])

      # Add the visited link to the set
      visited_urls.add(link)

    # Save the updated visited URLs to the file
    with open(visited_urls_file, 'w') as file:
        for url in visited_urls:
            file.write(url + '\n')

    return campaign_links


def run(id, passwd, debug) -> None:
    # The base URL to start with
    source_urls = []
    source_urls.append("https://www.clien.net/service/board/jirum")
    source_urls.append("https://damoang.net/economy")
    campaign_links = find_naver_campaign_links(source_urls, "/data/visited_urls.txt")
    if campaign_links == []:
        print("모든 링크를 방문했습니다.")
        return
    if debug:
        print("campaign_links.count: ", len(campaign_links))

    # 크롬 드라이버 옵션 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-renderer-backgrounding");
    chrome_options.add_argument("--disable-background-timer-throttling");
    chrome_options.add_argument("--disable-backgrounding-occluded-windows");
    chrome_options.add_argument("--disable-client-side-phishing-detection");
    chrome_options.add_argument("--disable-crash-reporter");
    chrome_options.add_argument("--disable-oopr-debug-crash-dump");
    chrome_options.add_argument("--no-crash-upload");
    chrome_options.add_argument("--disable-gpu");
    chrome_options.add_argument("--disable-extensions");
    chrome_options.add_argument("--disable-plugins");
    chrome_options.add_argument("--disable-low-res-tiling");

    # 새로운 창 생성
    if debug:
        print("크롬 실행 중...")
    driver = webdriver.Chrome(options=chrome_options)

    if debug:
        print("네이버 접속 중...")
    driver.get('https://naver.com')

    # 현재 열려 있는 창 가져오기
    current_window_handle = driver.current_window_handle

    # <a href class='MyView-module__link_login___HpHMW'> 일때 해당 링크 클릭
    driver.find_element(By.XPATH, "//a[@class='MyView-module__link_login___HpHMW']").click()

    # 새롭게 생성된 탭의 핸들을 찾습니다
    # 만일 새로운 탭이 없을경우 기존 탭을 사용합니다.
    new_window_handle = None
    for handle in driver.window_handles:
        if handle != current_window_handle:
            new_window_handle = handle
            break
        else:
            new_window_handle = handle

    # 새로운 탭을 driver2로 지정합니다
    driver.switch_to.window(new_window_handle)
    driver2 = driver

    if debug:
        print("네이버 로그인 입력 컨트롤 찾는 중...")

    username = driver2.find_element(By.NAME, 'id')
    pw = driver2.find_element(By.NAME, 'pw')

    # ID input 클릭
    username.click()
    # js를 사용해서 붙여넣기 발동 <- 왜 일부러 이러냐면 pypyautogui랑 pyperclip를 사용해서 복붙 기능을 했는데 운영체제때문에 안되서 이렇게 한거다.
    driver2.execute_script("arguments[0].value = arguments[1]", username, id)
    time.sleep(1)

    pw.click()
    driver2.execute_script("arguments[0].value = arguments[1]", pw, passwd)
    time.sleep(1)

    #입력을 완료하면 로그인 버튼 클릭
    driver2.find_element(By.CLASS_NAME, "btn_login").click()
    time.sleep(1)

    if debug:
        print("네이버 로그인 완료")

    for link in campaign_links:
        print(link) # for debugging
        # Send a request to the base URL
        driver2.get(link)
        if link.startswith("https://campaign2-api.naver.com"):
            try:
                result = driver2.switch_to.alert
                print(result.text)
                result.accept()
            except:
                print("no alert")
                pageSource = driver2.page_source
                print(pageSource)
        time.sleep(5)


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--id', type=str, required=True, help="naver id")
parser.add_argument('-p', '--pwd', type=str, required=True, help="naver password")
parser.add_argument('-d', '--debug', type=str, required=False, action=argparse.BooleanOptionalAction, help="debug")
args = parser.parse_args()
if args.id is None:
    print('use -i or --id argument')
    exit(0)
if args.pwd is None:
    print('use -p or --pwd argument')
    exit(0)

run(args.id, args.pwd, args.debug)
