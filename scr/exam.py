#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/5/22 19:33
import re
import time
import random
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import config

# 存储所有label=green的值 ，包括选择题会出现两个一样的
anslist=[]

# 题号
def wait():
    minn=float(config.cf.get('DATABASE','wtmin'))
    maxn=float(config.cf.get('DATABASE','wtmax'))
    time.sleep(random.uniform(minn,maxn))
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
        self.testlist=[]
        self.auto_fill_answer=None
        self.is_close_answerwindow=None
        self.is_auto_submit=None
    def start_exam(self):
        self.driver.get(self.target_url)
        # 这里必须是timesleep? 因为他本来就有但是没有弹出来
        try:
            # 第一种登录方法 正常情况
            time.sleep(3)
            self.driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div/div/div[1]/i').click()

            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath('//*[@id="pageLayout"]/div/div[2]/div/div/div/button').click()
        except:
            # 第二种登录方法 非正常情况
            # 没有点击确认按钮，直接就进入了考试
            pass
        return
    def get_answer(self):

        anslist.clear()

        self.driver.switch_to.window(self.driver.window_handles[0])
        ele=WebDriverWait(self.driver,1000).until(ec.presence_of_element_located((By.TAG_NAME,'iframe')))
        url=ele.get_attribute('src')
        exercise = 'exerciseId=\d+&'
        sign = r'sign=\d*\w*&'
        exercise = re.findall(exercise, url)[0]
        sign = re.findall(sign, url)[0]
        sid = 'studentId='+self.studentid
        url = 'https://uexercise.unipus.cn/itest/t/clsExam/rate/detail?%s%s%s' % (exercise, sign, sid)

        js = 'window.open("https://baidu.com");'
        self.driver.execute_script(js)
        print('正在获取答案页面，请等待')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)
        time.sleep(2)
        html = self.driver.page_source
        temp = self.driver.find_elements_by_class_name('green')
        for i in temp:
            # 选择题读入和选词填空题读入都是一句话，其余的是一个单词|短语
            anslist.append((i.text).replace('(', '').replace(')', '').strip())
        # 判断是否关闭答案窗口
        if self.is_close_answerwindow=='1':
            self.driver.close()

        soup=BeautifulSoup(html,'lxml')
        self.testlist=soup.find_all(name='div',attrs={'class','Test'})

        print('答案获取成功')

        return 0
    def solve(self):

        self.driver.switch_to.window(self.driver.window_handles[0])
        try:
            self.driver.switch_to.frame('iframe')
        except:
            pass

        # 有的还有个加载成功弹窗
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_id('success-ok').click()
        except:
            pass

        # 得到所有题目的种类
        itest_section = self.driver.find_elements_by_class_name('itest-section')

        # 答案的位置，输入框的位置
        ansnum=-1
        for i,section in enumerate(itest_section):
            text=section.get_attribute('part1')
            #print(text)
            flag = check(text)
            if flag == 1:
                ansnum=self.multiple_choices(i,section,ansnum)
            elif flag == 2:
                ansnum=self.multiple_selection(i,section,ansnum)
            elif flag == 3:
                ansnum=self.chun_tiankong(i,section,ansnum)
            elif flag ==4:
                ansnum=self.xuanci_tiankong(i,section,ansnum)
        self.submint()
    def chun_tiankong(self,th,section,ansnum):
        '''
            纯填空题
        :param section:第几部分
        :param ansnum: 到第几个答案
        :return: ansnum
        '''
        # 这个部分下所有的大题
        question_set=section.find_elements_by_class_name('itest-ques-set')
        for i,wordlist in enumerate(question_set):
            # 得到每个大题需要填的空
            need_input_list=(question_set[i]).find_elements_by_tag_name('input')
            for j in range(0,len(need_input_list)):
                wait()
                ansnum+=1
                self.driver.execute_script("arguments[0].value=arguments[1]", need_input_list[j],anslist[ansnum])
        return ansnum
    def xuanci_tiankong(self,th,section,ansnum):
        '''
            选词填空题
        :param section:第几部分
        :param ansnum: 到第几个答案
        :return: ansnum
        '''

        # 因为wordlist这是在答案页面存的所以有个th来找这是第几个section里面的，然后再找wordlist...其他的th没用懒得删了
        # 虽然感觉可以写简单
        wordlist_tot=self.testlist[th].select("div [class='Question-Conversation'] ul")
        # 这个部分下所有的大题
        question_set=section.find_elements_by_class_name('itest-ques-set')
        dic={}
        for i,wordlist in enumerate(wordlist_tot):
            # 找对应关系
            al=wordlist.find_all(name='li')
            for word in al:
                dic[word.text[4:]]=word.text[0]

            # 得到每个大题需要填的空
            need_input_list=(question_set[i]).find_elements_by_tag_name('input')
            for j in range(0,len(need_input_list)):
                wait()
                ansnum+=1
                self.driver.execute_script("arguments[0].value=arguments[1]", need_input_list[j],dic[anslist[ansnum]])
        return ansnum
    def multiple_choices(self,th,section,ansnum):
        '''
            单选题
        :param section:
        :return:ansnum
        '''
        global jishuqi

        question_set = section.find_elements_by_class_name('itest-ques-set')
        for i, wordlist in enumerate(question_set):
            # 得到每个大题需要填的空|选择题的空是一般题的四倍

            need_input_list = (question_set[i]).find_elements_by_tag_name('input')
            l=len(need_input_list)
            for j in range(0, int(l/4)):
                wait()
                ansnum += 2
                qoo=need_input_list[j*4].get_attribute('qoo').replace('[','').replace(']','').replace(',','')
                # qoo是随机打乱序列 qoo[原pos]=现pos 现在先用循环写着，以后再优化
                for step,k in enumerate(qoo):
                    if eval(k)==(ord(anslist[ansnum][0])-ord('A')):
                        (need_input_list[j*4+step]).click()
                        break
        return ansnum
    def multiple_selection(self,th,section,ansnum):
        '''
        多选题
        :param section:
        :return:
        '''
        return ansnum
    def submint(self,):
        # 前面已经进入了iframe里面就不需要再进了
        # 不同course button不同，以后再改吧
        if self.is_auto_submit=='1':
            self. driver.find_element_by_xpath('//*[@id="submit-answer"]').click()
            # self.driver.quit()
        print('答题完成,请提交')
def check(text):
    '''
        判断这个部分的类型 单选|多选|填空
    :param text:
    :return:
    '''
    danxuan=['短对话','仔细阅读','长对话','短文理解','新闻报道']
    duoxuan=['']
    chun_tiankong=['听写填空','复合式听写','长篇阅读']
    xuanci_tiankong=['词汇理解']
    if text in danxuan:
        return 1
    elif text in duoxuan:
        return 2
    elif text in chun_tiankong:
        return 3
    elif text in xuanci_tiankong:
        return 4