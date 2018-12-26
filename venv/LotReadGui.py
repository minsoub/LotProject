import PySimpleGUI as sg
import json
import os.path
from pprint import pprint

file_name = 'machine_env.json'

timeList =  ['17', '18', '19', '20', '21', '22', '23']

layout = [
    [sg.Text('데이터분석 및 전송 프로그램', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.OK('Save'), sg.Ok('Start'), sg.Exit('종료하기')],
    [sg.Text('Machine Data Location', size=(17, 1)), sg.Input(key='_machine_dir_'), sg.FolderBrowse('Search')],
    [sg.Text('Data Read Time',         size=(17, 1)), sg.InputCombo(timeList, key='_tmList_')],
    [sg.Text('전송 URL(Image)',         size=(17, 1)), sg.Input(key='_url_')],
    [sg.Text('Mongo DB URL',            size=(17, 1)), sg.Input(key='_db_url_')],
    [sg.Text('Mongo DB Port',           size=(17, 1)), sg.Input(key='_db_port_')],
    [sg.Text('Mongo DB Collection',    size=(17, 1)), sg.Input(key='_db_col_')],
    [sg.Text('Log Message')],
    [sg.Output(size=(80, 10))]
]

if __name__ == '__main__':
    # create the window
    window = sg.Window('데이터분석 및 전송 프로그램').Layout(layout)

    # 환경설정 파일 Load
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
    if os.path.exists(file_name):
        with open('machine_env.json') as f:
            data = json.load(f)

        if data is not None:
            pprint(data)
            window.FindElement('_machine_dir_').Update(data["env"]["machine_data_loc"])
            window.FindElement('_tmList_').Update(data["env"]["data_read_tm"])
            window.FindElement('_url_').Update(data["env"]["snd_url"])
            window.FindElement('_db_url_').Update(data["env"]["db_url"])
            window.FindElement('_db_port_').Update(data["env"]["db_port"])
            window.FindElement('_db_col_').Update(data["env"]["db_col"])

    while True:
        event, values = window.Read()
        if event is None or event == 'Exit':
            break

        if event == 'Save':
            # 입력 내용 체크
            if values['_machine_dir_'] is '':
                sg.Popup('Error', '머신 데이터 저장 폴더가 입력되지 않았습니다!!!')
            elif values['_tmList_'] is '':
                sg.Popup('Error', 'Data Read Time을 설정하지 않았습니다!!!')
            elif values['_url_'] is '':
                sg.Popup('Error', '전송 URL을 설정하지 않았습니다!!!')
            else :  # JSON 포멧으로 저장한다.
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
                with open(file_name, 'w', encoding='UTF-8') as mark_file:
                    json.dump(env_data, mark_file, ensure_ascii=False, indent='\t')


        # 기존 입력값을 설정한다.
        window.FindElement('_machine_dir_').Update(values['_machine_dir_'])
        window.FindElement('_tmList_').Update(values['_tmList_'])
        window.FindElement('_url_').Update(values['_url_'])
        window.FindElement('_db_url_').Update(values['_db_url_'])
        window.FindElement('_db_port_').Update(values['_db_port_'])
        window.FindElement('_db_col_').Update(values['_db_col_'])

        print(event, values)
    window.Close()


    # sg.Popup(event, number)
    #while True:
    #    event, values = window.Read()
    #    if event is None:
    #        break;
    # PySimpleGUI.main()
