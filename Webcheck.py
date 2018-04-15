import os
import sys
import datetime
import requests
import twitter
import Webconf
import time
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
        pid_file = open('/var/run/Webcheck.pid', mode='w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
    if pid == 0:
        get()


def Post(result, month, day, hour, , minute, changeflag):
    auth = twitter.OAuth(consumer_key=Webconf.CK,
                         consumer_secret=Webconf.CS,
                         token=Webconf.AT,
                         token_secret=Webconf.ATS)
    po = twitter.Twitter(auth=auth)
    if result == 1:
        al = (str(Webconf.checksite) + '\nwas Changed\nChecktime:' +
              str(month) + '/' + str(day) + ' ' + str(hour) +
              ':' + str(minute))
        po.statuses.update(status=al)
    if hour == 0:
        up = (str(month) + '/' + str(day-1) + '\n' +
              str(Webconf.checksite) + ' chenged ' + str(changeflag) +
              ' times')
        po.statuses.update(status=up)


def get():
    flag = 0
    changeflag = 0
    checktime = 0
    result = 0
    try:
        origint = requests.get(Webconf.checksite)
    except:
        print('conection failed')
        time.sleep(30)
        get()
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
            flag = 0
            checktime += 15
            checktime %= 60
        Post(result, now.month, now.day, now.hour, now.minute, changeflag)
        if now.hour == 0:
            changeflag = 0
        time.sleep(45)
    return 0

if __name__ == '__main__':
    while True:
        daemonize()
