import sys
j = 'abcd 54321'
k = j.find(' ')
print(k)
value = j[j.find(' '):]
print(value)

print(type(sys.argv))

if '4' in j:
    print("yup")