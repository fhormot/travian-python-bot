from subprocess import Popen
import sys

filename = "overnightFS.py"

while True:
    print("\nStarting " + filename)
    p = Popen("python3 " + filename, shell=True)
    p.wait()
