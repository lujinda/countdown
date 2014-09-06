#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-09-05 12:37:25
# Filename        : countdown/data.py
# Description     : 

import shelve
from contextlib import contextmanager


class DoDataBase():
    def __init__(self):
        pass
    
    @contextmanager
    def __db_opera(self):
        import os
        HOME_PATH=os.environ['HOME']
        DB_PATH=os.path.join(HOME_PATH,".countdown.db")
        db = shelve.open(DB_PATH,'c')
        yield db
        db.close()

    # retuen database item:key,value...
    def items(self):
        with self.__db_opera() as db:
            return db.items()

    def select(self,key):
        with self.__db_opera() as db:
            return db[key]

    def update(self,key,value):
        with self.__db_opera() as db:
            db[key] = value

    def delete(self,key=None):
        with self.__db_opera() as db:
            if key:
                del db[key]
            else:
                db.clear()

        

