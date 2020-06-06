#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/5/19 18:25

# v 3.1.1
# some courses-> many units-> many tests
import os
import config
import exam
import time


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

    print('如果登录页面进去就闪退，检查账号密码是否错误\n如果答案页面是空白,说明sid可能错误\n（自古readme没人看，只好写这了）')
    print('-'*40)
    print('更改用户密码建议到config.ini')
    flag=input('是否要更改配置文件(config.ini) y|n (回车默认不更改')
    if flag=='y':
        config.change_config()
    else:
        pass
    test.is_auto_submit,test.is_close_answerwindow,test.username,test.password,test.studentid,test.auto_fill_answer=config.get_config()
    try:
        driver = login()
        test.driver = driver
    except:
        print('可能账号密码错误，请检查配置文件,后再重新运行程序')
        time.sleep(5)
    while 1:
        #test.start_exam()
        os.system('cls')
        flag=input('进入可答题页面后，任意输入来确认开始')
        os.system('cls')
        print('答题开始，请勿退出或切换页面')
        try:
            test.get_answer()
            if test.auto_fill_answer=='1':
                print('正在准备自动答题')
                test.solve()
            else:
                print('已选择手动答题，请手动答题时不要关闭程序')
        except:
            print('sid可能错误,请检查sid是否正确匹配(一般是7位数字)\n如果答案页面有全部答案则可以刷新再来一次或先做别的测验，软件不太稳定\n')
            time.sleep(4)

if __name__=='__main__':
    os.system('cls')
    main()