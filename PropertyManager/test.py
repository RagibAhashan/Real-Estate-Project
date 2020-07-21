import time


f = open("copy.txt", "r")
x = f.read()
x.replace('\n', ' ')
f.close()

print('Replacing...')
time.sleep(5)

f = open("copy.txt", "a")

f.write(x)
f.close()


f = open("copy.txt", "r")
print(f.read())