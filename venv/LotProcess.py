import threading, requests, time

# LOT 처리 관련 쓰레드 클래스
class LotProcess (threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        resp = requests.get(self.url)
        time.sleep(1)
        print(self.url)
        print(resp.text)

