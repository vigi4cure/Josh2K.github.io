#!/usr/bin/python

import sys
import re
import os
import shutil
import commands
import csv
from bs4 import BeautifulSoup

from stravalib.client import Client
import csv
import time
import datetime

def getSec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])


def segment_details(num,segment,topguy,friend_colour_dict):

    id = num + 1
    segment_id = segment.id
    segment_name = segment.name.encode('utf-8')
    segment_name = re.sub(',', "", segment_name)
    url = 'http://www.strava.com/segments/'+str(segment_id)+'/compare/'

    start_latitude = segment.start_latitude
    start_longitude = segment.start_longitude
    end_latitude = segment.end_latitude
    end_longitude = segment.end_longitude

    tuple=(str(num),str(start_latitude),str(start_longitude),str(segment_name)+':  ['+str(topguy)+']',str(topguy),str(friend_colour_dict[topguy]),str(segment_name),str(segment_id),str(url))
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    print str(now)+': ID: '+str(id)+'     Segment ID:  '+str(segment_id)+'   Owner:  '+str(topguy)
    return tuple
    

        
def main():
    reload(sys)  
    sys.setdefaultencoding('utf8')

    segmentlist = []
    file = open('segments.csv')
    reader = csv.DictReader(file)
    for line in reader:
        segmentlist.append(line["Segment Id"])

    #get rid of badsegments
    badsegments = []
    badinfile = open('bad_segments.csv')
    badreader = csv.DictReader(badinfile)
    for line in badreader:
        badsegments.append(line["Segment Id"])
    print 'Bad Segments: '+str(badsegments)
    
    for x in badsegments:
        if x in segmentlist:
            segmentlist.remove(x)
        
    client = Client(access_token='76824abf6abf903eb3d8b0bde83625135c0be0ec')
    athlete = client.get_athlete()
    print("Hello, {}. I know your email is {}".format(athlete.firstname, athlete.email))
    josh_friends = client.get_athlete_friends(5991862)
    for a in josh_friends:
        print("{} is Josh's friend.".format(a.firstname))
        
    #colors
    colours = ['575757','FFCDF3','FFEE33','FF9233','29D0D0','8126C0','814A19','1D6914','2A4BD7','AD2323','000000','88C6ED','82C341']
    
    segoutfile = open('segoutput.csv', 'w')
    segoutfile.write('id,latitude,longitude,name,type,color,segment_name,segment_id,url'+'\n')
    segoutputlist = []

    friend_colour_dict = {}
    friend_colour_file = open('friend_colour.csv')
    colourreader = csv.DictReader(friend_colour_file)
    for line in colourreader:
        friend_colour_dict[line["name"]] = line["colour"]

    friend_count_dict = {}
           
    
    for num,j in enumerate(segmentlist):
        time.sleep(5)
        segment = client.get_segment(j)
                        
        try:
            leaderboard = client.get_segment_leaderboard(j,following=True)
            if not leaderboard:
                topguy = 'UNCLAIMED'
            else:
                topguy = leaderboard[0].athlete_name
                            
            if not topguy in friend_colour_dict:
                friend_colour_dict[topguy] = colours.pop()

            if topguy in friend_count_dict:
                friend_count_dict[topguy] += 1
            else:
                friend_count_dict[topguy] = 1

                      
            
            for z in segment_details(num,segment,topguy,friend_colour_dict):
                segoutfile.write(str(z)+',')
            segoutfile.write('\n')
            
   
        except Exception:
            badoutfile = open('bad_segments.csv', 'a+')
            badoutfile.write(str(j)+',')
            badoutfile.close()
            pass

    segcountoutfile = open('segmentcount.csv', 'w')
    segcountoutfile.write('name,colour,count'+'\n')
    for x in friend_count_dict:
        if x != 'UNCLAIMED':
            print str(x)+': '+str(friend_count_dict[x])
            segcountoutfile.write(str(x)+','+str(friend_colour_dict[x])+','+str(friend_count_dict[x])+'\n')
    segcountoutfile.write('\n')
    segcountoutfile.close()


    segcountovertimefile = open('segmentcountovertime.csv', 'a+')
    nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
    for x in friend_count_dict:
        if x != 'UNCLAIMED':
            print str(x)+': '+str(friend_count_dict[x])
            segcountovertimefile.write(str(nowdate)+','+str(x)+','+str(friend_colour_dict[x])+','+str(friend_count_dict[x])+'\n')
    segcountovertimefile.write('\n')
    segcountovertimefile.close()
              

if __name__ == "__main__":
  main()
