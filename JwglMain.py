import os

from JwglCrawlClass import JwglCrawl

# crwal = JwglCrawl()
# crwal.login()
# crwal.getTerm(line_limit=4)
# crwal.getAcadProg()

crawl = JwglCrawl()


def printLevel1Menu():
    i = 0
    for index in range(0,len(level1Menu),2):
        print("%d. %s" % (i + 1, level1Menu[index]))
        i = i + 1
    return 0

def printLevel2Menu():
    string1 = level1Menu[(level1Pointer-1)*2]
    i = 0
    for index in range(0,len(levelMap),2):
        if levelMap[index] == string1:
            print("%d. %s" % (i+1, levelMap[index+1]))
            i = i + 1



# def execMenu1(level1Pointer, level2Pointer):
#     for index, item in enumerate(level1Menu):
#         if index + 1 == level1Pointer:
#             if level2Pointer == 0:
#                 print(level1Menu[level1Pointer])
#             else:
#                 for item1 in levelMap:
#                     if item == item1:
#                         loginLevel2Menu[levelMap[item1]]()
#
def execMenu2():
    temp_1 = 0
    for i in range(len(levelMap)):
        for index, item in enumerate(level1Menu):
            if index + 1 == level1Pointer:
                if levelMap[i] == level1Menu[level1Pointer]:
                    temp_1 = i
                    break
    ans = levelMap[temp_1 + 1 + (level2Pointer-1)*2]
    print(ans)
    loginLevel2Menu[ans]()

def setBackFlag():
    global  backFlag,level2Pointer
    backFlag = True
    level2Pointer = 0

def clear():
    os.system('cls')


level1Pointer = 0
level2Pointer = 0

backFlag = False

level1Menu = ["进入软件", "正在进入系统...",
              "查看程序描述和特点", "正在打开...",]

loginLevel2Menu = {"登录教务管理系统": crawl.login,
                   "获取某学期所有课程成绩": crawl.getTermCoursesGrade,
                   "查看某课程成绩(支持关键词模糊搜索)": crawl.getCourseGrade,
                   "查看学业完成进度": crawl.getAcadProg,
                   "查看选课中心课程": crawl.notFinish,
                   "返回上一级": setBackFlag,
                   "退出系统": exit}

levelMap = ["进入软件", "登录教务管理系统",
            "进入软件", "获取某学期所有课程成绩",
            "进入软件", "查看某课程成绩(支持关键词模糊搜索)",
            "进入软件", "查看学业完成进度",
            "进入软件", "查看选课中心课程",
            "进入软件", "返回上一级",
            "进入软件", "退出系统"]

if __name__ == "__main__":
    # global level1Pointer, level2Pointer
    #
    print("北科教务管理系统快速查询器")
    while True:
        print("-" * 10)
        printLevel1Menu()
        level1Pointer = int(input())
        while True:
            printLevel2Menu()
            try:
                level2Pointer = int(input())
            except:
                print("请输出正确格式数字")
            execMenu2()
            if backFlag == True:
                break
            else:
                input("按回车继续")
        backFlag = False
