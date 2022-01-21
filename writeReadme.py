import json,calendar,time,os

def get_json_data(json_path):
    with open(json_path,'rb') as f:
        params = json.load(f)
    f.close()
    return params

def getMothDate(year, month):
    """
    返回某年某月的所有日期
    :param year:
    :param month:
    :return:
    """
    date_list = []
    for i in range(calendar.monthrange(year, month)[1] + 1)[1:]:
        str1 = str(year) + "-"+str("%02d" % month) +"-"+ str("%02d" % i)
        date_list.append(str1)
    return date_list

data=get_json_data("data.json")
days=len(data['data'])

timeY=int(time.strftime("%Y", time.localtime()))
timeMonth=int(time.strftime("%m", time.localtime()))
timeD=int(time.strftime("%d", time.localtime()))
timeH=int(time.strftime("%H", time.localtime()))
timeM=int(time.strftime("%M", time.localtime()))

if timeD==1 and timeH==0 and timeM==0:
    if timeMonth==1:
        timeMonth=2
    date_list = getMothDate(timeY, timeMonth-1)
    if not os.path.exists('historyData'):
        os.makedirs('historyData')
        if not os.path.exists('historyData/'+str(timeY)):
            os.makedirs('historyData/'+str(timeY))
    else:
        if not os.path.exists('historyData/'+str(timeY)):
            os.makedirs('historyData/'+str(timeY))
    f = open('historyData/'+str(timeY)+'/'+str(timeMonth-1)+'.md', 'w+')
    for date in date_list:
        if date in data['data']:
            # 删除messageID
            del data['data'][date]['messageId']
            f.write('| 日期 |')
            #每一日期的时间和毫升
            for time,ml in data['data'][date].items():
                f.write(' '+time+' |')
            f.write('\n'+'| :----: |')
            for time,ml in data['data'][date].items():
                f.write(' :----: |')
            f.write('\n'+'| '+date+' |')
            for time,ml in data['data'][date].items():
                f.write(' '+str(ml)+' |')
            f.write('\n\n')
    f.close

data=get_json_data("data.json")
if days >= 30:
    f = open('README.md', 'w+')
    f.write('# 近30日饮水数据\n')
    #日期和值
    i=0
    #日期和值
    for date,value in data['data'].items():
        # 删除messageID
        del data['data'][date]['messageId']
        f.write('| 日期 |')
        #每一日期的时间和毫升
        for time,ml in data['data'][date].items():
            f.write(' '+time+' |')
        f.write('\n'+'| :----: |')
        for time,ml in data['data'][date].items():
            f.write(' :----: |')
        f.write('\n'+'| '+date+' |')
        for time,ml in data['data'][date].items():
            f.write(' '+str(ml)+' |')
        f.write('\n\n')
        i+=1
        if i>30:
            break
    f.close
else:
    f = open('README.md', 'w+')
    f.write('# 近30日饮水数据\n')
    #日期和值
    for date,value in data['data'].items():
        # 删除messageID
        del data['data'][date]['messageId']
        f.write('| 日期 |')
        #每一日期的时间和毫升
        for time,ml in data['data'][date].items():
            f.write(' '+time+' |')
        f.write('\n'+'| :----: |')
        for time,ml in data['data'][date].items():
            f.write(' :----: |')
        f.write('\n'+'| '+date+' |')
        for time,ml in data['data'][date].items():
            f.write(' '+str(ml)+' |')
        f.write('\n\n')
    f.close