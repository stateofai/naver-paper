import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# disable InsecureRequestWarning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

base_url = "https://www.damoang.net/economy"
site = "damoang"

def find_naver_campaign_links(visited_urls_file='visited_urls_'+ site +'.txt'):
    # Read visited URLs from file
    try:
        with open(visited_urls_file, 'r') as file:
            visited_urls = set(file.read().splitlines())
    except FileNotFoundError:
        visited_urls = set()

    # Send a request to the base URL
    request_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(base_url, timeout=5, headers=request_headers, verify=False)
        print(f"{site}\tlist get HTTP STATUS : {response.status_code}")
    except:
        print(f"{site}\tlist get error\r\n{base_url}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all span elements with class 'list_subject' and get 'a' tags
    list_subject_links = soup.find_all('li', class_='list-group-item')

    naver_links = []
    for span in list_subject_links:
        a_tag = span.find('a', href=True)
        if a_tag and '네이버' in a_tag.text:
            naver_links.append(a_tag['href'])

    # Initialize a list to store campaign links
    campaign_links = []

    # Check each Naver link
    for link in naver_links:
        full_link = urljoin(base_url, link)
        print(f"{site}\tlinks : " + full_link)
        if full_link in visited_urls:
            continue  # Skip already visited links

        try:
            res = requests.get(full_link, headers=request_headers)
        except:
            print(f"{site}\tfull link get error\r\n{full_link}")
            pass
        inner_soup = BeautifulSoup(res.text, 'html.parser')

        # Find all links that start with the campaign URL
        for a_tag in inner_soup.find_all('a', href=True):
            campaign_link = a_tag['href']

            if ('campaign2-api.naver.com' in campaign_link or 'ofw.adison.co' in campaign_link) and campaign_link not in campaign_links:
                campaign_links.append(campaign_link)

        # Add the visited link to the set
        visited_urls.add(full_link)

    # Save the updated visited URLs to the file
    with open(visited_urls_file, 'w') as file:
        for url in visited_urls:
            file.write(url + '\n')

    return campaign_links


if __name__ == "__main__":
    find_naver_campaign_links()
