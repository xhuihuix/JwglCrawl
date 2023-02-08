import datetime
import os
import sys

import requests
from PIL import Image  # 导入PIL库
from urllib import parse
from lxml import etree
from re import search
from io import BytesIO


class JwglCrawl:
    guanwangUrl = "https://sis.ustb.edu.cn"
    tokenUrl = "https://jwgl.ustb.edu.cn/glht/Logon.do?method=randToken"
    retUrl = "https://jwgl.ustb.edu.cn/glht/Logon.do?method=weCharLogin"
    qrcodeUrl = ""
    termUrl = "https://jwgl.ustb.edu.cn/kscj/cjcx_query"
    acadProgUrl = "https://jwgl.ustb.edu.cn/pyfa/toxywcqk"
    # 每学期成绩url
    grage_url = "https://jwgl.ustb.edu.cn/kscj/cjcx_list"

    appid = ""
    rand_token = ""
    sid = ""
    Term_data = []

    def __init__(self):
        self.session = requests.session()

    def getQrCodeUrl(self):
        api_url = self.guanwangUrl + "/connect/qrpage"

        return_url = "https://jwgl.ustb.edu.cn/glht/Logon.do?method=weCharLogin"
        sid_pattern = r'sid = "(.*?)",'

        token_data = {
            "method": "randToken"
        }

        res = self.session.post(self.tokenUrl, data=token_data)
        token_json = res.json()

        qrcode_html_url = api_url + "?appid=" + token_json["appid"] + "&return_url=" + parse.quote(
            return_url) + "&rand_token=" + token_json["rand_token"] + "&embed_flag=1"
        res = self.session.get(qrcode_html_url)
        html = etree.HTML(res.text)

        self.qrcodeUrl = self.guanwangUrl + html.xpath("//div[@class=\"mains_mb\"]/img/@src")[0]

        self.sid = search(sid_pattern, res.text).group(1)
        self.appid = token_json["appid"]
        self.rand_token = token_json["rand_token"]
        return True

    def login(self, show_image=True):
        if not self.getQrCodeUrl():
            print("获取二维码出现问题")
            return False

        if show_image:
            response = self.session.get(self.qrcodeUrl)
            image = Image.open(BytesIO(response.content))
            image.show()  # 展示

        linkStr = "&"
        state_url = self.guanwangUrl + "/connect/state"

        data_sid = {
            "sid": self.sid
        }

        res = self.session.get(state_url, params=data_sid, timeout=60)
        res_data = res.json()
        if res_data['state'] == 102:
            print("微信二维码已扫码")
        while True:
            res = self.session.get(state_url, params=data_sid, timeout=60)
            res_data = res.json()
            index_url = self.retUrl + linkStr + "appid=" + self.appid + "&auth_code=" + res_data[
                "data"] + "&rand_token=" \
                        + self.rand_token

            if res_data['state'] == 200:
                self.session.get(index_url)
                print("登录成功")
                break
            elif res_data['state'] == 101 or res_data['state'] == 102:
                continue
            elif res_data['state'] == 103 or res_data['state'] == 104:
                self.restart()
            else:
                print("\n出现异常")
                return False
        return True

    def getCourseList(self):
        pass

    def getAcadProg(self):
        self.parseTable(self.session.get(self.acadProgUrl).text, table_num=2)

    def getTermCoursesGrade(self):
        self.getTerm(line_limit=4)
        choose_term = input("选择学期\n")
        data = {
            "kksj": choose_term,
            "xsfs": "all"
        }
        res = self.session.get(self.grage_url, params=data)
        self.parseTable(res.text)

    def getTerm(self, line_limit=-1, show_list=True):
        self.Term_data = self.parseTerm(self.session.get(self.termUrl).text)
        if show_list == True:
            self.print2Cmd(self.Term_data, line_limit=line_limit, center_space=15)

    def getCourseGrade(self, name=""):
        self.getTerm(show_list=False)
        if name == "":
            name = input("课程名称: ")
        today = datetime.datetime.today()
        for termList in self.Term_data:
            if str(today.year) >= str(termList) and str(today.year-4) <= str(termList):
                data = {
                    "kksj": termList,
                    "xsfs": "all"
                }
                res = self.session.get(self.grage_url, params=data)
                if name in res.text:
                    self.parseTable(res.text, name=name)
                    continue

    def restart(self):
        python = os.executable
        os.execl(python, python, *sys.argv)

    def parseTable(self, html, table_num=1, name=""):
        html = etree.HTML(html)
        item = html.xpath("//table[%d]/tr/th/text()" % table_num)
        self.print2Cmd(item)
        for i in range(len(html.xpath("//table[%d]/tr" % table_num)) - 1):
            # data = []
            item = html.xpath(("//table[%d]/tr[{}]/td/text()" % table_num).      format(i + 2))
            if name == "":
                self.print2Cmd(item)
            else:
                for i in item:
                    if name in str(item):
                        self.print2Cmd(item)
                        return

    @staticmethod
    def parseTerm(html):
        return etree.HTML(html).xpath("//select[@name=\"kksj\"]/option/text()")[1:]

    @staticmethod
    def print2Cmd(InfoList, line_limit=-1, center_space=10):
        data = []
        output_format_one = ""
        for i, item_list in enumerate(InfoList):
            output_format_one = output_format_one + "|{%d:{%d}^%d}|" % (i, len(InfoList), center_space)
            if line_limit != -1 and i % line_limit == 0:
                output_format_one = output_format_one + '\n'
            data.append(item_list.replace("\n", "").replace("\t", ""))
        data.append(" ")
        print(output_format_one.format(*data))

    def printDesc(self):
        pass

    @staticmethod
    def notFinish():
        print("功能未完成")