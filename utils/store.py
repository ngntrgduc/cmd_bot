import json
import os
import os.path

def load():
    global data

    storePath = os.getenv('STORE_PATH')
    if storePath == None:
        storePath = 'store.json'

    if not os.path.isfile(storePath):
        data = {}
        writeData()
    f = open(storePath, 'r')

    fileContent = f.read()
    if fileContent == '':
        fileContent = '{}'

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
    storePath = os.getenv('STORE_PATH')
    if storePath == None:
        storePath = 'store.json'

    f = open(storePath, 'w')
    f.write(json.dumps(data))
    f.close()
