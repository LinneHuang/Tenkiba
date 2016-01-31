#!/usr/bin/env python

import sys, re, time
import getopt, os, urllib, subprocess as sub
import urllib2
import json
import nltk
import pprint

from weathercom import get_weathercom
from tree import traverse
from google_api import get_google_asr
from tts import tts

# city? idk wut is this whole dame things. lol
lo = ""

def usage():
    print "weatherbot.py [-u \"Celsius\"] [-c \"San Francisco\"]"

def traverse(t,gpe):
    global lo

    if gpe != "":
        return
    else:
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined

            if t.label()=="GPE":
                is_gpe = True
            else:
                is_gpe = False

            for child in t:
                if is_gpe:
                    if gpe == "":
                        gpe = child[0]
                    else:
                        gpe = gpe + " "
                        gpe = gpe + child[0]
                    lo = gpe
                else:
                    traverse(child, gpe)
            return

if __name__=="__main__":

    # set defaults
    default_unit = "Celsius"
    default_city = "Tokyo"
    default_date = "today"

    #read command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:c:",
                                   ["help", "units=", "current_city="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    # parse command line arguments
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-u", "--units"):
            default_unit = a
        elif o in ("-c", "--current_city"):
            default_city = a
        else:
            assert False, "unknown option"

    # # # GREETINGS # # #
    print ""
    print "Ask me weather. Say [ goodbye ] to exit."

    tenkiba0 = "ask me weather. say goodbye to exit"
    tts(tenkiba0)

    # # # L O O P # # #
    stopped = False
    while not stopped:

        # Step 1-0: user_input
        print ""
        tenkiba1 = "Say a city and a day."
        print "(Ex: weather info + city + today/tomorrow)"
        print ""
        tts(tenkiba1)

        # Step 1-1: get the user input from microphone and send it to Google API
        user_input = get_google_asr()

        # (!) GOODBYE or NOT GOODBYE? #
        if user_input == "goodbye":
            print "Bye."
            tenkiba1_1 = "Bye."
            print tenkiba1_1
            print ""
            tts(tenkiba1_1)
            sys.exit()
            # to terminate Tenkiba

        # Step 2-1: parse TOPIC user_input
        topic = "notweather"
        m = re.search("(Weather|weather|cold|warm|rain|wind|windy|typhoon|tsunami|tornado|thunderstorm|thunder|thermometer|temperature|sunny|sun|storm|snowy|snowstorm|snow|sleet|sky|rainy|rainbow|rainstorm|rain|radar|pressure|precipitation|moon|meteorology|lightning|ice|hurricane|humidity|hot|heat|hail|frost|freeze|forecast|fog|flood|Fahrenheit|dry|drizzle|dew|degree|cyclone|cold|cloudy|clouds|cloud|cirrus|chill|Celsius|blizzard|barometer|air)", user_input, re.I)
        if m:
            topic = "weather"

        if topic != "weather":
            tenkiba3_1 = "try again:"
            print tenkiba3_1
            tts(tenkiba3_1)
            continue

        tenkiba3 = "Your question:"
        print(tenkiba3)
        print user_input
        tts(tenkiba3)

        # Step 2-1: parse CITY from user_input
        location = default_city
        m = re.search("in (\w+)(\ )?(\w+)", user_input) #(\w+)(\ )?(\w+)
        if m:
            location = m.group(0)
            location = location.replace("in", "")
            location = location.replace("today", "")
            location = location.replace("tomorrow", "")

        else:
            location = default_city
            tenkiba3_2 = "Your city is not found. Searching with the default city..."
            print tenkiba3_2
            tts(tenkiba3_2)
        #print "Parsed location: " + location
        
        """location = default_city
        result = ""
        tokens = nltk.word_tokenize(user_input)
        tagged = nltk.pos_tag(tokens)
        chunk = nltk.chunk.ne_chunk(tagged)
        traverse(chunk, result)

        if lo == "":
            location = default_city
        else:
            location = lo"""

        # Step 2-0: user_input -- 


        #Step 2-3: parse DATE from user_input
        date = default_date
        m = re.search("today|tomorrow|forecasts", user_input)
        if m:
            date = m.group(0)
            
        else:
            date = default_date
            tenkiba4_0 = "Your date is not found. Searching with the default date, today."
            print tenkiba4_0
            tts(tenkiba4_0)

        
        #get current weather and weather forecast from weather.com
        weathercom_result = get_weathercom(location) 
        if weathercom_result == False:
           print "Wrong result."
           continue

        # print weathercom_result

        ######
        # Step 5: generate output to the user
        # This is the part you should modify
        #######
        weatherbot_output = ""
        weatherbot_w_text = ""
        weatherbot_w_uv = ""
        weatherbot_w_rain = ""
        weatherbot_w_tmrtext = ""

        # (X) If the user asked "San Fransokyo"...
        if weathercom_result.has_key("current_conditions") == False:
            tenkiba2_4 = location + "is not found. Ask another city:"
            print tenkiba2_4
            tts(tenkiba2_4)
            continue

        # (O) If the user asked "San Francisco + today":
        if date == "today":

            weatherbot_output += "Today in " + \
                                location + \
                                " is [ " + \
                                weathercom_result["current_conditions"]["text"] + \
                                " ]."

            weatherbot_output += " [ " + \
                                weathercom_result["current_conditions"]["temperature"] + \
                                " C ] "

            weatherbot_output += "feels like: [ " + \
                                weathercom_result["current_conditions"]["feels_like"] + \
                                " C ]. " 

            weatherbot_output += "Humidity: [ " + \
                                weathercom_result["current_conditions"]["humidity"] + \
                                " % ]."

            weatherbot_output += " UV: [ " + \
                                weathercom_result["current_conditions"]["uv"]["index"] + \
                                " uv degree, " + \
                                weathercom_result["current_conditions"]["uv"]["text"] + \
                                " chance ]. "


            print ""
            print weatherbot_output
            tts(weatherbot_output)
            print ""



        elif date == "tomorrow":

            weatherbot_output += "Tomorrow in " + \
                                location + \
                                " is [ " + \
                                weathercom_result["forecasts"][1]["day"]["text"] + \
                                " ] "

            weatherbot_output += "[ " + \
                                weathercom_result["forecasts"][1]["low"] + \
                                " - " + \
                                weathercom_result["forecasts"][1]["high"] + \
                                " C ]. " 

            weatherbot_output += " Precipitation: [ " + \
                                weathercom_result["forecasts"][1]["day"]["chance_precip"] + \
                                " % ]."

            weatherbot_output += " Sunrise: [ " + \
                                weathercom_result["forecasts"][1]["sunrise"] + \
                                " ]. " 

            print ""
            print weatherbot_output
            tts(weatherbot_output)
            print ""

        else:
            weatherbot_output += "Something wrong." # link



''' Weather Bot - Shiba / weatherbot.py / 
    Edited by Linn S. Huang / Tutored by Maxim & Roberto'''
