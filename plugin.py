import re
showPrint = True


def getToken(data):
    if showPrint:
        print('[Find Token]')
    data = data.replace('\n', '')
    token = re.findall(
        r'<input name="__RequestVerificationToken" type="hidden" value="(.*?)" />', data)
    if showPrint:
        print(f'[Info]find {len(token)} token elements!')
    if len(token) > 0:
        return token[0]
    else:
        return False


def trasferCookie(data):
    print('[Create]New cookie')
    cookie = ''
    for key in data:
        print('[KEY]', key)
        cookie += "{}={};".format(key, data[key])
    print('[Create]Success')
    return cookie
