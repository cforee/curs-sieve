#!/usr/bin/python
import termios, fcntl, sys, os
fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

# movement handlers
def up(location):
  location["y"] -= 1
def right(location):
  location["x"] += 1
def down(location):
  location["y"] += 1
def left(location):
  location["x"] -= 1

# render the screen
def render(map_context):
  print map_context

# define starting location
location = {
  "x":42,
  "y":42
}

# map keypress to movement
actions = {
  "i":up,
  "k":right,
  "m":down,
  "j":left
}

# start main program loop
print "\n\n=== Use i,k,m,j to move around ===\n"

try:	
  while True:
    try:
      render(location)
      keypress = sys.stdin.read(1).lower()
      if keypress in actions:
        actions[keypress](location)
    except IOError: pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
