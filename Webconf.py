checksite = 'http://www.official-robocon.com/kosen/'
checkword = ['2018']
checktime = (*range(0, 60, 5),)
timeloger = '/home/wister/Documents/logfile/timel.log'


def logstamp(month, day, hour, minute):
    try:
        logfile = open(timeloger, 'a')
        logfile.write(str(month) + '/' + str(day) + ' ' + str(hour) + ':' +
                      str(minute))
        logfile.close()
    except:
        return -1
    return 0
