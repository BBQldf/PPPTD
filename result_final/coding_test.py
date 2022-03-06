import time

def procedure():
    time.sleep(10)

# measure process time
t0 = time.process_time()
procedure()
t1 = time.process_time()
print(t0, "seconds process time")

# measure wall time
t0 = time.time()
procedure()
print(time.time() - t0, "seconds wall time")

procedure()
procedure()