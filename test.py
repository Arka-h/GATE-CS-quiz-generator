from datetime import datetime as dt
import multiprocessing as mp


def timer(q, start):
    while True:
        stop = q.qsize()
        diff = dt.now() - start
        ms = diff.microseconds//10**4
        min, sec = divmod(diff.seconds, 60)
        print(f"Time Taken {min}:{sec}:{ms}", end="\r")
        if stop:
            q.get()
            q.put(diff)
            break


if __name__ == "__main__":
    
    start = dt.now()
    q = mp.Queue()
    p = mp.Process(target=timer, args=(q, start))
    
    p.start()
    m = input()
    q.put(True)
    p.join()
    print("\n",q.get())
