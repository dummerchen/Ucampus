#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/5/19 18:25

# v 3.1.1
# some courses-> many units-> many tests
import os
import config
import exam


def login():
    '''
        从config里面获取信息并登录
    :return: driver
    '''
    url='https://sso.unipus.cn/sso/login?service=https%3A%2F%2Fu.unipus.cn%2Fuser%2Fcomm%2Flogin%3Fschool_id%3D'
    driver=config.check_cd()
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
    print('更改用户密码建议到config.ini')
    flag=input('是否要更改config y|n (回车默认不更改')
    if flag=='y':
        config.change_config()
    else:
        pass
    test.is_auto_submit,test.is_close_answerwindow,test.username,test.password,test.studentid=config.get_config()
    driver = login()

    test.driver=driver
    while 1:
        #test.start_exam()
        flag=input('进入可答题页面后，任意输入来确认开始')
        os.system('cls')
        print('答题开始，请勿退出或切换页面')
        test.get_answer()
        test.solve()
if __name__=='__main__':
    os.system('cls')
    main()