#!/bin/python3
import threading
import time
import multireciever
import sender


if __name__ == "__main__":
	rec=["multireciever.start_reciever1()","multireciever.start_reciever2()"]
	threads = list()
	for index in rec:
		x = threading.Thread(target=index,daemon=True)
		threads.append(x)
		x.start()
	for index, thread in enumerate(threads):
		thread.join()
	
