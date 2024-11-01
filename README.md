[![Naver Paper Python GitHub Actions](https://github.com/stateofai/naver-paper/actions/workflows/action.yml/badge.svg)](https://github.com/stateofai/naver-paper/actions/workflows/action.yml)

> 기존 requests 모듈을 이용한 로그인이 작동하지 않아 selenium을 사용하도록 변경되었습니다. (Thanks to @bagng)
> chromedriver 설치 후 코드를 실행해주세요.
> 리눅스(Ubuntu 22.04) 및 맥(macOS Sonoma)에서 작동 되는 것을 확인했습니다.
> 윈도우는 확인해보지 못했으나, 혹시 실행되신 분이 있으면 알려주세요.

### GitHub Actions 사용
1. 이 repo를 fork
2. secrets에 ID, PASSWORD 항목에 네이버 ID 및 패스워드 입력. ID라는 이름으로 네이버 ID를 넣고 PASSWORD라는 항목에 패스워드 입력
   CREDENTIALENV 항목에 복수 계정 입력. 값은 [{"id":"ID_1","pw":"PW_1"},{"id":"ID_2","pw":"PW_2"}] 형태 이어야 합니다.
   (Settings -> Secrets and variable -> Actions -> New repository secret)
3. 30분마다 주기적으로 실행되는 것을 확인
4. secrets TRY_LOGIN 항목에 로그인 재시도 횟수 입력, 기본값은 3번

## Prerequisites
### Install Google Chrome
```bash
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo apt-get update
$ sudo apt-get install -y gdebi-core
$ sudo gdebi google-chrome-stable_current_amd64.deb
```
> Verifying Google Chrome Installation
```bash
$ google-chrome --version
Google Chrome 120.0.6099.224
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
$ sudo cp chromedriver-linux64/chromedriver /usr/local/bin
$ sudo chmod a+x /usr/local/bin/chromedriver
$ /usr/local/bin/chromedriver --version
ChromeDriver 120.0.6099.109 (3419140ab665596f21b385ce136419fde0924272-refs/branch-heads/6099@{#1483})
```
## Usage
```
$ git clone https://github.com/stateofai/naver-paper.git
$ cd naver-paper
$ pip install -r requirements.txt

# 환경 변수로 USERNAME, PASSWORD 단일 계정 읽어서 실행
$ python run_new.py

# 환경 변수로 CREDENTIALENV 복수 계정 읽어서 실행
# CREDENTIALENV 값은 [{"id":"ID_1","pw":"PW_1"},{"id":"ID_2","pw":"PW_2"}] 형태 이어야 합니다.
$ python run_new.py

# argument 로 id, pw 입력
$ python run_new.py -i YOUR_ID -p YOUR_PW

# argument 로 멀티 계정 입력
$ python run_new.py -c '[{"id":"ID_1","pw":"PW_1"},{"id":"ID_2","pw":"PW_2"}]'

# 브라우저 표시 --no-headless
$ python run_new.py -c '[{"id":"ID_1","pw":"PW_1"}]' --no-headless

# credential-file로 로그인
$ python run_new.py -cf accounts.json
```

## Contribution
* 저는 전문개발자가 아니라 코드의 품질은 낮을 수 있습니다. 많은 능력자분들이 기여를 해주시면 좋겠어요

## References
* https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/win64/chromedriver-win64.zip
* https://help.naver.com/service/5640/contents/10219?lang=ko
* https://help.naver.com/service/5640/contents/8584?lang=ko
