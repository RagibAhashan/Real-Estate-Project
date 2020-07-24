import os
import json
import time
import datetime

def reformat_file(file_name: str):
    og_file = {}
    new_version = {}

    with open(file_name, 'r') as json_file:
        og_file = json.load(json_file)

    for item in og_file:
        addr = item['Address']
        new_version[addr] = item

    with open('./filtered/{}.json'.format(datetime.datetime.now()), 'w') as outfile:
        json.dump(new_version, outfile)
    
    os.remove(file_name)

def unify_json_files(PATH: str):
    PATH = os.getcwd() + '/filtered'
    all_files_names = list(os.listdir(PATH))
    main_file = {}
    js_file = {}
    for file_name in all_files_names:
        with open('./filtered/'+file_name, 'r') as json_file:
            js_file = json.load(json_file)

        for key in js_file:
            main_file[key] = js_file[key]
    
    with open('./filtered/all_data_unified.json', 'w') as outfile:
        json.dump(main_file, outfile)


def revert_to_old_format():
    js_file = {}
    new_file = []
    with open('./filtered/all_data_unified.json', 'r') as json_file:
            js_file = json.load(json_file)
    
    for key in js_file:
        new_file.append(js_file[key])
    
    with open('./filtered/fixed.json', 'w') as outfile:
        json.dump(new_file, outfile)


if __name__ == "__main__":
    # PATH = os.getcwd()
    # files = list(os.listdir(PATH))
    # files.remove('CleanFiles.py')
    # files.remove('filtered')

    # for json_file_names in files:
    #     print(json_file_names + '--> transforming')
    #     time.sleep(1)
    #     reformat_file(json_file_names)

    # unify_json_files(PATH + '/filtered')

    with open('./filtered/all_data_unified.json', 'r') as json_file:
        js_file = json.load(json_file)
    
        print(len(js_file))