#!/usr/bin/env python
#coding:utf8
from countdown.do import showData,setData
import optparse


def parse_args():
    usage="usage: %prog [set]"
    parser=optparse.OptionParser(usage)
    
    _,option=parser.parse_args()

    if not option:
        return "show"
    
    if option[0]!='set':
        return "show"
    return "set"




def main():
    action=parse_args()
    if action=="show":
        do=showData()
    else:
        do=setData()
        do.cmdloop()


if __name__=="__main__":
    main()
        
