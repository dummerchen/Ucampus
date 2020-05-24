#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/5/19 18:25


# some courses-> many units-> many tests
import time
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import config
import exam

# 现在可以重复多次获得答案了只需要改url了
def login():
    '''
        从config里面获取信息并登录
    :return: driver
    '''
    url='https://sso.unipus.cn/sso/login?service=https%3A%2F%2Fu.unipus.cn%2Fuser%2Fcomm%2Flogin%3Fschool_id%3D'
    driver=webdriver.Chrome()
    driver.get(url)

    driver.find_element_by_name('username').send_keys(test.username)
    driver.find_element_by_name('password').send_keys(test.password)
    driver.find_element_by_id('login').click()

    driver.implicitly_wait(3)
    try:
        driver.find_element_by_class_name('layui-layer-btn0').click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    except:
        pass
    driver.switch_to.window(driver.window_handles[0])
    return driver

test=exam.Test()

def main():
    print('更改用户密码建议到config.ini文件里面更改')
    flag=input('是否要更改config y|n (回车默认不更改')
    if flag=='y':
        config.change_config()
    else:
        pass
    test.is_auto_submit,test.is_close_answerwindow,test.username,test.password,test.studentid=config.get_config()
    #test.target_url=input('请输入要写的试卷原始链接')
    driver = login()

    test.driver=driver
    while 1:
        #test.start_exam()
        flag=input('任意输入来确认开始')
        os.system('cls')
        print('答题开始，请勿退出或切换页面')
        test.get_answer()
        test.solve()
if __name__=='__main__':
    main()