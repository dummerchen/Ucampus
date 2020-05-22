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

allhandles=exam.allhandles
#
# # 存储所有label=green的值 ，包括选择题会出现两个一样的
# anslist=[]
#
# class Test(object):
#     def __init__(self):
#         self.username=''
#         self.password=''
#         self.studentid=''
#         self.target_url=''
#         self.driver=None
#         # 新视野是sign+exerciseid+studentid
#         # 但是四六级不需要sid也可以
#         # studentid在个人中心页面
#         self.testlist=[]
#         self.is_close_answerwindow=None
#         self.is_auto_submit=None
#     def start_exam(self):
#         self.driver.get(self.target_url)
#         # 这里必须是timesleep? 因为他本来就有但是没有弹出来
#         try:
#             # 第一种登录方法 正常情况
#             time.sleep(3)
#             self.driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div/div/div[1]/i').click()
#
#             self.driver.implicitly_wait(10)
#             self.driver.find_element_by_xpath('//*[@id="pageLayout"]/div/div[2]/div/div/div/button').click()
#         except:
#             # 第二种登录方法 非正常情况
#             # 没有点击确认按钮，直接就进入了考试
#             pass
#         return
#     def get_answer(self):
#         try:
#             url=self.driver.find_element_by_tag_name('iframe').get_attribute('src')
#         except:
#             # 第二种登录方法
#             url=self.driver.current_url
#         exercise = 'exerciseId=\d+&'
#         sign = r'sign=\d*\w*&'
#         exercise = re.findall(exercise, url)[0]
#         sign = re.findall(sign, url)[0]
#         sid = 'studentId='+self.studentid
#         url = 'https://uexercise.unipus.cn/itest/t/clsExam/rate/detail?%s%s%s' % (exercise, sign, sid)
#
#         self.driver.switch_to.window(allhandles[1])
#         self.driver.get(url)
#         self.driver.implicitly_wait(5)
#         time.sleep(2)
#         html = self.driver.page_source
#         temp = self.driver.find_elements_by_class_name('green')
#         for i in temp:
#             # 选择题读入和选词填空题读入都是一句话，其余的是一个单词|短语
#             anslist.append((i.text).replace('(', '').replace(')', '').strip())
#         # 判断是否关闭答案窗口
#         # if self.is_close_answerwindow:
#         #     self.driver.implicitly_wait(2)
#         #     self.driver.close()
#         self.driver.switch_to.window(allhandles[0])
#
#         soup=BeautifulSoup(html,'lxml')
#         self.testlist=soup.find_all(name='div',attrs={'class','Test'})
#         print(anslist)
#         return
#     def solve(self):
#         self.driver.switch_to.window(allhandles[0])
#         try:
#             self.driver.switch_to.frame('iframe')
#         except:
#             # 第二种登录的特判
#             pass
#
#         # 有的还有个加载成功弹窗
#         try:
#             self.driver.implicitly_wait(10)
#             self.driver.find_element_by_id('success-ok').click()
#         except:
#             pass
#
#         # 得到所有题目的种类
#         self.driver.implicitly_wait(5)
#         itest_section = self.driver.find_elements_by_class_name('itest-section')
#
#         # 答案的位置，输入框的位置
#         ansnum=-1
#         for i,section in enumerate(itest_section):
#             text=section.get_attribute('part1')
#             #print(text)
#             flag = check(text)
#             if flag == 1:
#                 ansnum=self.multiple_choices(i,section,ansnum)
#             elif flag == 2:
#                 ansnum=self.multiple_selection(i,section,ansnum)
#             elif flag == 3:
#                 ansnum=self.chun_tiankong(i,section,ansnum)
#             elif flag ==4:
#                 ansnum=self.xuanci_tiankong(i,section,ansnum)
#         self.submint()
#     def chun_tiankong(self,th,section,ansnum):
#         '''
#             纯填空题
#         :param section:第几部分
#         :param ansnum: 到第几个答案
#         :return: ansnum
#         '''
#         # 这个部分下所有的大题
#         question_set=section.find_elements_by_class_name('itest-ques-set')
#         for i,wordlist in enumerate(question_set):
#             # 得到每个大题需要填的空
#             need_input_list=(question_set[i]).find_elements_by_tag_name('input')
#             for j in range(0,len(need_input_list)):
#                 ansnum+=1
#                 self.driver.implicitly_wait(4)
#                 self.driver.execute_script("arguments[0].value=arguments[1]", need_input_list[j],anslist[ansnum])
#         return ansnum
#     def xuanci_tiankong(self,th,section,ansnum):
#         '''
#             选词填空题
#         :param section:第几部分
#         :param ansnum: 到第几个答案
#         :return: ansnum
#         '''
#         # 因为wordlist这是在答案页面存的所以有个th来找这是第几个section里面的，然后再找wordlist...其他的th没用懒得删了
#         # 虽然感觉可以写简单
#         wordlist_tot=self.testlist[th].select("div [class='Question-Conversation'] ul")
#         # 这个部分下所有的大题
#         question_set=section.find_elements_by_class_name('itest-ques-set')
#         dic={}
#         for i,wordlist in enumerate(wordlist_tot):
#             # 找对应关系
#             al=wordlist.find_all(name='li')
#             for word in al:
#                 dic[word.text[4:]]=word.text[0]
#
#             print(dic)
#             # 得到每个大题需要填的空
#             need_input_list=(question_set[i]).find_elements_by_tag_name('input')
#             for j in range(0,len(need_input_list)):
#                 ansnum+=1
#                 self.driver.implicitly_wait(4)
#                 self.driver.execute_script("arguments[0].value=arguments[1]", need_input_list[j],dic[anslist[ansnum]])
#         return ansnum
#     def multiple_choices(self,th,section,ansnum):
#         '''
#             单选题
#         :param section:
#         :return:ansnum
#         '''
#         question_set = section.find_elements_by_class_name('itest-ques-set')
#         for i, wordlist in enumerate(question_set):
#             # 得到每个大题需要填的空|选择题的空是一般题的四倍
#             need_input_list = (question_set[i]).find_elements_by_tag_name('input')
#             l=len(need_input_list)
#             for j in range(0, int(l/4)):
#                 ansnum += 2
#                 qoo=need_input_list[j*4].get_attribute('qoo').replace('[','').replace(']','').replace(',','')
#                 # qoo是随机打乱序列 qoo[原pos]=现pos 现在先用循环写着，以后再优化
#                 for step,k in enumerate(qoo):
#                     if eval(k)==ord(anslist[ansnum][0])-ord('A'):
#                         self.driver.implicitly_wait(4)
#                         #print(need_input_list[j*4+step].text)
#                         (need_input_list[j*4+step]).click()
#                         break
#         return ansnum
#     def multiple_selection(self,th,section,ansnum):
#         '''
#         多选题
#         :param section:
#         :return:
#         '''
#         return ansnum
#     def submint(self,):
#         # 前面已经进入了iframe里面就不需要再进了
#         # 不同course button不同，以后再改吧
#         print(type(self.is_auto_submit))
#         if self.is_auto_submit=='1':
#             self. driver.find_element_by_xpath('//*[@id="submit-answer"]').click()
#             # self.driver.quit()
# def check(text):
#     '''
#         判断这个部分的类型 单选|多选|填空
#     :param text:
#     :return:
#     '''
#     danxuan=['短对话','仔细阅读','长对话','短文理解','新闻报道']
#     duoxuan=['']
#     chun_tiankong=['听写填空','复合式听写','长篇阅读']
#     xuanci_tiankong=['词汇理解']
#     if text in danxuan:
#         return 1
#     elif text in duoxuan:
#         return 2
#     elif text in chun_tiankong:
#         return 3
#     elif text in xuanci_tiankong:
#         return 4
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

test=exam.Test()

def main():
    print('更改用户密码建议到config.ini文件里面更改更快')
    flag=input('是否要更改密码 y|n (回车默认不更改')
    if flag=='y':
        config.change_config()
    else:
        pass
    test.is_auto_submit,test.is_close_answerwindow,test.username,test.password,test.studentid=config.get_config()
    test.target_url=input('请输入要写的试卷原始链接')
    driver = login()
    test.driver=driver
    test.start_exam()
    test.get_answer()
    test.solve()
if __name__=='__main__':
    main()