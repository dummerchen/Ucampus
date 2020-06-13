#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/5/20 8:52
import configparser
import os
import re
from selenium import webdriver
cf = configparser.ConfigParser()
path=os.path.abspath('..')
cf.read(path+'/config.ini')
def change_config():
    opt=cf.options('DATABASE')

    for i,name in enumerate(opt):
        print(i,'---->\n','当前配置名称为%s\n'%name,'是',cf.get('DATABASE',name))
    while 1:
        num=input('请输入要更改的配置文件序号|return退出')
        if num=='return':
            break
        new = input('输入新的该文件')
        try:
            cf.set('DATABASE',opt[int(num)],new)
        except:
            print('出错了！')
            break
    cf.write(open(path+'/config.ini','w'))
def check_cd():
    if cf.get('DATABASE','v_chromedriver')=='':
        for num in range(80,84):
            try:
                pathcd=path+'/chromedriver/chromedriver_%s.exe'%(num)
                # 如果有配置环境变量可以把这个改为
                #driver=webdriver.Chrome()
                driver = webdriver.Chrome(pathcd)

                cf.set('DATABASE','v_chromedriver',str(num))
                cf.write(open(path + '/config.ini', 'w'))
                return driver
            except:
                pass
    else:
        pathcd = path + '/chromedriver/chromedriver_%s.exe' %cf.get('DATABASE','v_chromedriver')
        # 这里也要改
        #driver = webdriver.Chrome()
        driver = webdriver.Chrome(pathcd)
        return driver
    print('请确认支持的版本或手动配置chrome相应的chromedriver版本到chromedriver文件夹')

def get_sid(driver):
    text=driver.page_source
    studentid = re.findall('sid:\d+',text)[0].replace('sid:','')
    cf.set('DATABASE','studentid',str(studentid))
    cf.write(open(path + '/config.ini', 'w'))
    return studentid
def get_config():

    if cf.get('DATABASE','username')=='':
        username = input('缺失账号，请输入账号\n')
        cf.set('DATABASE','username',username)
    if cf.get('DATABASE','password')=='':
        password = input('缺失密码，请输入密码\n')
        cf.set('DATABASE','password',password)

    cf.write(open(path+'/config.ini', 'w'))
    l=[]
    for i in cf.options('DATABASE'):
        l.append(cf.get('DATABASE', i))
    return l[:6]
if __name__ == '__main__':
    l=get_config()
    print(l)
    check_cd()