import threading, requests, time
from datetime import datetime
import os.path

# LOT 처리 관련 쓰레드 클래스
class LotProcess (threading.Thread):
    stopSignal = True
    stopBit = 1
    stsTm = 0          # process start time
    sfile_name = 'lot_process_chk.dat'

    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def setTm(self, tm):
        self.stsTm = tm

    def setSignal(self, signal):
        self.stopSignal = signal

    def setStopBit(self, bit):
        self.stopBit = bit

    # 환경 파일 데이터 구조
    # - 파일이 없으면 처음이다.
    # - 0(진행여부 : 0(종료), 1(진행)):yyyyymmddHH24MISS(start time):0(Lot 완료여부):0(Dimension 완료여부):0(Nozzle):0(Pos):yyyyymmddHH24MISS(end time)
    def time_check_process(self):
        print('time_check_process called....')
        now = datetime.now()
        if self.stsTm == now.hour:  # 설정된 시각과 현재의 시간이 같으면
            print('설정된 시간과 현재의 시간이 같다')
            start_time = '%s%s%s%s%s%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
            if os.path.exists(self.sfile_name):   # 존재한다.
                r = open(self.sfile_name, mode='rt', encoding='utf-8')
                r.seek(0)
                line = r.readline()
                r.close()
                print(line)
            else:   # 처음이다.
                contents = '1:'+start_time+':0:0:0:0:0'
                # 파일에 작성한다.
                f = open(self.sfile_name, mode='wt', encoding='utf-8')
                f.writelines(contents)
                f.close()

    def run(self):
        print('프로세스가 시작되었습니다!!!')
        while True:
            if self.stopSignal is True:
                if self.stsTm != 0:
                    self.time_check_process()
                    #time.sleep(60 * 10)  # 10 minute
                else:
                    print('stopSignal is True')
                    resp = requests.get(self.url)
                    time.sleep(2)
                    print(self.url)
                    #print(resp.text)
                time.sleep(2)
            else:
                print('stopSignal is False')
                time.sleep(2)
                if self.stopBit == 0:
                    break
        print('프로세스가 종료되었습니다!!!')

