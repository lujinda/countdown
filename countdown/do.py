#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-09-01 17:39:09
# Filename        : countdown/do.py
# Description     : 
from countdown.core import countDown,ErrorDate


class showData(countDown):
    def __init__(self):
        countDown.__init__(self)
        self.handler("end")

class setData(countDown):
    def __init__(self):
        countDown.__init__(self)
        self.input_do()

    def input_do(self):
        while 1:
            try:
                line=raw_input("> ")
            except (KeyboardInterrupt,EOFError):
                self.handler("end")
            self.handler(line.strip())

    def do_set(self,line):
        thing=self.getKey(line)
        if thing:
            newDate=raw_input("请输入新日期(year-mon-day):")
            
            self.handler("add %s:%s"%(thing,newDate))
            
    def do_add(self,line):
        try:
            thing,date=line.split(':',1)
            date,update_days=(date.split(':',1) + [None])[:2]

            try:
                state=self.toTime(" ",date)[0]   # 起到测试日期是否合理作用
         #       if state == 0 and update_days: # 表示是已经过去了，不符合自动更新规范
          #          raise ErrorData

            except:
                print "请输入正确日期!"
                return None

            
            self.database.update(thing,
                    date + ':' + update_days)
            self.logger.info("%s >> %s"%(thing,date))
            self.handler("show")
        except (KeyError,ValueError):
            print "请正确输入(事件名:事件发生日期):"
            return None
            
    def getKey(self,line):
        try:
            return self.listItem[line]
        except KeyError:
            print "请选择一个有效的序列!"
            return None
        
    
    def do_del(self,line):
        try:
            thing=self.getKey(line)
            time=self.database.select(thing)
            self.database.delete(thing)
            self.logger.info("del %s at %s"%(thing,time))
            self.handler("show")
        except:
            pass

    def do_delall(self,line):
        self.database.delete()
        self.logger.info("del all things")
