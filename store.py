import json
import os
import os.path

def load():
    global data

    filePath = os.getenv('STORE_PATH')
    if not os.path.isfile(filePath):
        data = {}
        writeData()
    f = open(filePath, 'r')

    fileContent = f.read()
    if fileContent == '':
        fileContent = '\{\}'

    data = json.loads(fileContent)
    if not isinstance(data, dict):
        data = {}

    f.close()

def get(key: str):
    return data.get(key, None)

def set(key: str, value):
    data[key] = value
    writeData()

def delete(key: str):
    data.pop(key, None)
    writeData()

def writeData():
    f = open(os.getenv('STORE_PATH'), 'w')
    f.write(json.dumps(data))
    f.close()
