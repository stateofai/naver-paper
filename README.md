## Usage
> Before you run , please edit the run.py and make sure that your Naver ID would be login with application password to avoid 2FA or CAPTCHA
```
$ git clone https://github.com/stateofai/naver-paper.git
$ cd naver-paper
$ pip install -r requirements.txt
$ python run.py 
```

## Example Code
```python
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
```

## References
* https://help.naver.com/service/5640/contents/10219?lang=ko
* https://help.naver.com/service/5640/contents/8584?lang=ko
