import threading
import FINAL_UPDATE_R, FINAL_UPDATE_D
import time

while True:
  try:
    FINAL_UPDATE_D.DELIVERED_UPDATE()
    print('waiting for 30 seconds')
    time.sleep(30)
    FINAL_UPDATE_R.RESPONDED_UPDATE()
    time.sleep(30)
    print('waiting for 30 seconds')
  except Exception as ex:
    print('err while Updating D & R ' + str(ex))
