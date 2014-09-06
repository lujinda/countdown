#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-09-06 15:25:35
# Filename        : countdown/core.py
# Description     : 

from countdown.data import DoDataBase
import re
import sys
import datetime
import time
import logging

class ErrorDate(Exception):pass

class commandHandler():
    def handler(self,line):
        parts=line.split(' ',1)
        cmd=parts[0]
        try:
            line=parts[1]
        except IndexError:
            line=""
        
        func=getattr(self,"do_"+cmd,None)
        try:
            func(line)
        except TypeError,e:
            print e
            self.do_help(cmd)

    def do_help(self,cmd):
        print """command list:
        show
        set <序号>
        end
        del <序号>
        add <事件名:事件要发生的日期[:事件发送周期]>
        delall"""

class countDown(commandHandler):
    def __init__(self):
        self.__conflog()
        self.re_thing=re.compile(r"\"(.+?)\"")
        self.database=DoDataBase()
        self.handler("show")

    def check_update(self):
        for thing,date in self.database.items():
            date,update_days = (date.split(':',1)+[None])[:2]
            if update_days and self.toTime('',date)[0] == 0:
                self.update_date(thing,
                        datetime.datetime(*map(int,date.split('-'))),
                        int(update_days))

    # 传入date是一个datetime对象，并非xxxx-xx-xx

    def update_date(self,thing,date,update_days):
        while True:
            date=date+datetime.timedelta(days=update_days)
            if (date - datetime.datetime.now()).days + 1 >=0:
                break

        date=date.strftime("%Y-%m-%d")
        self.database.update(thing,
                date + ':' + str(update_days))


    def __conflog(self):
        log_file="/var/log/countdown.log"
        self.logger=logging.getLogger("countDown")
        handler=logging.FileHandler(log_file)
        formatter=logging.Formatter("%(asctime)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def do_show(self,line):
        self.check_update()
        self.listItem={}
        things=[self.toTime(x,y.split(":")[0])[1] for x,y in self.database.items()]
        for i,thing in enumerate(things):
            print "(%d) %s "%(i+1,thing)
            self.listItem[str(i+1)]=self.re_thing.findall(thing)[0]

    def toTime(self,thing,time):
        
        date=datetime.datetime(*map(int,time.split('-')))
        nowDate=datetime.datetime.now()
        dates=(date-nowDate).days + 1

        if dates>=0:
            line=1,"离\"%s\"还有 %d 天"%(thing,dates)
        else:
            line=0,"\"%s\"已经过去了 %d 天"%(thing,abs(dates))
        return line

    def do_end(self,line):
        sys.exit(0)
