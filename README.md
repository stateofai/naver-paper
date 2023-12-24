## Install
```
$ pip install naverpaper
```

## Example Code
```python
import time
import naverpaper

base_url = "https://www.clien.net/service/board/jirum"

if __name__ == "__main__":
    s = naverpaper.naver_session("##ID##", "##PASSWORD##")
    campaign_links = naverpaper.find_naver_campaign_links(base_url)
    #if campaign_links == []:
    #    print("모든 링크를 방문했습니다.")
    for link in campaign_links:
        response = s.get(link)
        #print(response.text)  # for debugging
        response.raise_for_status()
        time.sleep(5)
        print("캠페인 URL : " + link)
```

## Usage
> Please edit the example.py before you run and make sure that your Naver ID should be login with application password
```
$ git clone https://github.com/stateofai/naverpaper.git
$ cd naverpaper
$ pip install -r requirements.txt
$ python example.py 
```

## References
* https://help.naver.com/service/5640/contents/10219?lang=ko
* https://help.naver.com/service/5640/contents/8584?lang=ko
