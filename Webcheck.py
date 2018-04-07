import datetime
import requests
import Webconf
'''
In Webconf
checksite:URL of site you want to monitor
CK:Consumer_Key
CS:Consumer_Secret_Key
AT:Access_Token
ATS:Access_Token_Secret
'''

flag = 0
changeflag = 0
checktime = 0
origint = requests.get(Webconf.checksite)
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
