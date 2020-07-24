import os
import json
import time

PATH = os.getcwd()
files = list(os.listdir(PATH))
files.remove('CleanFiles.py')
first = files[0]
files.remove(first)


og_file = {}
new_version = {}

with open(first, 'r') as json_file:
    og_file = json.load(json_file)

for item in og_file:
    new_version[item['Address']] = item


print(og_file[0])
print('\n\n\n\n\n\n\n\n\n\n\n\n')
print(new_version)

with open('test.json', 'w') as outfile:
    json.dump(new_version, outfile)

# for js_file in files:
#     data = []
#     with open(js_file, 'r') as json_file:
#         data = json.load(json_file)
#     print(data)