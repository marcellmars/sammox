from datetime import datetime
import time

counter = 0
slip = 0.005

print(datetime.now().isoformat())

def tinterval():
    global counter
    global slip
    counter = counter + 1
    time.sleep(slip)
    delta = time.perf_counter() - (ztime + counter * 0.005)
    slip = 0.005 - delta
    #print("slip: {}, ztime: {}, delta: {}".format(slip, ztime, delta))

def go_tinterval(n=2000):
    global ztime 
    ztime = time.perf_counter()
    for i in range(n):
        tinterval()
    print("total time: {}, total delta: {}".format(time.perf_counter() - ztime, (time.perf_counter() - (ztime + counter * 0.005))))

go_tinterval()
print(datetime.now().isoformat())
