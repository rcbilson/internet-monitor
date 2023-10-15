#!/usr/bin/env python

from subprocess import Popen, PIPE
from enum import Enum
import io
import re
import threading
import time
import logging

class Pinger(threading.Thread):
  def __init__(self, address):
    threading.Thread.__init__(self)
    self.address = address
    self.count = 0
    self.output = ""
    self.success = False

  def nextline(self):
    if len(self.output) > 0:
      print(self.address + ": " + self.output)
    self.count = 0
    self.output = ""

  def run(self):
    proc = Popen(["/usr/bin/ping", self.address], stdout=PIPE)
    text = io.TextIOWrapper(proc.stdout, encoding="utf-8")
    pat = re.compile("time=([0-9]*)")
    while proc.poll() is None:
      line = text.readline()
      match = pat.search(line)
      if match:
        ms = int(round(int(match.group(1))/10, 0))
        if ms < 10:
          self.output += str(ms)
        else:
          self.output += "*"
        self.success = True
        self.count = self.count + 1
        if self.count >= 60:
          self.nextline()
      else:
        self.nextline()

  def check(self):
    result = self.success
    self.success = False
    return result

class State(Enum):
  INITIALIZING = 1
  ONLINE = 2
  OFFLINE = 3

if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s', level=logging.INFO)

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
    elif state == State.OFFLINE:
      if pingSuccessful:
        state = State.INITIALIZING
    else:
      logging.error(f"invalid state: {state}")
      state = State.INITIALIZING
    logging.debug(f"{oldState} -> {state}")
    if oldState != state:
      logging.info(f"{oldState} -> {state}")
