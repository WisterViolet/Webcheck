import datetime
import requests

flag = 0
changeflag = 0
checksite = 'http://www.official-robocon.com/kosen/'
checktime = 0
origint = requests.get(checksite)
while True:
    now = datetime.datetime.now()
    if (now.minute == checktime and flag == 0):
        flag = 1
        rest = requests.get(checksite)
        if origint.text != rest.text:
            print("Changed!")
            origint = requests.get(checksite)
        else:
            print("Not Changed")
        if now.minute == checktime+1:
            flag = 1
