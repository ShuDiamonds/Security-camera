#!/usr/bin/env python3
# -*- Coding: utf-8 -*-
import os
import sys
import time

import reporting2


def fork():
    pid = os.fork()

    if pid > 0:
        f = open('/var/run/reporting2d.pid','w')
        f.write(str(pid)+"\n")
        f.close()
        sys.exit()

    if pid == 0:
        time.sleep(20)
        reporting2.main()
        #print("a")
        




if __name__=='__main__': 
    fork()
