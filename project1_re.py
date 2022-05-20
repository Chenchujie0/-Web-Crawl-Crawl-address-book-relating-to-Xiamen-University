import re
def main():
    text = input()

    #先找到包含“厦门”两个字的隶属单位
    pattern1 = r"([\u4e00-\u9fa5]*)([\u53a6\u95e8])([\u4e00-\u9fa5]*)([0-9]*)([\u4e00-\u9fa5]*)"

    #只要字符串中的某个字串符合正则表达式即可
    res = re.search(pattern1, text)
    if res != None:
        res1 = res.group()
        print(res1)

    #电话号码格式：（+86）*(-)* xxxx[-|\s]xxxxxxx,（+86）*(-)* xxx[-|\s]xxxxxxxx, （+86）*(-)* xxx[-|\s]xxxx[-|\s]xxxx, [:|：|,|\s]xxxxxxx
    pattern = re.compile(r"(((([\u4e00-\u9fa5]*)(\s*))([\u4e00-\u9fa5])(:|：))((((([0-9]*[0-9]*)(-*))(((\d{4})(-|\s)(\d{7}))|((\d{3})(-|\s)(\d{8}))|((\d{3})(-|\s)(\d{4})(-|\s)(\d{4})))))|(((:|：|,|，)(\d{7}))((((\s)*,|，)*(\d{7})*)*))))")

    lst = re.findall(pattern, text)

    reslst = []
    for item in lst:
        reslst.append(item[0])

    for item in reslst:
        print(item)

if __name__ == '__main__':
    main()

"""
"联系电话：0592-2580168 / 传 真：0592-2580258 / 电子邮箱： cogsci@xmu.edu.cn Copyright © 2020 厦门大学人工智能系 | All Rights Reserved” “厦大总机：0592-2180000 地址：福建省厦门市思明区思明南路 422 号 邮政编 码：361005 闽 ICP 备 05005471 号 闽公网安备 35020302001480 号” “版权所有：厦门大学科技处 福建省厦门市厦门大学颂恩楼（嘉庚主楼 11 层） 邮政编码：361005 传真:2180407 E-Mail:std@xmu.edu.cn 综合事务:2185815，2187957 / 纵向事务:2181680，2184033 ,2180583/ 横向事 务:2185633 / 平台成果事务:2183408 / 专项事务:2184282"
"""