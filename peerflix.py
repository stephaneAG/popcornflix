#!/usr/bin/env python
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import os
import re

try:
 input = raw_input
except NameError:
 pass

# Getting user input
mort = int(raw_input("Movie(1) or Tv Show(2)?:"))
if mort == 1:
    print ("**include year for more accurate results**")
    check = raw_input("Movie Title:").replace(" ","%20")
elif mort == 2:
    check2 = raw_input("What show would you like to watch?")
    print ("**Leave season choice blank if looking for newest episodes**")
    check3 = raw_input("Which season are you looking for? (1,2,3... etc):")
    if check3 == "":
        check = str(check2)
    else:
        check = ("{} season {}".format(check2, check3)).replace(" ","%20")
else:
    raw_input("Press Enter to Exit and try again")
    


# Creating link
query = "http://thepiratebay.gd/search/{}/0/99/200".format(check)
r = requests.get(query)
soup = BeautifulSoup(r.content, "html.parser")

# Finding seeds and leachers
q = []
seeders = []
leachers = []
for x in soup.find_all('td'):
    q.append(x)
seeds = q[2:32:4]
for x in seeds:
    seeders.append(str(x)[18:23])
leacher = q[3:32:4]
for x in leacher:
    leachers.append(str(x)[18:22])
    
# Finding file sizes
sizelist = []
size = q[1:32:4]
for x in size:
    size1 = (str(x).split("Size")[1:2])
    finalsize = (str(size1)[2:7])
    sizelist.append(finalsize)
    
# title and magnet link lists
j = []
read = []

# filtering out un-needed data and creating lists
for link in soup.find_all('a'):
    text = link.get('href')
    title = text.split("torrent")[1:2]
    for h in title:
        if h != " ":
            read.append(h)
    magnet = text.split("magnet")[1:2]
    for x in magnet:
        if x != " ":
            j.append(x)

# Grabbing list items containing torrent titles
j1 = read[0:16:2]

# Printing out torrent titles
r = 1
o = 0
for t in j1:
    print ("{})  {}".format(r, t[9:]).replace("/", " "))
    seeders[o] = re.sub("[^0-9]","", seeders[o])
    leachers[o] = re.sub("[^0-9]","", leachers[o])
    try:
        sizelist[o] = float(sizelist[o])
    except ValueError:
        sizelist[o] = 0
    if float(sizelist[o]) == 0:
        print ("     Seeds-{}    Leachers-{}    Size- No Data".format(seeders[o], leachers[o]))
    elif float(sizelist[o]) < 50.0:
        print ("     Seeds-{}    Leachers-{}    Size-{}Gb".format(seeders[o], leachers[o], sizelist[o]))  
    elif float(sizelist[o]) > 50.0:
        print ("     Seeds-{}    Leachers-{}    Size-{}Mb".format(seeders[o], leachers[o], sizelist[o]))
    else:
        print ("     Seeds-{}    Leachers-{}    Size-No Data Available".format(seeders[o], leachers[o]))
    print (" ")
    r += 1
    o += 1
    
# User chooses proper link
choice = raw_input("Whick link is correct? (1,2,3.. etc):")
# Finalizing magnet link

link = "magnet" + j[int(choice)-1]
# Launching Peerflix
if mort == 1 or check3 == "":
    os.system('peerflix "{}" --vlc'.format(link))
else:
    while True:
        print ("***Be sure to check file size. Not all files within the torrent will be full episodes***")
        os.system('peerflix "{}" -l --vlc'.format(link))
