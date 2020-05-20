#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/5/19 18:25


# some courses-> many units-> many tests
import time
import re
import os
from selenium import webdriver
import config

allhandles = []


class Test(object):
    def __init__(self):
        self.username=''
        self.password=''
        self.studentid=''
        self.target_url=''
        self.driver=None
        # 新视野是sign+exerciseid+studentid
        # 但是四六级不需要sid也可以
        # studentid在个人中心页面
        self.answerlist=[]
        self.is_close_answerwindow=None
        self.is_auto_submit=None
    def start_exam(self):
        self.driver.get(self.target_url)
        # 这里必须是timesleep 因为他本来就有但是没有弹出来
        time.sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div/div/div[1]/i').click()

        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('//*[@id="pageLayout"]/div/div[2]/div/div/div/button').click()


    def get_answer(self):

        url=self.driver.find_element_by_tag_name('iframe').get_attribute('src')

        exercise = 'exerciseId=\d+&'
        sign = r'sign=\d*\w*&'
        exercise = re.findall(exercise, url)[0]
        sign = re.findall(sign, url)[0]
        sid = 'studentId='+self.studentid
        url = 'https://uexercise.unipus.cn/itest/t/clsExam/rate/detail?%s%s%s' % (exercise, sign, sid)
        self.driver.switch_to.window(allhandles[1])
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        temp=self.driver.find_elements_by_class_name('green')
        for i in temp:
            self.answerlist.append((i.text).replace('(', '').replace(')', ''))

        # 判断是否关闭答案窗口|似乎必须要关闭窗口才可以提交
        if self.is_close_answerwindow:
            self.driver.close()
        self.driver.switch_to.window(allhandles[0])
        return
    def solve(self):
        self.driver.switch_to.window(allhandles[0])
        self.driver.switch_to.frame('iframe')

        # 有的还有个加载成功弹窗
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_id('success-ok').click()
        except:
            pass
        self.driver.implicitly_wait(5)
        # time.sleep(1)
        section = self.driver.find_elements_by_class_name('itest-section')
        for i in section:
            text = i.get_attribute('part1')

            #print(text)
            flag = check(text)
            if flag == 1:
                self.multiple_choices(i)
            elif flag == 2:
                self.multiple_selection(i)
            elif flag == 3:
                self.fill_blanks(i)
        self.submint()
    def fill_blanks(self,section):
        '''
            填空题
        :param section: 一个部分的所有题目
        :return:
        '''
        questionlist = section.find_elements_by_tag_name('input')
        #print(len(self.answerlist),len(questionlist))
        for i, question in enumerate(questionlist):
            self.driver.implicitly_wait(4)
            self.driver.execute_script("arguments[0].value=arguments[1]", questionlist[i], self. answerlist[i])
            #print(self. answerlist[i])
    def multiple_choices(self,section):
        '''
            单选题
        :param section:
        :return:
        '''
        pass
    def multiple_selection(self,section):
        '''
        多选题
        :param section:
        :return:
        '''
        pass
    def submint(self,):
        # 前面已经进入了iframe里面就不需要再进了
        # 不同course button不同，以后再改吧
        if self.is_auto_submit==1:
            self. driver.find_element_by_xpath('//*[@id="submit-answer"]').click()
            self.driver.find_elements_by_class_name('layui-layer-btn0').click()
#test=[Test() for i in range(10000)]
def check(text):
    '''
        判断这个部分的类型 单选|多选|填空
    :param text:
    :return:
    '''
    # 单选只用点input就行了
    danxuan=['短对话','仔细阅读','长对话',]
    # ctrl+click
    duoxuan=['']
    # 改变input 的value
    tiankong=['复合式听写','词汇理解','长篇阅读']
    if text in danxuan:
        return 1
    elif text in duoxuan:
        return 2
    elif text in tiankong:
        return 3
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
    driver.find_element_by_class_name('layui-layer-btn0').click()
    handles = driver.window_handles
    for i in handles:
        allhandles.append(i)
    driver.switch_to.window(allhandles[0])
    return driver

test=Test()

def main():
    #target_url = 'https://ucontent.unipus.cn/_pc_default/pc.html?cid=215103#/course-v1:Unipus+nhce_3_vls_2+2018_03/courseware/u1/u1g65/u1g66/u1g67/p_1'
    print('更改用户密码建议到config.ini文件里面更改更快')
    flag=input('是否要更改密码 y|n (回车默认不更改')
    if flag=='y':
        config.change_config()
    else:
        pass
    test.is_auto_submit,test.is_close_answerwindow,test.username,test.password,test.studentid=config.get_config()
    test.target_url=input('请输入要写的试卷链接')
    driver = login()
    test.driver=driver
    test.start_exam()
    test.get_answer()
    test.solve()
if __name__=='__main__':
    main()