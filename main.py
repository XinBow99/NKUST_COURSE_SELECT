
import requests
import plugin
import nkust
import threading
import SelectInfo


def Course(courseData):
    while True:
        try:
            # print('=========================================')
            NkustClinet = nkust.createSession()
            token = nkust.initPage(NkustClinet)
            nkust.login(NkustClinet, token, SelectInfo.UserInfo)
            selectToken = nkust.AddSelect(client=NkustClinet)
            if nkust.AddSelectCrs(clinet=NkustClinet, datas=courseData, token=selectToken):
                pass
            else:
                print(courseData, '選課成功！')
                open(courseData['name'] + '_success',
                     'w', encoding='utf8').write('選課成功')
                nkust.logout(NkustClinet)
                break
            nkust.logout(NkustClinet)
            NkustClinet.close()
        except Exception as e:
            print('[意外錯誤！]', e, courseData)


def main():
    NkustClinet = nkust.createSession()
    token = nkust.initPage(NkustClinet)
    nkust.login(NkustClinet, token, SelectInfo.UserInfo)
    print(nkust.about(NkustClinet))
    nkust.logout(NkustClinet)
    print('[Start Select!]')
    nkust.showPrint = False
    plugin.showPrint = False
    threads = []
    for course in SelectInfo.SelectInfo:
        threads.append(
            threading.Thread(target=Course, args=(course,))
        )
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    print('[start]')
    main()
    # std_account = input('[Enter]Your account:')
    # std_password = input('[Enter]Your password:')
    # check = login(("C107118116", "a9931543"))
