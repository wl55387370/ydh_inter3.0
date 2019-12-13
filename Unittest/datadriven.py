# -*- coding:utf-8 -*-
# @Time    :2019/8/29 0029 11:15
# @Author  :wulin
# @Mail    :286075568@qq.com
# @FileName: datadriven.py
# @Software: PyCharm


import inspect, sys, datetime
from common.do_excel import Reader, Writer

reader = Reader()
writer = Writer()
alllist = []
runtype = 'HTTP'
title = ''


# 获取关键字
def geffunc(line, http):
    func = None
    try:
        func = getattr(http, line[0])
    except Exception as e:
        print(e)

    return func


# 获取参数
def getargs(func):
    if func:
        args = inspect.getfullargspec(func).__str__()
        args = args[args.find('args=') + 5:args.find(', varargs')]
        args = eval(args)
        args.remove('self')
        l = len(args)
        return l
    else:
        return 0


# 运行用例
def run(func, lenargs, line):
    if func is None:
        return False

    if lenargs < 1:
        res = func()
        return res

    if lenargs < 2:
        res = func(line[1])
        return res

    if lenargs < 3:
        res = func(line[1], line[2])
        return res

    if lenargs < 4:
        res = func(line[1], line[2], line[3])
        return res

    print('error：目前只支持3个参数!')
    return False


# 选择排序
def selectSort(height):
    l = len(height)
    for i in range(0, l):

        tmp = 0
        for j in range(1, l - i):
            if str(height[tmp]) < str(height[j]):
                tmp = j

        # 把最高的放到最后
        t = height[tmp]
        height[tmp] = height[l - i - 1]
        height[l - i - 1] = t


def mysort(lists):
    # 用来存下标
    l = []
    # 初始化一共有多少个元素
    list1 = []
    for i in range(len(lists)):
        l.append(i)
        list1.append(i)

    selectSort(l)

    for i in range(len(l)):
        list1[l[i]] = lists[i]

    return list1


def getparams(casepath, resultpath):
    global reader, writer, alllist, runtype, title
    wb = reader.open_ecxel(casepath)
    print(wb)

    # sheetname = reader.get_sheets()
    # for sheet in sheetname:
    #     # 设置当前读取的sheet页面
    #
    #     reader.set_sheet(sheet)
    #     # 第一行
    #     reader.readline(0)
    #
    #     # 第二行
    #     line = reader.readline(1)

    # # 默认获取最后的一个sheet页
    # runtype = line[1]
    # print(runtype)
    #
    #
    # title = line[2]
    # if resultpath == '':
    #     pass
    # else:
    #     writer.copy_open(casepath, resultpath)

    writer.copy_open(casepath, resultpath)

    sheetname = reader.get_sheets()
    writer.set_sheet(sheetname[0])

    for sheet in sheetname:
        reader.set_sheet(sheet)
        line = reader.readline(1)
        # print(line)
        # 循环遍历每一个
        if line[1] == 'HTTP':
            runtype = line[1]
            print(runtype)
            title = line[2]
        else:
            continue

        writer.set_sheet(sheet)

        writer.clo = 8
        list = [sheet, '', '', '', '', '']
        alllist.append(list)
        for i in range(reader.rows):
            list = [i]
            line = reader.readline(i)
            if len(line[0]) > 0 or len(line[1]) > 0:
                pass
            else:
                list += line[2:7]
                alllist.append(list)
    # 后期如果有乱序的问题可以去掉注解
    # alllist = mysort(alllist)

    print(alllist)
