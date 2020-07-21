import json

data = {}
data = []
data.append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data.append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data.append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)