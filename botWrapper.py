from subprocess import Popen
import sys

filename = 'app.py'
while True:
    print("\nStarting " + filename)
    p = Popen("python3 " + filename, shell=True)
    p.wait()
