#!/usr/bin/python3
#coding=utf-8

'''
BMLink - links and unlinks BM TGs by command line using APIv2

This is a simple Python3 script which links or unlinks BM talkgroups by command line.
You can call it manually to quickly link or unlink TGs to your repeater without login into the dashboard.
You can also call the script e.g. by crontab to schedule time dependent bookings of TGs.

Before you go to use this script, create an API key in your BM Selfcare profile and add it below.
You must also insert the DMR-ID of your repeater / hotspot below.

Please keep in mind that you can only modify repeaters where you are assigned as a sysop.
(And your own devices of course...)


Created on 29.07.2024

@author: dd5xl
'''


import json
import requests
import sys


# 1st ToDo:
# Enter your BM-API key and DMR-ID of repeater / node below!
APIKEY = "<< Insert your API-Key here >>"
DMRID = "<< Target node >>"
# don't edit below this line!


def showHelp(retCode=0):
    print ("\nBM-LinkTG - link and unlink BM talkgroups by cmdline\n")
    if retCode == 1:
        print ("Error: wrong number of arguments, 3 expected.")
    elif retCode == 2:
        print ("Error arg1: wrong command, 'start', 'stop' or 'list' expected.")
    elif retCode == 3:
        print ("Error arg2: wrong slot number, 1 or 2 expected.")
    elif retCode == 4:
        print ("Error arg3: wrong TG number, only digits expected.")
    print ("\nUsage: python3 bmlink.py [start|stop] [slot] [TGNr]")
    print ("Example: 'python3 bmlink.py start 2 2626' -> book TG2626 to repeater slot 2\n")
    exit (retCode)


def showTGs (tgStr):
    tgList = json.loads(tgStr)
    for slot in ["1", "2"]:
        for tgDict in tgList:
            if tgDict['slot'] == slot:
                print (f"Slot {tgDict['slot']} : {tgDict['talkgroup']}")
        print()
    return len(tgList)


def bmLink():
    APIENDP = "https://api.brandmeister.network/v2/"

    if len (sys.argv) > 1: # at least 1 arugument?
        req = APIENDP + f"device/{DMRID}/talkgroup"
        if sys.argv[1].lower() in ["start", "stop"]:
            if sys.argv[2] in ["1", "2"]:
                if sys.argv[3].isdigit():
                    jdata = json.dumps({"slot":sys.argv[2], "group":sys.argv[3]})
                    if sys.argv[1] == "start":
                        print (f"Linking TG{sys.argv[3]} on node {DMRID} to slot {sys.argv[2]}: ", end="")
                        resp = requests.post(req, \
                                             headers={"Content-Type" : "application/json", \
                                                      "Accept" : "application/json, text/plain, */*", \
                                                      "Authorization" : "Bearer " + APIKEY}, \
                                             data=jdata)
                    else:
                        req += f"/{sys.argv[2]}/{sys.argv[3]}"
                        print (f"Unlinking TG{sys.argv[3]} on node {DMRID} from slot {sys.argv[2]}: ", end="")
                        resp = requests.delete(req, \
                                               headers={"Content-Type" : "application/json", \
                                                      "Accept" : "application/json, text/plain, */*", \
                                                      "Authorization" : "Bearer " + APIKEY})
                    if resp.status_code == 200:
                        print (f"API request successful, ({resp.status_code}).")
                    else:
                        print (f"API request failed, ({resp.status_code}), Error.")
                        return 128
                else:
                    showHelp(4) # invalid TG number
            else:
                showHelp(3) # wrong slot
        elif sys.argv[1].lower() == "list":
            resp=requests.get(req, \
                                   headers={"Content-Type" : "application/json", \
                                          "Accept" : "application/json, text/plain, */*", \
                                          "Authorization" : "Bearer " + APIKEY})
            if resp.status_code == 200:
                print (f"API request successful, ({resp.status_code}).\n")
                print (f"Currently linked TGs on node {DMRID}:\n")
                showTGs(resp.text)
            else:
                print (f"API request failed, ({resp.status_code}), Error.")
                return 128
        else: # wrong command
            showHelp(2)
    else: # wrong length
        showHelp(1)
    return 0
    
if __name__ == '__main__':
    bmLink()