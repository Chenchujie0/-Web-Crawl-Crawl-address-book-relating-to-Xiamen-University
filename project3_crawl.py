import re
import requests
import urllib3
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout, ConnectionError, RequestException
from pybloom_live import BloomFilter
import os
import psutil

# 使用requests访问https时会有SSL验证，需要在get方法时关闭验证，同时会显示警告
# 访问页面：获取指定页面中含有的url
class find():
    url = ""
    depth = 0
    visited = [] # 已经访问过（爬取过）的url。访问：即get该页面并取出该页面上的所有url
    unvisited = [] # 已经取出的、但是还没有访问的/等待访问的url
    url_count = 0 # 已经访问过的url数量
    END_COUNT = 3000 # 总共需要访问的url数量
    end_flag = False # 标志是否该结束了（url_count >= END_COUNT）
    alist = [] #存放所有爬取到的页面
    def __init__(self, _url):
        self.url = _url

    def visit(self): 
        if(self.url not in self.visited):
            self.visited.append(self.url) # 将该链接置为访问过
            try:
                req = requests.get(self.url, verify=False, timeout=5) # verify参数：关闭SSL验证
            except ReadTimeout: # 超时异常
                print('Timeout: ', self.url)
                ## 需要把当前的 url 放到任务中，过一段时间再尝试连接
            except ConnectionError: # 连接异常
                print('Connection error: ', self.url)
            except RequestException: # 请求异常
                print('Error: ', self.url)
            else:
                if req.status_code == 404:
                    print('404页面不存在: ', self.url)
                    ## 把当前的 url 从爬虫任务中删除掉
                if req.status_code == 403:
                    print('403页面禁止访问: ', self.url)
                    ## ... 
                if req.status_code == 200:

                    # 如果正确访问，count+1；判断是否结束
                    # global url_count
                    # global end_flag
                    self.url_count += 1
                    if self.url_count >= self.END_COUNT:
                        self.end_flag = True

                    # print("\t"*depth, "#%d-%d %s"%(depth, url_count, url))
                    self.alist.append(self.url)

                    PATTERN_URl = "<a.*href=\"(https?://.*?)[\"|\'].*"
                    self.ulist = re.findall(PATTERN_URl, req.text)
                    self.ulist = [self.url for self.url in self.ulist if self.url.find(".pdf") == -1 ]
                    # 为了防止下载pdf文件，特意跳过了：只保留没有".pdf"后缀的url

                    return self.ulist
            return None
        return None

    def bfs(self):
        urllib3.disable_warnings() # 用该行代码消除警告
        # global unvisited
        self.unvisited.append([self.url, self.depth])

        while(self.unvisited): # unvisited每个元素是[url, depth]
            [self.url, self.depth] = self.unvisited.pop(0)

            # 只访问1、2层
            if self.end_flag or self.depth >= 3:
                break

            self.ulist = self.visit()
            if self.ulist:
                self.ulist = list(set(self.ulist)-set(self.visited))

                self.depth += 1 # ulist中的url都是当前url的孩子，所以深度加一
                self.unvisited = self.unvisited + [[self.url, self.depth] for self.url in self.ulist]

def re_find(text):
    pattern1 = r"((([\u4e00-\u9fa5]*|[a-zA-Z]*)(©|&copy;)([0-9]*)(([a-zA-Z]*\s*)*|[\u4e00-\u9fa5]*))|(([\u4e00-\u9fa5]*)(\s*)(厦门大学)([\u4e00-\u9fa5]*)))"

    #只要字符串中的某个字串符合正则表达式即可
    place = re.findall(pattern1, text)
    if place == None:
        pass

    for i in range(len(place)):
        place[i] = place[i][0]

    for item in place:
        if "中国" in item or "关" in item or "电" in item:
            place.remove(item)
        if "&copy" in item:
            place.remove(item)
            item = list(item.split('&'))[0]
            place.append(item)
        # if "版权" in item:
        #     place.remove(item)
        #     item = list(item.split('版'))[0]
        #     place.append(item)

    for item in place:
        if "厦门" not in item:
            place.remove(item)
     
    #电话号码格式：（+86）*(-)* xxxx[-|\s]xxxxxxx,（+86）*(-)* xxx[-|\s]xxxxxxxx, （+86）*(-)* xxx[-|\s]xxxx[-|\s]xxxx, [:|：|,|\s]xxxxxxx
    pattern = re.compile(r"(((([\u4e00-\u9fa5]*|(^QQ)[a-zA-Z]*)\s*)([\u4e00-\u9fa5]|(^QQ)[a-zA-Z])(:|：)\s*)((((([0-9]*[0-9]*)(-*))((\d{4}(-|\s)\d{7})|(\d{3}(-|\s)\d{8})|(\d{3}(-|\s)\d{4}(-|\s)\d{4}))))|(\d{7}(((\s*,)|，)*\d{7})*)))")

    phone = re.findall(pattern, text)
    if len(phone) == 0:
        return None

    # if len(place) != 0:
    #     print(place[0])

    for i in range(len(phone)):
        phone[i] = phone[i][0]
        # print(phone[i])
    
    for item in phone:
        if "邮箱" in item:
            phone.remove(item)
        if len(item) < 7:
            phone.remove(item)

    if len(place) != 0:
        return place[0], phone
    else:
        return phone

class BF:
    def __init__(self):
        self.blm = BloomFilter(capacity = 10000000)

    def add(self, text):
        self.blm.add(text)

def main():
    global visited_url
    # visited_url = BF()
    url = "https://informatics.xmu.edu.cn"
    st_find = find(url)
    st_find.bfs()
    all_url = list(set(st_find.alist))

    # tags = ['li', 'p', 'div', 'span', 'address']
    for iurl in all_url: #改url
        try:
            response = requests.get(iurl) #改url
            response.encoding = response.apparent_encoding  # 指定编码等于原始页面编码
            soup = BeautifulSoup(response.text, 'lxml') 

        except Exception as e:
            print(e)

        bf = BF()
        content = []
            # for i in range(len(tags)):
            #     tag = tags[i]
            #     tag_all = soup.find_all(tag)

            #     for j in range(len(tag_all)):
            #         temp = re_find(str(tag_all[j]))
            #         if temp != None:
            #             if temp not in bf.blm:
            #                 bf.add(temp)
            #                 content.append(temp)

        tag_all = soup.find_all("div")

        for j in range(len(tag_all)):
            result = re_find(str(tag_all[j]))
            if result != None:
                if len(result) == 2:
                    place = result[0]
                    phone = result[1]
                    if "关" in place or "于" in place:
                        place = "Unkonwn"
                    if "电话" in place:
                        continue
                    for item in phone:
                        if len(item) < 7 or "群" in item:
                            continue
                        if item not in bf.blm:
                            bf.add(item)
                            temp = [place, item]
                            print(temp)
                            content.append(temp)
                if len(result) == 1:
                    phone = result
                    for item in phone:
                        if item not in bf.blm:
                            bf.add(item)
                            temp = ["Unknown", item]
                            print(temp)
                            content.append(temp)
    

if __name__ == "__main__":
    main()
