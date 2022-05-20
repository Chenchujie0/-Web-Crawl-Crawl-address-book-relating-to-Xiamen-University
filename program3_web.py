import re
import requests
from requests.exceptions import ReadTimeout, ConnectionError, RequestException
import urllib3
# 使用requests访问https时会有SSL验证，需要在get方法时关闭验证，同时会显示警告

# 访问页面：获取指定页面中含有的url

class find():
    url = ""
    depth = 0
    visited = [] # 已经访问过（爬取过）的url。访问：即get该页面并取出该页面上的所有url
    unvisited = [] # 已经取出的、但是还没有访问的/等待访问的url
    url_count = 0 # 已经访问过的url数量
    END_COUNT = 50 # 总共需要访问的url数量
    end_flag = False # 标志是否该结束了（url_count >= END_COUNT）
    alist = [] #存放所有爬取到的页面
    def __init__(self, _url):
        self.url = _url

    def visit(self): 
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
                url_count += 1
                if url_count >= self.END_COUNT:
                    self.end_flag = True

                # print("\t"*depth, "#%d-%d %s"%(depth, url_count, url))
                self.alist.append(self.url)

                PATTERN_URl = "<a.*href=\"(https?://.*?)[\"|\'].*"
                self.ulist = re.findall(PATTERN_URl, req.text)
                self.ulist = [self.url for self.url in self.ulist if self.url.find(".pdf") == -1 ]
                # 为了防止下载pdf文件，特意跳过了：只保留没有".pdf"后缀的url

                return self.ulist
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

            self.ulist = self.visit(self)
            if self.ulist:
                self.ulist = list(set(self.ulist)-set(self.visited))

                self.depth += 1 # ulist中的url都是当前url的孩子，所以深度加一
                self.unvisited = self.unvisited + [[self.url, self.depth] for self.url in self.ulist]




# def dfs(url, depth=1):
#     ulist = visit(url, depth)
#     if ulist:
#         ulist = list(set(ulist)-set(visited)) # ulist是局部变量，指的是一个节点的所有子节点
#         for url in ulist:
#             if depth<3 and not end_flag: # 只访问1、2、3层（根节点是第0层）
#                 dfs(url, depth+1)


# if __name__ == '__main__':
    # start_url = "http://www.xmu.edu.cn/"
    # strategy = input("输入dfs/bfs：")
    # if strategy == "dfs":
    #     print("\t"*0, "#%d %s"%(0, start_url))
    #     dfs(start_url)
    # elif strategy == "bfs":
    # bfs(start_url)
    # print(alist)
    # else:
    #     print("输入格式有误，请重新输入")

