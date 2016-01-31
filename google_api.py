import sys
import os
import subprocess
import time
import shlex   
import re      
from subprocess import call
from subprocess import CalledProcessError, check_output


re_asrresult = re.compile(r'.*?({"result.*)', re.DOTALL)
re_asrAlternative = re.compile(r'{"transcript":".*?".*?}', re.DOTALL)

filename = "temp.flac"
googlekeys = ["AIzaSyBfjHWXc3NFk-afqg3zKbIR3CtvOXi2NHM"]

def save_speech():
    command = "rec -r 16000 -L -c 1 -b 16 " + filename
    args = shlex.split(command)
    devnull = open('/dev/null', 'w')
    p = subprocess.Popen(args, stdout=devnull, stderr=devnull)
    time.sleep(0.5)
    print "I am listening... Press [ Enter ] again to stop recording."
    c = sys.stdin.readline().strip()
    time.sleep(2)
    p.kill()

def send_to_google():

    command = "curl -X POST --data-binary @{} --user-agent 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7' --header 'Content-Type: audio/x-flac; rate=16000;' 'https://www.google.com/speech-api/v2/recognize?client=chromium&lang=en-US&maxresults=10&key={}'".format(filename, googlekeys[0])

    try:
        devnull = open('/dev/null', 'w')
        out = check_output(shlex.split(command),
            shell=False,
            stderr=devnull)
    except CalledProcessError as e:
        print(e.returncode)
        sys.exit(1)

    #print "Google output:"
    #print out
    reObj = re_asrresult.match(out)
    asrResult = "NONE"
    if reObj:
        # raw-ish output
        asrResult = reObj.groups(1)[0]
        #print asrResult
    else:
        asrResult = " (Sorry, would you mind to say it again?:) "


    reObj = re_asrAlternative.findall(asrResult)
    if reObj:
        #return first alternative
        alternative = reObj[0]
        transcript = re.match(r'.*?"transcript":"(.*?)"', alternative)
        confidence = re.match(r'.*?"confidence":([\d.]+?)}', alternative)
        confidenceVal = -1 # default if no confidence returned
        if confidence:
            confidenceVal = confidence.group(1)
            #print "   transcript: {}, confidence: {}".format(transcript.group(1), confidenceVal)
        return transcript.group(1)
    return " (Sorry, would you mind to say it again?:) "

def get_google_asr():
    save_speech()
    return send_to_google()
