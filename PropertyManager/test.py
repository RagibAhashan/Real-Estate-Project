x = '1 / 254 '
# print(x.find('/'), len(x)-1)
print(int(x[(x.find('/')+2):(len(x)-1)]))