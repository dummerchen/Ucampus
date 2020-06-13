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

    print('如果答案页面是空白，请截图config.ini文件内容+测试链接 反馈bug\n（自古readme没人看，只好写这了）')
    print('更改用户密码建议到config.ini')
    print('-' * 40)
    flag=input('是否要更改配置文件(config.ini) y|n (回车默认不更改')
    if flag=='y':
        config.change_config()

    test.is_auto_submit,test.is_close_answerwindow,test.username,test.password,test.studentid,test.auto_fill_answer=config.get_config()
    try:
        driver = login()
        test.driver = driver
        if test.studentid=='':
            try:
                test.studentid=config.get_sid(driver)
            except:
                print('未找到形如sid:XXX,请手动配置或者因u版本已更新本软件已经不支持，欢迎反馈')
                time.sleep(4)
                return
    except:
        print('可能账号密码错误，请检查配置文件,后再重新运行程序')
        time.sleep(5)
        return
    while 1:

        os.system('cls')
        flag=input('进入可答题页面后，任意输入来确认开始')
        os.system('cls')
        print('答题完成后建议人工检查一下，如有未完成的题建议刷新再尝试一次不要提交因为答案乱序了！（软件不太稳定,第二次基本能全部答完）')
        print('答题开始，请勿退出或滑动页面')
        try:
            test.get_answer()
            if test.auto_fill_answer=='1':
                print('正在准备自动答题')
                test.solve()
                print('答题完成,请提交')
                time.sleep(3)
            else:
                print('已选择手动答题，请手动答题时不要关闭程序')
        except:
            print('出错了，如果自动答题未答全可以刷新再来一次或手动答题(软件不太稳定\n')
            time.sleep(4)

if __name__=='__main__':
    os.system('cls')
    main()