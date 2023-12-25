import time
from naver import session as s
from naver import find as f

base_url = "https://www.clien.net/service/board/jirum"

if __name__ == "__main__":
    s = s.session("##ID##", "##PASSWORD##")
    campaign_links = f.find(base_url)
    if campaign_links == []:
        print("모든 링크를 방문했습니다.")
    for link in campaign_links:
        response = s.get(link)
        print(response.text)  # for debugging
        response.raise_for_status()
        time.sleep(5)
        print("캠페인 URL : " + link)
