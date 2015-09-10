#!/usr/bin/python

import sys
import re
import os
import shutil
import commands
import csv
from bs4 import BeautifulSoup
import json
import requests
import csv
import time
import datetime
from subprocess import call
import strava1

        
def main():
    print 'Running parent script'
    time.sleep(10)
    commit_comment = 'autorun - '+str(datetime.datetime.now())
    print 'GIT commiting...'
    call(["git", "commit","-a","-m", commit_comment])
    time.sleep(10)
    print 'GIT pushing...'
    call(["git", "push"])
    


if __name__ == "__main__":
  main()
