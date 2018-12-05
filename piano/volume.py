import os
import subprocess


def volumechange(volume):
    subprocess.call(['./volbash.sh',str(volume)])
