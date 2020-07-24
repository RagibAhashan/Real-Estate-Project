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
        if len(item['Address']) > 37:
            addr = item['Address'][:37]
        else:
            addr = item['Address']
        new_version[addr] = item

    with open('./filtered/{}.json'.format(datetime.datetime.now()), 'w') as outfile:
        json.dump([new_version], outfile)
    
    os.remove(file_name)

# 'error_saved_2020-07-23 13:58:15.881524.json'
if __name__ == "__main__":
    PATH = os.getcwd()
    files = list(os.listdir(PATH))
    files.remove('CleanFiles.py')
    files.remove('filtered')

    for json_file_names in files:
        print(json_file_names + '--> transforming')
        time.sleep(1)
        reformat_file(json_file_names)  