import json,calendar,time,os,sys,requests,datetime
import matplotlib.pyplot as plt

def write_json_data(dict,path):
    with open(path,'w') as r:
        json.dump(dict,r)
    r.close()

def get_json_data(json_path):
    if len(sys.argv)>1:
        params = json.loads(requests.get(str(sys.argv[1])).text)
        if 'data' not in params:
            with open(json_path,'rb') as f:
                params = json.load(f)
            f.close()
        else:
            write_json_data(params,'data.json')
    else:
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

#timeD=1
#timeH=0
#timeM=30

if timeD==1 and timeH==0 and timeM<=30:
    if timeMonth==1:
        timeMonth=13
        timeY=timeY-1
    date_list = getMothDate(timeY, timeMonth-1)
    if not os.path.exists('historyData'):
        os.makedirs('historyData')
    if not os.path.exists('historyData/'+str(timeY)):
        os.makedirs('historyData/'+str(timeY))
    if not os.path.exists('historyData/'+str(timeY)+'/'+str(timeMonth-1)):
        os.makedirs('historyData/'+str(timeY)+'/'+str(timeMonth-1))
    
    f = open('historyData/'+str(timeY)+'/'+str(timeMonth-1)+'/'+str(timeMonth-1)+'.md', 'w+',encoding='utf-8')
    
    dateList=[]
    mlList=[]
    monthData={'all':0,'average':0}
    monthAll=0
    monthCount=0
    for date in date_list:
        if date in data['data']:
            monthData[date]=data['data'][date]
            dateList.append(time.strftime('%d', time.strptime(date,"%Y-%m-%d")))
            mlList.append(data['data'][date]['all'])
            monthAll += int(data['data'][date]['all'])
            monthCount += 1
    monthData['all']=monthAll
    monthData['average']=int(monthAll/monthCount)
    plt.style.use('seaborn-muted')
    fig, ax = plt.subplots(figsize=(18, 6),dpi=100)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.bar(dateList, mlList,width=0.45)
    plt.axhline(y=2000, linestyle='--', color='red')
    # 设置字体
    font = {'family': 'serif', 'color': '#999999'}
    plt.xlabel('time',fontdict=font)
    plt.ylabel('ml',fontdict=font)
    for a, b in zip(dateList, mlList):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom',fontdict=font)

    # 设置坐标轴颜色
    ax = plt.gca()  # 获取当前坐标轴
    ax.spines['bottom'].set_color('#999999')  # 设置底边框颜色
    ax.spines['left'].set_color('#999999')  # 设置左边框颜色
    ax.tick_params(axis='both', colors='#999999')  # 设置刻度颜色
    fig.tight_layout()
    plt.savefig('historyData/'+str(timeY)+'/'+str(timeMonth-1)+'/'+str(timeMonth-1)+'.png',transparent=True)
    write_json_data(monthData,'historyData/'+str(timeY)+'/'+str(timeMonth-1)+'/'+str(timeMonth-1)+'.json')
    
    f.write('<div align=center>'+'\n'+'<img src="'+str(timeMonth-1)+'.png"style="zoom: 100%;" />'+'\n\n')
    
    f.write('| 月总饮水量 | 日均饮水量 |'+'\n'+'| :----: | :----: |'+'\n'+'| '+str(monthAll)+' | '+str(int(monthAll/monthCount))+' |'+'\n'+'</div>'+'\n\n')
    f.close
    
    
    
    for date in date_list:
        if date in data['data']:
            # 删除messageID
            del data['data'][date]['messageId']
            f.write('\n| 日期 |')
            #每一日期的时间和毫升
            for timeee,ml in data['data'][date].items():
                f.write(' '+timeee+' |')
            f.write('\n'+'| :----: |')
            for timeee,ml in data['data'][date].items():
                f.write(' :----: |')
            f.write('\n'+'| '+date+' |')
            for timeee,ml in data['data'][date].items():
                f.write(' '+str(ml)+' |')
            f.write('\n\n')
    f.close

data=get_json_data("data.json")
f = open('README.md', 'w+',encoding='utf-8')

if time.strftime("%Y-%m-%d", time.localtime()) in data['data']:
    times=[]
    waters=[]
    waterSum=0
    hour=-1
    p=-1
    f.write('# 今日饮水数据\n\n')
    del data['data'][time.strftime("%Y-%m-%d", time.localtime())]['messageId']
    waterall=data['data'][time.strftime("%Y-%m-%d", time.localtime())]['all']
    del data['data'][time.strftime("%Y-%m-%d", time.localtime())]['all']
    for timee,ml in data['data'][time.strftime("%Y-%m-%d", time.localtime())].items():
        if hour != int(time.strftime('%H', time.strptime(timee,"%H:%M:%S"))):
            hour = int(time.strftime('%H', time.strptime(timee,"%H:%M:%S")))
            times.append(str(hour))
            waters.append(0)
            waterSum = 0
            p+=1
        waterSum += ml
        waters[p]=waterSum
    if p<12:
        for i in range(1,12-p):
            if hour+i>=24:
                hhh=hour+i-24
            else:
                hhh=hour+i
            times.append(str(hhh))
            waters.append(0)
        
    plt.style.use('seaborn-muted')
    fig, ax = plt.subplots(figsize=(18, 6),dpi=200)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.bar(times, waters,width=0.45)
    # 设置字体
    font = {'family': 'serif', 'color': '#999999'}
    plt.xlabel('time',fontdict=font)
    plt.ylabel('ml',fontdict=font)
    for a, b in zip(times, waters):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom',fontdict=font)

    # 设置坐标轴颜色
    ax = plt.gca()  # 获取当前坐标轴
    ax.spines['bottom'].set_color('#999999')  # 设置底边框颜色
    ax.spines['left'].set_color('#999999')  # 设置左边框颜色
    ax.tick_params(axis='both', colors='#999999')  # 设置刻度颜色
    fig.tight_layout()
    plt.savefig('today.png',transparent=True)
    f.write('<div align=center>'+'\n'+'<img src="today.png" style="zoom: 100%;" />'+'\n\n')
    
    f.write('| 今日总饮水量 | 每小时平均饮水量 |'+'\n'+'| :----: | :----: |'+'\n'+'| '+str(waterall)+' | '+str(int(waterall/(p+1)))+' |'+'\n'+'</div>'+'\n\n')
    
    data=get_json_data("data.json")
    del data['data'][time.strftime("%Y-%m-%d", time.localtime())]['messageId']
    del data['data'][time.strftime("%Y-%m-%d", time.localtime())]['all']
    f.write('| 日期 |')
    #每一日期的时间和毫升
    for timee,ml in data['data'][time.strftime("%Y-%m-%d", time.localtime())].items():
        f.write(' '+timee+' |')
    f.write('\n'+'| :----: |')
    for timee,ml in data['data'][time.strftime("%Y-%m-%d", time.localtime())].items():
        f.write(' :----: |')
    f.write('\n'+'| '+time.strftime("%Y-%m-%d", time.localtime())+' |')
    for timee,ml in data['data'][time.strftime("%Y-%m-%d", time.localtime())].items():
        f.write(' '+str(ml)+' |')
    f.write('\n\n')
        
data=get_json_data("data.json")
f.write('# 近30日饮水数据\n\n')
if time.strftime("%Y-%m-%d", time.localtime()) in data['data']:
    del data['data'][time.strftime("%Y-%m-%d", time.localtime())]
dateList=[]
mlList=[]
monthAll=0
monthCount=0
now = datetime.datetime.now()
for x in range(30,0,-1):
    delta = datetime.timedelta(days=-x)
    n_days = now + delta
    date=n_days.strftime('%Y-%m-%d')
    if date in data['data']:
        dateList.append(time.strftime('%m-%d', time.strptime(date,"%Y-%m-%d")))
        mlList.append(data['data'][date]['all'])
        monthAll += int(data['data'][date]['all'])
        monthCount += 1
plt.style.use('seaborn-muted')
fig, ax = plt.subplots(figsize=(18, 6),dpi=200)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.bar(dateList, mlList,width=0.45)
plt.axhline(y=2000, linestyle='--', color='red')
font = {'family': 'serif', 'color': '#999999'}
plt.xlabel('time',fontdict=font)
plt.ylabel('ml',fontdict=font)
for a, b in zip(dateList, mlList):
    plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom',fontdict=font)

# 设置坐标轴颜色
ax = plt.gca()  # 获取当前坐标轴
ax.spines['bottom'].set_color('#999999')  # 设置底边框颜色
ax.spines['left'].set_color('#999999')  # 设置左边框颜色
ax.tick_params(axis='both', colors='#999999')  # 设置刻度颜色
fig.tight_layout()
plt.savefig('30.png',transparent=True)
f.write('<div align=center>'+'\n'+'<img src="30.png"style="zoom: 100%;" />'+'\n\n')
f.write('| 总饮水量 | 日均饮水量 |'+'\n'+'| :----: | :----: |'+'\n'+'| '+str(monthAll)+' | '+str(int(monthAll/monthCount))+' |'+'\n'+'</div>'+'\n\n')

if days >= 30:
    i=0
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
else:
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
