from subprocess import Popen, PIPE
import io
import re
import threading
import logging

class Pinger(threading.Thread):
  def __init__(self, address):
    threading.Thread.__init__(self, daemon=True)
    self.address = address
    self.count = 0
    self.output = ""
    self.success = False

  def nextline(self):
    if len(self.output) > 0:
      logging.debug(self.address + ": " + self.output)
    self.count = 0
    self.output = ""

  def run(self):
    while True:
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
      logging.warning("ping subprocess exited unexpectedly; restarting")

  def check(self):
    result = self.success
    self.success = False
    return result

