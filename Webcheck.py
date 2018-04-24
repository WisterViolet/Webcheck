import os
import sys
import datetime
import requests
import twitter
import Webconf
import keyAPI
import time


def daemonize():
    pid = os.fork()
    if pid > 0:
        pid_file = open('/var/run/Webcheck.pid', mode='w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
    if pid == 0:
        get()


def Post(result, month, day, hour,  minute, changeflag):
    auth = twitter.OAuth(consumer_key=keyAPI.CK,
                         consumer_secret=keyAPI.CS,
                         token=keyAPI.AT,
                         token_secret=keyAPI.ATS)
    po = twitter.Twitter(auth=auth)
    if result == 1:
        al = ('[Warning]It is Test\n' + str(Webconf.checksite) + '\nwas Changed\nChecktime:' +
              str(month) + '/' + str(day) + ' ' + str(hour) +
              ':' + str(minute))
        po.statuses.update(status=al)
    if (hour == 0 and minute == 0):
        up = (str(month) + '/' + str(day-1) + '\n' +
              str(Webconf.checksite) + ' chenged ' + str(changeflag) +
              ' times')
        po.statuses.update(status=up)


def get():
    checkf = 0
    changef = 0
    result = 0
    while True:
        now = datetime.datetime.now()
        if (now.minute in Webconf.checktime and checkf == 0):
            checkf = 1
            try:
                ht = requests.get(Webconf.checksite)
            except:
                time.sleep(30)
                get()
            if any(ht.text.find(item) for item in Webconf.checkword):
                result = 1
                changef += 1
            else:
                result = 0
            del ht
            Post(result, now.month, now.day, now.hour, now.minute, changef)
        time.sleep(30)
    return 0
if __name__ == '__main__':
    get()
