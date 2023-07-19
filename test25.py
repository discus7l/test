
fileList = ['a','a','a','b','b','b','c']
idList = ['a1','a2','a3','b1','b2','b3','c']
dictionary = {}

noDupeFileList = list(set(fileList))

counter = len(noDupeFileList)


while counter > 0:
    dictionary[noDupeFileList[counter -1]] = []
    counter = counter -1

for index, value in enumerate(idList):
    dictionary[fileList[index]].append(value)

for items in dictionary:
    print(items)
    print(dictionary[items])
    print('----')

