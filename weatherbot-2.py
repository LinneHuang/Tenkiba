#!/usr/bin/env python

import sys, re
import getopt, os
import json
import nltk

from weathercom import get_weathercom


def usage():
    print "weatherbot.py [-u \"Celsius\"] [-c \"San Francisco\"]"

if __name__=="__main__":

    # set user model defaults
    default_unit = "Celsius"
    default_city = "San Francisco"
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

    print "Starting AwesomeProgram by Student..."   # modify this line to add the name of your bot.
    print "...default unit: " + default_unit
    print "...default city: " + default_city

    stopped = False
    while not stopped:
        
        # Step 1: get the user input
        user_input = raw_input("User utterance: ")
        print "User input is: " + user_input

        # check if the user wants to quit
        if user_input == "quit":
            break # exit the loop right away

        ########
        # Step 2: parse the user input into a semantic representation
        # of the form TOPIC, LOCATION, DATE
        # This is the part you should modify
        ########

        # parse topic
        topic = "notweather"
        m = re.search("weather", user_input, re.I)
        if m:
            topic = "weather"
        
        if topic != "weather":
            print "Sorry I am not smart enough to respond."
            continue

        print "Parsed topic: " + topic

        #parse location
        location = default_city
        m = re.search("in (\w+)", user_input)
        if m:
            location = m.group(1)
        print "Parsed location: " + location

        #parse date
        date = default_date
        m = re.search("today|tomorrow", user_input)
        if m:
            date = m.group(0)
        print "Parsed date: " + date

        ######
        # Steps 3 and 4: send and obtain the weather forecast
        ######
        
        #get current weather and weather forecast from weather.com
        weathercom_result = get_weathercom(location)

        #print weathercom_result

        ######
        # Step 5: generate output to the user
        # This is the part you should modify
        #######
        weatherbot_output = ""
        
        if date == "today":
            weatherbot_output = "Current weather in " + \
                                location + \
                                " is " + \
                                weathercom_result["current_conditions"]["text"] + \
                                " with temperature " + \
                                weathercom_result["current_conditions"]["temperature"] + \
                                " degrees Celsius."
        elif date == "tomorrow":
            weatherbot_output = "The weather tomorrow in " + \
                                location + \
                                " is " + \
                                weathercom_result["forecasts"][1]["day"]["text"] + \
                                " with temperature between " + \
                                weathercom_result["forecasts"][1]["low"] + \
                                " and " + \
                                weathercom_result["forecasts"][1]["high"] + \
                                " degrees Celsius or " + \
                                    str (int(weathercom_result["forecasts"][1]["high"])*20 - 16)



        print "WeatherBot says: " + weatherbot_output
            
            
    print "Goodbye."
