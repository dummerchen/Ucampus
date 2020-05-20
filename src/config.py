#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/5/20 8:52
import configparser
import os

cf = configparser.ConfigParser()
path=os.path.abspath('..')+'\config.ini'
cf.read(path)
def change_config():
    opt=cf.options('DATABASE')

    for i,name in enumerate(opt):
        print(i,'---->\n','当前配置名称为%s\n'%name,'是',cf.get('DATABASE',name))
    while 1:
        num=input('请输入要更改的配置文件序号|return退出')
        new=input('输入新的该文件')
        try:
            cf.set('DATABASE',opt[num],new)
        except:
            break
        if num=='return':
            break
    cf.write(open(path,'w'))

def get_config():

    if cf.has_option('DATABASE','username')==False:
        username = input('缺失账号，请输入账号\n')
        cf.set('DATABASE','username',username)
    if cf.has_option('DATABASE','password')==False:
        password = input('缺失密码，请输入密码\n')
        cf.set('DATABASE','password',password)
    if cf.has_option('DATABASE','studentid')==False:
        studentid = input('确实sid，请输入sid\n')
        cf.set('DATABASE','studentid',studentid)
    cf.write(open(path, 'w'))
    l=[]
    for i in cf.options('DATABASE'):
        l.append(cf.get('DATABASE', i))
    return l
if __name__ == '__main__':
    get_config()
    change_config()