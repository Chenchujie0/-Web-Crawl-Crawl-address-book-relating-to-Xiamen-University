from pybloom_live import BloomFilter
import os
import psutil

class BF:
    def __init__(self, rfilename, sfilename):
        f = open(rfilename, 'r')
        line = f.readlines()
        f.close()
        self.blm = BloomFilter(capacity = 10000000)

        f = open(sfilename, 'w')
        for i in line:
            if i in self.blm:
                print("true")
                continue
            else:
                self.blm.add(i)
                print("false")
                f.write(i)
        
        pid = os.getpid()
        p = psutil.Process(pid)
        info = p.memory_full_info()
        print(info.uss/1024./1024./1024.)

f = BF("test1.txt", "final.txt")
