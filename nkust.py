import requests
import plugin
import re
import html
import random
import time
showPrint = True


def createSession():
    if showPrint:
        print('=========================================')
        print('[INFO]createSession')
    headers = {
        'Accept': 'test{}'.format(random.randint(0,999)),
        'User-Agent': 'test{}'.format(random.randint(0,999)),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://aais4.nkust.edu.tw/selcrs_std/FirstSelect/SelectPage',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'test{}'.format(random.randint(0,999)),
        'Connection': 'keep-alive',
    }
    client = requests.session()
    client.headers.update(headers)
    client.verify = True
    if showPrint:
        print('[INFO]createSession success')
    return client


def initPage(client):
    if showPrint:
        print('=========================================')
        print('[INFO]initPage')
    thisUrl = "https://aais4.nkust.edu.tw/selcrs_std"
    res = client.get(thisUrl, timeout=5)
    if showPrint:
        print('[Server status]->', res.status_code)
    token = plugin.getToken(res.text)
    if showPrint:
        print('[INFO]initPage success')
    return token


def login(client, token, userData):
    if showPrint:
        print('=========================================')
        print('[INFO]login')
    thisUrl = "https://aais4.nkust.edu.tw/selcrs_std/Login"
    res = client.post(
        thisUrl,
        data={
            '__RequestVerificationToken': token,
            'Url': '',
            'UserAccount': userData['account'],
            'Password': userData['password']
        }, timeout=5
    )
    if showPrint:
        print('[Server status]->', res.status_code)
    client.headers.update(
        {
            'RequestVerificationToken': token,
            'X-Requested-With': 'XMLHttpRequest'
        }
    )
    if showPrint:
        print('[INFO]login success')


def logout(client):
    if showPrint:
        print('=========================================')
        print('[INFO]logout')
    # https://aais4.nkust.edu.tw/selcrs_std/Login/Logout
    thisUrl = "https://aais4.nkust.edu.tw/selcrs_std/Login/Logout"
    res = client.get(thisUrl, timeout=5)
    #if showPrint:
    print('[Server status]->', res.status_code)
    #if showPrint:
    print('[INFO]logout success')


def about(client):
    print('=========================================')
    print("[INFO]about")
    thisUrl = "https://aais4.nkust.edu.tw/selcrs_std/Home/About"
    res = client.get(
        thisUrl, timeout=5
    )
    print('[Server status]->', res.status_code)
    aboutText = res.text.strip("\n")
    aboutRE = re.findall(
        r'<label class="badge badge-info">(.*?)</label>(.*?)</span>', aboutText)[0]
    print("[INFO]about success")
    return html.unescape(aboutRE[0]), html.unescape(aboutRE[1])

# 以下為選課


def AddSelect(client):
    if showPrint:
        print('=========================================')
        print('[INFO]進入加退選頁面')
        print('[INFO]取得加退選Token')
    # print('[ENTER]AddSelect')
    thisUrl = "https://aais4.nkust.edu.tw/selcrs_std/AddSelect/AddSelectPage"
    res = client.get(thisUrl, timeout=5)
    token = plugin.getToken(res.text)
    if showPrint:
        print("[INFO]AddSelect success")
    return token


def AddSelectCrs(clinet, datas, token):
    if showPrint:
        print('=========================================')
        print('[INFO]開始進行加退選...')
        print('[INFO]加退選課程資訊為', datas)
    # print("[ENTER]AddSelectCrs")
    thisUrl = "https://aais4.nkust.edu.tw/selcrs_std/AddSelect/AddSelectCrs"
    clinet.headers.update({
        'RequestVerificationToken': token,
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    res = clinet.post(thisUrl, data=datas, timeout=5)
    error = re.findall(
        r'<input id="errorInfo" type="hidden" value="(.*?)" />', res.text.strip('\n'))
    flag = False
    if error:
        # print(datas)
        error = error[0]
        print('==========>\n', '[ERROR]', datas['name'],
              html.unescape(error), '<==========')
        flag = True
    else:
        print(datas['CrsNo'], res.json())
        if str(res.json()['result']) == '1':
            flag = False
        else:
            flag = True
    return flag
