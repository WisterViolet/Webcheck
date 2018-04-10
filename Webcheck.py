import os
import sys
import datetime
import requests
import twitter
import Webconf
'''
In Webconf
checksite:URL of site you want to monitor
CK:Consumer_Key
CS:Consumer_Secret_Key
AT:Access_Token
ATS:Access_Token_Secret
'''


def daemonize():
    pid = os.fork()
    if pid > 0:
        pid_file = open('/var/run/Webcheck.pid')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
    if pid == 0:
        Post()


def Post(result, month, day, hour, changeflag):
    auth = twitter.OAuth(consumer_key=Webconf.CK,
                         consumer_secret=Webconf.CS,
                         token=Webconf.AT,
                         token_secret=Webconf.ATS)
    po = twitter.Twitter(auth=auth)
    if result == 1:
        al = ('【テスト】\n' + str(Webconf.checksite) + '\nの更新を検出しました(もしかしたら間違いかも)')
        po.statuses.update(status=al)
    if hour == 0:
        up = ('【テスト】\n' + str(month) + '月' + str(day-1) + '日、\n' +
              str(Webconf.checksite) + '\nは' + str(changeflag) +
              '回更新されました(もしかしたら間違いかも)')
        po.statuses.update(status=up)


def get():
    flag = 0
    changeflag = 0
    checktime = 0
    result = 0
    origint = requests.get(Webconf.checksite)
    while True:
        now = datetime.datetime.now()
        if (now.minute == checktime and flag == 0):
            flag = 1
            changeflag += 1
            rest = requests.get(checksite)
            if origint.text != rest.text:
                result = 1
                origint = requests.get(Webconf.checksite)
            else:
                result = 0
        if now.minute == checktime+1:
            flag = 1
        Post(result, now.month, now.day, now.hour, changeflag)
        if now.hour == 0:
            changeflag = 0
    return 0

if __name__ == '__main__':
    while True:
        daemonize()
