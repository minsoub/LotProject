import numpy as np
import csv
import os.path
from pymongo import MongoClient
import datetime
import json
from bson import json_util

machines = ['AVI58', 'AVI59']    # machine name
folder = 'D:/ExternalPJT/PythonPJT/opt_data/'   # '/home/hgkim11/optrontec/opt_data/'



def make_dict_from_lot_info_file(equip, lot_summary_file):
    sequence = ['lot정보', '수량', '블랙마킹개수', '상면NoPKG', '언로더진공불량', 'No PKG 불량',
                '상면검사 조건1불량[수량/수율]', '하면검사 조건1불량[수량/수율]']
    dicts = temp = {}
    dicts['Machine'] = m
    i = 0
    f = open(lot_summary_file, encoding='cp949')
    for line in f:
        print(line)
        if (line.strip() != ''):
            key, value = line.strip().split('\t')
            # print(key,value)
            temp[key.strip()] = value.strip()
            if (key.strip() == 'LotStartTime' or key.strip() == 'LotEndTime'):
                temp[key.strip()] = datetime.datetime.strptime(value.strip(), '%Y-%m-%d %H:%M:%S')
        else:
            if i:
                dicts[sequence[i]] = temp
            i = i + 1
            temp = {}
    f.close()
    return dicts


def make_dict_from__wafer_file(wafer_file):
    foreign_material = []
    sequence = ['wafer정보', '불량내역', '전체수량', '상면이물', 'No PKG 불량',
                '상면검사 조건1불량[수량/수율]', '하면검사 조건1불량[수량/수율]']
    dicts = temp = {}
    i = 0
    f = open(wafer_file, encoding='cp949')
    for line in f:
        # print(line)
        if (line.strip() != ''):
            if (i == 1):
                continue
            if (i == 7):
                # print(line.split('\t'))
                arr = make_array(line.split('\t'))
                foreign_material.append(arr)
            else:
                key, value = line.strip().split('\t')
                # print(key,value)
                temp[key.strip()] = value.strip()
                if (key.strip() == 'WaferStartTime' or key.strip() == 'WaferEndTime'):
                    temp[key.strip()] = datetime.datetime.strptime(value.strip(), '%Y-%m-%d %H:%M:%S')


        else:
            if i:
                dicts[sequence[i]] = temp
            i = i + 1
            # print(i)
            temp = {}
    f.close()
    dicts['foreign_material'] = foreign_material
    return dicts


now = ['[01라인]', '01:N:4: ', '02:G:0: ', '03:G:0: ', '04:N:2: ', '05:G:0: ', '06:N:1: ', '07:N:1: ', '08:N:1: ',
       '09:N:1: ', '10:N:1: ', '11:N:1: ', '12:N:6: ', '13:N:1: ', '14:N:1: ', '15:N:4: ', '\n']


def make_array(line_array):
    arr = []
    for j in line_array[1:-1]:
        # print(j.strip().split(':'))
        temp = j.strip().split(':')
        if (temp[1] == 'N'):
            blur = int(temp[2])
            arr.append(blur)
        else:
            arr.append(0)
            # print(line)
    return arr


def read_dimension_csv(csv_file):
    dimension_out = {}
    dimension_out['wafer_csv_file'] = csv_file
    print(csv_file)
    with open(csv_file) as f:
        reader = csv.reader(f)
        for i in range(6):
            next(reader)  # skip header
        data = []
        for row in reader:
            if (row != []):
                # print(row)
                data.append(row)

    data = data[1:]
    dimension_out['lines'] = []
    # print(int((len(data))/7))
    for cur_line in range(int((len(data)) / 7)):
        cur_dimension = data[cur_line * 7:(cur_line + 1) * 7]
        # print(cur_dimension[0][0])
        # dimension_out['LINE NO']=int(cur_dimension[0][0])
        dimension_out['lines'].append(int(cur_dimension[0][0]))
        now_line_dimension = {}
        for i in range(7):
            # print(cur_dimension,cur_dimension)
            # print([float(cur_dimension[i][j+2]) for j in range(noColumn+1)])
            now_line_dimension[cur_dimension[i][1]] = [float(j) for j in cur_dimension[i][2:-1]]
        dimension_out[cur_dimension[0][0]] = now_line_dimension
    return dimension_out


#client = MongoClient('localhost', 27017)
#db = client['optrontec']


# main
if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client['optrontec']

    # data delete
    db.lot_info.remove()

    # Lot folder
    for m in machines:
        target = folder + m + '/Lot Data'
        days = [f.path.split(target)[1] for f in os.scandir(target) if f.is_dir()]
        days.sort()
        # print(days)
        for d in days:
            lot_loc = target + d + '/'
            print(lot_loc)
            Lots = [f.path.split(lot_loc)[1] for f in os.scandir(lot_loc) if f.is_dir()]
            Lots.sort()
            for lot in Lots:
                print(lot_loc + lot + '/' + lot + '.txt')
                wafer_dict = {}
                if os.path.exists(lot_loc + lot + '/' + lot + '.txt'):
                    dicts = make_dict_from_lot_info_file(m, lot_loc + lot + '/' + lot + '.txt')
                    wafer_text_files = [f.name for f in os.scandir(lot_loc + lot + '/')
                                        if f.name.split('.')[0] != lot]
                    # print(wafer_text_files)

                    wafer_dict['wafer_lot_text_files'] = wafer_text_files

                    #dicts['wafer_lot_text_files'] = wafer_text_files
                    for wafer_file in wafer_text_files:
                        print(lot_loc + lot + '/' + wafer_file)
                        wafer_file_dict = make_dict_from__wafer_file(lot_loc + lot + '/' + wafer_file)

                        wafer_file_name = wafer_file.split('.')[0] + '_lot'
                        #dicts[wafer_file_name] = wafer_file_dict
                        wafer_dict[wafer_file_name] = wafer_file_dict
                    dicts['wafer_info'] = wafer_dict
                    dicts['createdDate'] = datetime.datetime.now()
                    dicts['Completed'] = True


                    result = db.lot_info.find_one({'LotEndTime': dicts['LotEndTime'],
                                                   'LotName': dicts['LotName'],
                                                   'LotStartTime': dicts['LotStartTime']})
                    if result == None:
                        _id = db.lot_info.insert_one(dicts).inserted_id
                        print(_id)

                else:  # 아직 lot가 완료되지 않음
                    print(lot_loc + lot + '/' + lot + '.txt  not exist')
                    print(lot)
                    dicts = {}
                    dicts['LotName'] = lot
                    dicts['Completed'] = False
                    dicts['LotStartTime'] = datetime.datetime.strptime("2030-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
                    dicts['LotEndTime'] = datetime.datetime.strptime("2030-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
                    wafer_text_files = [f.name for f in os.scandir(lot_loc + lot + '/')
                                        if f.name.split('.')[0] != lot]
                    dicts['wafer_lot_text_files'] = wafer_text_files
                    # print('not completed',wafer_text_files)
                    for wafer_file in wafer_text_files:
                        print(lot_loc + lot + '/' + wafer_file)
                        wafer_file_dict = make_dict_from__wafer_file(lot_loc + lot + '/' + wafer_file)

                        wafer_file_name = wafer_file.split('.')[0] + '_lot'
                        dicts[wafer_file_name] = wafer_file_dict
                    dicts['createdDate'] = datetime.datetime.now()
                    _id = db.lot_info.insert_one(dicts).inserted_id
                    print(_id)

    # Dimension folder
    for m in machines:
        target = folder + m + '/Dimension'
        days = [f.path.split(target)[1] for f in os.scandir(target) if f.is_dir()]
        days.sort()
        # print(days)
        for d in days:
            lot_loc = target + d + '/'
            print(lot_loc)
            Lots = [f.path.split(lot_loc)[1] for f in os.scandir(lot_loc) if f.is_dir()]
            Lots.sort()
            for lot in Lots:
                wafer_csv_files = [f.name for f in os.scandir(lot_loc + lot + '/')]
                # dicts['wafer_dimension_csv_files']=wafer_csv_files
                # print(wafer_csv_files)
                result = db.lot_info.find_one({'LotName': lot})

                if result != None:
                    dims = {}
                    for csv_file in wafer_csv_files:
                        wafer_csv_dict = read_dimension_csv(lot_loc + lot + '/' + csv_file)
                        wafer_file_name = csv_file.split('.')[0] + '_dim'
                        dims[wafer_file_name] = wafer_csv_dict

                    db.lot_info.update_one({'_id': result['_id']},
                                           {'$set': {'Dimensions': {'dims': dims, 'wafer_dimension_csv_files': wafer_csv_files}}})


    # UnloadNozzle folder
    for m in machines:
        target = folder + m + '/UnloadNozzle'
        days = [f.path.split(target)[1] for f in os.scandir(target) if f.is_dir()]
        days.sort()
        #print('sort ', days)
        for d in days:
            nozzle_dir = target + d + '/'
            # print(nozzle_dir)     # D:/ExternalPJT/PythonPJT/opt_data/AVI58/UnloadNozzle\2018-09-10/
            Lots = [f.path.split(nozzle_dir)[1] for f in os.scandir(nozzle_dir) if f.is_dir()]
            Lots.sort()
            print(Lots)
            for lot in Lots:
                lines_dir = nozzle_dir+lot+'/'
                lines = [f.path.split(lines_dir)[1] for f in os.scandir(lines_dir) if f.is_dir()]
                lines.sort()
                lst = {}
                lst_dir = {}
                for line in lines:
                    UnloadNozzle_files = [f.name for f in os.scandir(lines_dir + line + '/')]
                    result = db.lot_info.find_one({'LotName': lot})
                    if result != None:
                        lst[line] = UnloadNozzle_files
                        str_path = lines_dir + line + '/'
                        db.lot_info.update_one({'_id': result['_id']},
                                           {'$set': {'UnloadNozzle' : {'file_path' : str_path, 'lines' : lst}}})  # UnloadNozzle_files}})  # {'dims': dims, 'wafer_dimension_csv_files': wafer_csv_files}}})

    # UnloadNozzle folder
    for m in machines:
        target = folder + m + '/UnloadPos'
        days = [f.path.split(target)[1] for f in os.scandir(target) if f.is_dir()]
        days.sort()
        #print('sort ', days)
        for d in days:
            unpos_dir = target + d + '/'
            # print(unpos_dir)     # D:/ExternalPJT/PythonPJT/opt_data/AVI58/UnloadPos\2018-09-10/
            Lots = [f.path.split(unpos_dir)[1] for f in os.scandir(unpos_dir) if f.is_dir()]
            Lots.sort()
            print(Lots)
            for lot in Lots:
                lines_dir = unpos_dir+lot+'/'
                lines = [f.path.split(lines_dir)[1] for f in os.scandir(lines_dir) if f.is_dir()]
                lines.sort()
                lst = {}
                lst_dir = {}
                for line in lines:
                    UnPos_files = [f.name for f in os.scandir(lines_dir + line + '/')]
                    result = db.lot_info.find_one({'LotName': lot})
                    if result != None:
                        lst[line] = UnPos_files
                        str_path = lines_dir + line + '/'
                        db.lot_info.update_one({'_id': result['_id']},
                                           {'$set': {'UnloadPos' : {'file_path' : str_path, 'lines' : lst}}})  # UnloadNozzle_files}})  # {'dims': dims, 'wafer_dimension_csv_files': wafer_csv_files}}})



    # DB 등록이 완료되면 데이터를 읽어서 JSON 포멧으로 파일을 생성한다.
    result = db.lot_info.find()  #pretty()  #find_one();
    arr = []
    for r in result:
        # print(r)
        #y = json.dumps(r, indent=4, default=json_util.default)   # dict -> json
        #s = str(y) # r)
        arr.append(r)

    data = json.dumps(arr, indent=4, default=json_util.default, ensure_ascii=False)  # loads(arr)
    # print(data)

    with open('lot_data.json', 'w', encoding='UTF-8-sig') as file:
        file.write(data)  # json.dumps(dict, ensure_ascii=False))




