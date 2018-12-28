import PySimpleGUI as sg
import json
import os.path
from pprint import pprint
import threading, requests, time

from LotProcess import LotProcess


file_name = 'machine_env.json'
timeList =  ['17', '18', '19', '20', '21', '22', '23']

layout = [
    [sg.Text('데이터분석 및 전송 프로그램', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.OK('설정정보 저장', key='Save'), sg.Ok('프로세스 시작', key='Start'), sg.Ok('프로세스 종료', key='End'), sg.Exit('종료하기', key='Exit')],
    [sg.Text('Machine Data Location', size=(17, 1)), sg.Input(key='_machine_dir_', disabled='true'), sg.FolderBrowse('Search')],
    [sg.Text('Data Read Time',         size=(17, 1)), sg.InputCombo(timeList, key='_tmList_')],
    [sg.Text('전송 URL(Image)',         size=(17, 1)), sg.Input(key='_url_')],
    [sg.Text('Mongo DB URL',            size=(17, 1)), sg.Input(key='_db_url_')],
    [sg.Text('Mongo DB Port',           size=(17, 1)), sg.Input(key='_db_port_')],
    [sg.Text('Mongo DB Collection',    size=(17, 1)), sg.Input(key='_db_col_')],
    [sg.Text('Log Message')],
    [sg.Output(size=(80, 10))]
]

# 환경설정 파일을 로드한다.
# {
#   "env": {
#      "machine_data_loc": "c://xxx",
#      "data_read_tm" : 12,
#      "snd_url" : url
#      "db_url" : db_url
#      "db_port" : db_port
#      "db_col" : db_col
#   }
# }
def EnvFileRead(window):
    if os.path.exists(file_name):
        with open('machine_env.json') as f:
            data = json.load(f)

        if data is not None:
            print(data)
            window.FindElement('_machine_dir_').Update(data["env"]["machine_data_loc"])
            window.FindElement('_tmList_').Update(data["env"]["data_read_tm"])
            window.FindElement('_url_').Update(data["env"]["snd_url"])
            window.FindElement('_db_url_').Update(data["env"]["db_url"])
            window.FindElement('_db_port_').Update(data["env"]["db_port"])
            window.FindElement('_db_col_').Update(data["env"]["db_col"])

# 등록한 환경정보를 JSON 포멧으로 파일에 저장한다.
# 기존에 등록한 파일이 있으면 덮어쓴다.
def EnvSave(values):
    # 입력 내용 체크
    if values['_machine_dir_'] is '':
        sg.Popup('Error', '머신 데이터 저장 폴더가 입력되지 않았습니다!!!')
    elif values['_tmList_'] is '':
        sg.Popup('Error', 'Data Read Time을 설정하지 않았습니다!!!')
    elif values['_url_'] is '':
        sg.Popup('Error', '전송 URL을 설정하지 않았습니다!!!')
    else:  # JSON 포멧으로 저장한다.
        env_data = {}
        env = {}
        env['machine_data_loc'] = values['_machine_dir_']
        env['data_read_tm'] = values['_tmList_']
        env['snd_url'] = values['_url_']
        env['db_url'] = values['_db_url_']
        env['db_port'] = values['_db_port_']
        env['db_col'] = values['_db_col_']
        env_data['env'] = env
        # JSON 포멧으로 파일에 저장한다.
        print('환경정보 저장')
        print(env_data)
        with open(file_name, 'w', encoding='UTF-8') as mark_file:
            json.dump(env_data, mark_file, ensure_ascii=False, indent='\t')

def getHTML(url):
    resp = requests.get(url)
    time.sleep(1)
    print(url, len(resp.text))

t = LotProcess('http://google.com')


if __name__ == '__main__':
    # create the window
    window = sg.Window('데이터분석 및 전송 프로그램').Layout(layout)

    # 환경설정 파일 Load
    EnvFileRead(window)

    t.setSignal(False)
    t.start()

    while True:
        event, values = window.Read()
        #print (event, values)
        if event is None or event == 'Exit':
            break

        if event == 'Save':
            EnvSave(values)
        elif event == 'Start':    # process start
            print(event)
            t.setTm(int(values['_tmList_']))
            t.setSignal(True)
        elif event == 'End':     # process end
            t.setSignal(False)   # process stop
            # while True:
            #     if t.is_alive() is False:
            #         break
            #     else:
            #         t.join()
            #         time.sleep(1)

        # 기존 입력값을 설정한다.
        window.FindElement('_machine_dir_').Update(values['_machine_dir_'])
        window.FindElement('_tmList_').Update(values['_tmList_'])
        window.FindElement('_url_').Update(values['_url_'])
        window.FindElement('_db_url_').Update(values['_db_url_'])
        window.FindElement('_db_port_').Update(values['_db_port_'])
        window.FindElement('_db_col_').Update(values['_db_col_'])

        #print(event, values)

    t.setSignal(False)
    t.setStopBit(0)
    t.join()
    window.Close()


    # sg.Popup(event, number)
    #while True:
    #    event, values = window.Read()
    #    if event is None:
    #        break;
    # PySimpleGUI.main()
