## Usage
> Install Google Chrome
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get update
sudo apt-get install -y gdebi-core
sudo gdebi google-chrome-stable_current_amd64.deb
```

> Verifying Google Chrome Installation
```bash
google-chrome --version
```

> Install ChromeDriver
- Go to [https://googlechromelabs.github.io/chrome-for-testing/]
- Download ChromeDriver same as Google Chrome Version
- Unzip and Copy chromedriver binary file to /usr/bin/chromedriver

> This is example
```bash
$ google-chrome --version
Google Chrome 120.0.6099.109

$ wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip
--2024-01-17 10:01:07--  https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip
Resolving edgedl.me.gvt1.com (edgedl.me.gvt1.com)... 34.104.35.123, 2600:1900:4110:86f::
Connecting to edgedl.me.gvt1.com (edgedl.me.gvt1.com)|34.104.35.123|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 8624482 (8.2M) [application/octet-stream]
Saving to: ‘chromedriver-linux64.zip’

chromedriver-linux64.zip   100%[=======================================>]   8.22M  5.21MB/s    in 1.6s

2024-01-17 10:01:10 (5.21 MB/s) - ‘chromedriver-linux64.zip’ saved [8624482/8624482]

$ unzip chromedriver-linux64.zip
Archive:  chromedriver-linux64-120.0.6099.109.zip
  inflating: chromedriver-linux64/LICENSE.chromedriver
  inflating: chromedriver-linux64/chromedriver

$ sudo cp chromedriver-linux64/chromedriver /usr/bin
$ sudo chmod a+x /usr/bin/chromedriver

$ /usr/bin/chromedriver --version
ChromeDriver 120.0.6099.109 (3419140ab665596f21b385ce136419fde0924272-refs/branch-heads/6099@{#1483})
```

> Before you run , please edit the run.py and make sure that your Naver ID would be login with application password to avoid 2FA or CAPTCHA
```bash
$ git clone https://github.com/20eung/naver-paper.git
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
