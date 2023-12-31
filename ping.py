#!/usr/bin/env python

from pinger import Pinger
from enum import Enum
from datetime import datetime
import os
import time
import logging
import notification

class State(Enum):
  INITIALIZING = 1
  ONLINE = 2
  OFFLINE = 3

if __name__ == "__main__":
  logArgs = {
    'format': '%(asctime)s:%(levelname)s:%(process)d:%(message)s',
    'level': logging.INFO
  }
  logFile = os.environ.get('LOG_FILE')
  if logFile != None:
    logArgs['filename'] = logFile

  logging.basicConfig(**logArgs)

  pinger = Pinger("8.8.8.8")
  pinger.start()

  state = State.INITIALIZING
  while True:
    time.sleep(15)
    pingSuccessful = pinger.check()
    oldState = state
    if state == State.INITIALIZING:
      if pingSuccessful:
        state = State.ONLINE
    elif state == State.ONLINE:
      if not pingSuccessful:
        state = State.OFFLINE
        offlineDate = datetime.now()
    elif state == State.OFFLINE:
      if pingSuccessful:
        state = State.INITIALIZING
        notification.send(f"Internet connection restored, offline since {offlineDate.isoformat()}")
    else:
      logging.error(f"invalid state: {state}")
      state = State.INITIALIZING
    if oldState != state:
      logging.info(f"{oldState} -> {state}")
