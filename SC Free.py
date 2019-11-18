#!/usr/bin/env python3

# -------------------------------------------------------------
# DESCRIPION :  Scary simple script to auto log into Southwark
#               Center's free wifi.
# AUTHOR :      EchoLogic
# DATE :        16 Oct 2019
# -------------------------------------------------------------

import requests
import subprocess
import signal
import os

# caught from POST request in developer tools
url = "http://172.20.0.2:8082/vpn/loginUser/"
params = "?userid=scfree&password=scfree" # waw

driver = requests.Session()

try:
    response = driver.post(url + params)
    if str(response.status_code) == "200":
        print("You're in.")
    elif str(response.status_code) != "200":
        print("ERROR : Unable to login")
except Exception as e:
    print("ERROR : " + e)

# Yeah, that simple
# Let's close the login window for good mesure

proc_name = "gnome-shell-por"

# ps command in python (list running process) as a byte stream
ps = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
out, err = ps.communicate()

for line in out.splitlines():
    if proc_name in str(line):
        # extracting the first colomn or PID
        pid = int(line.split(None, 1)[0])

        # kill the process via it's PID
        os.kill(pid, signal.SIGKILL)

exit(0)
