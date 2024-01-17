import time
from naver import session as s
from naver import find as f

base_url = "https://www.clien.net/service/board/jirum"

if __name__ == "__main__":
    driver = s.session("20eung", "ZFHUJEUXFLBG")
#   driver = s("20eung", "ZFHUJEUXFLBG")
    campaign_links = f.find(base_url)

    if campaign_links == []:
        print("모든 링크를 방문했습니다.")

    for link in campaign_links:
        driver.get(link)
        page_source = driver.page_source

        print(page_source)  # for debugging

        time.sleep(5)
        print("캠페인 URL : " + link)

    driver.quit()
