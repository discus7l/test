
from locPack import memsourceControl
import requests
import logging
import logging.handlers
from pprint import pprint
import csv
import time

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] - %(message)s')

logHandler = logging.handlers.RotatingFileHandler('debug.log', maxBytes=10485760, backupCount=1, encoding='utf-8')
logHandler.setFormatter(formatter)
logHandler.setLevel(logging.DEBUG)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
streamHandler.setLevel(logging.INFO)

logger.addHandler(logHandler)
logger.addHandler(streamHandler)



def createProject(token, name, sourceLang, targetLangs):
    try:
        url = 'https://cloud.memsource.com/web/api2/v3/projects'
        headers = {'Authorization': f'ApiToken {token}'}
        data = {
            'name': name,
            'sourceLang': sourceLang,
            'targetLangs': targetLangs
            }
        response = requests.post(url, headers=headers, json=data)
        createProjectRes = response.json()
    except:
        exceptionError = 'test error message'
        taskRes = 1
        myError = 'myError'
        logger.exception(exceptionError)
        return myError, taskRes, exceptionError
    return createProjectRes

def getJobInfo(token, projectUid, jobUid):
    try:
        url = f'https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}'
        headers = {'Authorization': f'ApiToken {token}'}
        response = requests.get(url, headers=headers)
        getJobInfoRes = response.json()
        getJobInfoResCode = response.status_code
        getJobInfoResHeaders = response.headers
    except:
        exceptionError = 'test error message'
        taskRes = 1
        myError = 'myError'
        logger.exception(exceptionError)
        return myError, taskRes, exceptionError
    return getJobInfoRes, getJobInfoResCode, getJobInfoResHeaders

def downloadTargetAsync(token, projectUid, jobUid):
    try:
        url = f'https://cloud.memsource.com/web/api2/v2/projects/{projectUid}/jobs/{jobUid}/targetFile'
        headers = {'Authorization': f'ApiToken {token}'}
        response = requests.put(url, headers=headers)
        downloadTargetAsyncRes = response.json()
        downloadTargetAsyncResCode = response.status_code
    except:
        exceptionError = 'test error message'
        taskRes = 1
        myError = 'myError'
        logger.exception(exceptionError)
        return myError, taskRes, exceptionError
    return downloadTargetAsyncRes, downloadTargetAsyncResCode

def downloadAsyncRequest(token, projectUid, jobUid, asyncRequestId):
    try:
        url = f'https://cloud.memsource.com/web/api2/v2/projects/{projectUid}/jobs/{jobUid}/downloadTargetFile/{asyncRequestId}'
        headers = {'Authorization': f'ApiToken {token}'}
        response = requests.get(url, headers=headers)
        downloadAsyncRequestRes = response.text
        downloadAsyncRequestResCode = response.status_code
        downloadAsyncRequestResHeaders = response.headers
    except:
        exceptionError = 'test error message'
        taskRes = 1
        myError = 'myError'
        logger.exception(exceptionError)
        return myError, taskRes, exceptionError
    return downloadAsyncRequestRes, downloadAsyncRequestResCode, downloadAsyncRequestResHeaders

def listAsyncRequests(token):
    try:
        url = 'https://cloud.memsource.com/web/api2/v1/async'
        headers = {'Authorization': f'ApiToken {token}'}
        response = requests.get(url, headers=headers)
        listAsyncRequestsRes = response.json()
    except:
        exceptionError = 'test error message'
        taskRes = 1
        myError = 'myError'
        logger.exception(exceptionError)
        return myError, taskRes, exceptionError
    return listAsyncRequestsRes

def downloadTargetFile(token, projectUid, jobUid):
    try:
        url = f'https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}/targetFile'
        headers = {'Authorization': f'ApiToken {token}'}
        response = requests.get(url, headers=headers)
        downloadTargetFileRes = response.text

    except:
        exceptionError = 'test error message'
        taskRes = 1
        myError = 'myError'
        logger.exception(exceptionError)
        return myError, taskRes, exceptionError
    return downloadTargetFileRes



# Create project

# name = 'test001'
# sourceLang = 'ja'
# targetLangs = ['en']

# createProjectRes = createProject(token, name, sourceLang, targetLangs)
# print(createProjectRes)

# TEST
# projectUid = 'TJJOQ19Fi8MEfyzZfwgPN4'
# jobUid = '53rpgDFbojqu8JOdTd2EC2'
# tokenRes = memsourceControl.loginMemsource('', '')

# STAGING
projectUid = 'ZFmrQtfaHQo93BwF0AW1zc'
jobUid = 'eOqZHRAv63aDeddf7Fyei1'
# tokenRes = memsourceControl.loginMemsource('', '')

# token = tokenRes['token']
token = ''
# print(tokenRes['token'])

####----getJobInfo----####
getJobInfoRes = getJobInfo(token, projectUid, jobUid)
logger.debug(getJobInfoRes[0]) # Response content
logger.debug(getJobInfoRes[1]) # Response code
logger.debug(getJobInfoRes[2]) # Response headers

# Process file name
targetLang = getJobInfoRes[0]['targetLang']
fileName = getJobInfoRes[0]['filename']
splitFilename = fileName.split('.')

if len(splitFilename) > 2:
    print('Invalid file name!')
    exit()

finalFileName = f'{splitFilename[0]}_{targetLang}.{splitFilename[1]}'
logger.debug(finalFileName)


####----downloadTargetAsync----####
downloadTargetAsyncRes = downloadTargetAsync(token, projectUid, jobUid)
logger.debug(downloadTargetAsyncRes[0]) # Response content
pprint(downloadTargetAsyncRes[1]) # Response code
pprint(downloadTargetAsyncRes[0]['asyncRequest']['id'])


####----downloadAsyncRequest----####
asyncRequestId = downloadTargetAsyncRes[0]['asyncRequest']['id']
res = downloadAsyncRequest(token, projectUid, jobUid, asyncRequestId)

while res[1] != 200:
    print(f'Current state code: {res[1]}')
    print('Waiting for Phrase...')
    res = downloadAsyncRequest(token, projectUid, jobUid, asyncRequestId)
    time.sleep(2)

print('Async request completed...')
logger.debug(res[0]) # Response content
logger.debug(res[2]) # Response headers
pprint(res[1]) # Response code


####----Write to file----####
with open(finalFileName, 'w', encoding='utf-8-sig', newline='') as f:
    writeRes = f.write(res[0])




# Open, read file, and and add comment
# with open(finalFileName, 'r', encoding='utf-8-sig', newline='') as f:
#     reader = csv.DictReader(f)
#     for i in reader:
#         print(i['Comment'])
