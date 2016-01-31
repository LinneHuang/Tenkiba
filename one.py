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
    print " "
    print "* * * * * * * * * * * *  * * * * * * * * * * * *"
    print "* * * * * Good day! My name is Tenkiba.* * * * *"
    print "* * * * I am a Shiba and I know weather. * * * *"
    print " "
    print "* Say [ Goodbye ] to me if you gotta go. :3"
    print " "    
    print "* The default unit is [" + default_unit + "] * *"
    print "* The default city is [" + default_city + "] * *"
    print "* Today is " + time.strftime("%x") + ", Wooooof."
    print "* * * * * * * * * * * *  * * * * * * * * * * * *"
    print "* * * * * * * * * * * *  * * * * * * * * * * * *"

    tenkiba0 = "Goodday! My name is Ten-ki-ba. I am a shi-ba, and I know weather......Say Goodbye to me if you gotta go."
    tts(tenkiba0)

# # # L O O P - 1 # # #
    stopped = False
    while not stopped:

# "Ask me weather! Give me a city, and the day you would like to know."
# "tokyo / tomorrow / weather"

#L# user_input = get_google_asr()
  # parse location
  # parse date
  # parse weather or NOT weather -- "ask me weather-related questions."
  # answering
  # continue / exit


        # Step 1-0: user_city_input
        print ""
        tenkiba1 = "What city you would like to know?"
        print "--What city you would like to know?"
        tts(tenkiba1)

        # Step 1-1: get the user input from microphone and send it to Google API
        user_city_input = get_google_asr()

        # GOODBYE or NOT GOODBYE? #
        if user_city_input == "goodbye":
            print " [ Goodbye ] "
            tenkiba1_1 = "I heard you. Have a nice day! Goodbye."
            print tenkiba1_1
            print ""
            print "* * * * * * * * * * * * * * * * * * * * * * * * *"
            tts(tenkiba1_1)
            sys.exit()
            # break # exit the loop right away

        # Step 1-2: parse user_city_input
        result = ""
        tokens = nltk.word_tokenize(user_city_input)
        tagged = nltk.pos_tag(tokens)
        chunk = nltk.chunk.ne_chunk(tagged)
        traverse(chunk, result)

        if lo == "":
            location = default_city
        else:
            location = lo

        # Step 2-0: user_ask_input -- 

        tenkiba2_1 = "Got it. So,"
        print "--Got it. So,"
        tts(tenkiba2_1)

        tenkiba2_2 = location
        print "[ " + (tenkiba2_2) + " ]"
        tts(tenkiba2_2)
        continue

# # # L O O P - 2 # # #
    stopped = False
    while not stopped:

        tenkiba2_3 = "What weather info you would like to know? Weather today, weather tomorrow, or chance to rain, or, chance to get tanned..."
        print "---- Ask me: | weather today | weather tomorrow | chance to rain | chance to get sunburn | ..."
        tts(tenkiba2_3)
    
        # Step 2-1: get the user's question, and send it to Google API
        user_ask_input = get_google_asr()

        # GOODBYE or NOT GOODBYE? #
        if user_ask_input == "goodbye":
            print " [ Goodbye ] "
            tenkiba2_4 = "I heard you. Have a nice day! Goodbye."
            print tenkiba2_4
            print ""
            tts(tenkiba2_4)
            print "* * * * * * * * * * * * * * * * * * * * * * * * *"
            sys.exit()


                            ########
                            # Step 2: parse the user input into a semantic representation
                            # of the form TOPIC, LOCATION, DATE
                            # This is the part you should modify
                            ########

        result = ""

        # Step 2-2: parse user_ask_input
        topic = "notweather"
        m = re.search("(Weather|weather|cold|warm|rain|wind|windy|typhoon|tsunami|tornado|thunderstorm|thunder|thermometer|temperature|sunny|sun|storm|snowy|snowstorm|snow|sleet|sky|rainy|rainbow|rainstorm|rain|radar|pressure|precipitation|moon|meteorology|lightning|ice|hurricane|humidity|hot|heat|hail|frost|freeze|forecast|fog|flood|Fahrenheit|dry|drizzle|dew|degree|cyclone|cold|cloudy|clouds|cloud|cirrus|chill|Celsius|blizzard|barometer|air)", user_ask_input, re.I)
        if m:
            topic = "weather"
            tenkiba3 = "Roger that. I heard you said [ " + user_ask_input + " ]. Let me think..."
            print(tenkiba3)
            tts(tenkiba3)
        else:
            tenkiba3_1 = "Woof-Woof... Would you mind to ask me again?"
            print "Woof Woof? Would you mind to ask me again? :3"
            tts(tenkiba3_1)
            print ""
            continue


        #Step 2-3: parse date
        date = default_date
        m = re.search("today|tomorrow|forecasts", user_ask_input)
        if m:
            date = m.group(0)
        else:
            tenkiba4_0 = "Pardon me, I didn't get your date. I will tell you today's weather first:"
            print tenkiba4_0
            tts(tenkiba4_0) 

        ######
        # Steps 3 and 4: send and obtain the weather forecast
        ######
        
        #get current weather and weather forecast from weather.com
        weathercom_result = get_weathercom(location) 

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
            print "Sorry I can't find " + location + ", would you mind to ask me another city?"
        
        # (O) If the user asked "San Francisco + today":
        if date == "today":

            # briefly describing the weather today
            w_text = weathercom_result["current_conditions"]["text"]

            if w_text in ["Clear", "Fair", "Very Hot"]:
               weatherbot_w_text += "It is a lovely day. I can feel the sunshine on my face. Woof! "
            elif w_text == "Partly Cloudy":
               weatherbot_w_text += "Keep warm and carry a jacket on, woof."
            elif w_text in ["Cloudy", "Mostly Cloudy"]:
               weatherbot_w_text += "Every cloud has a silver lining, woof."
            elif w_text in ["Blowing Snow", "Chance of Snow Showers", "Snow Showers", "Chance of Snow", "Snow", "Flurries", "Chace of Ice Pellets", "Ice Pellets", "Blizzard", "Very Cold"]:
               weatherbot_w_text += "Melting your frozen morning with a sound from the steam of a cup of hot coffee."
            elif w_text in ["Chance of Showers", "Showers", "Chance of Rain", "Rain"]:
               weatherbot_w_text += "plop plop drip drip, plop plop drip drip. Umbrella? Check. Ah, did you write your name on it?"
            else:
               weatherbot_w_text += ""


            weatherbot_output += "Today in " + \
                                location + \
                                " is... [ " + \
                                weathercom_result["current_conditions"]["text"] + \
                                " ]! with [ " + \
                                weathercom_result["current_conditions"]["temperature"] + \
                                " C ] ,and feels like [ " + \
                                weathercom_result["current_conditions"]["feels_like"] + \
                                " C ]. Humidity is [ " + \
                                weathercom_result["current_conditions"]["humidity"] + \
                                " % ]. Will it burn? [ " + \
                                weathercom_result["current_conditions"]["uv"]["index"] + \
                                " uv degree, " + \
                                weathercom_result["current_conditions"]["uv"]["text"] + \
                                " chance ]. "

            w_uv = int(weathercom_result["current_conditions"]["uv"]["index"])
            if w_uv >= 5:
               weatherbot_w_uv += "It might be a good day to get tanned. But be careful of heat-stroke!"
            elif w_uv <= 4:
                weatherbot_w_uv += "Mr. Sunshine is very gentle today, just like me."

            print ""
            print "- - - - - ( Tenkiba is checking ) - - - - - "
            print ""
            print weatherbot_w_text
            tts(weatherbot_w_text)
            print ""
            print weatherbot_output
            tts(weatherbot_output)
            print ""
            print weatherbot_w_uv
            tts(weatherbot_w_uv)
            print ""


        elif date == "tomorrow":

            # Briefly describing the weather tomorrow:
            w_tmrtext = weathercom_result["forecasts"][1]["day"]["text"]

            if w_tmrtext in ["Clear", "Fair", "Very Hot"]:
               weatherbot_w_tmrtext += "It is a lovely day. I can feel the sunshine on my face. Woof!"
            elif w_tmrtext == "Partly Cloudy":
               weatherbot_w_tmrtext += "Keep warm and carry a jacket on, woof."
            elif w_tmrtext in ["Cloudy", "Mostly Cloudy"]:
               weatherbot_w_tmrtext += "Every cloud has a silver lining, woof."
            elif w_tmrtext in ["Chance of Showers", "Showers", "Chance of Rain", "Rain"]:
               weatherbot_w_tmrtext += "plop plop drip drip, plop plop drip drip. Umbrella? Check. Ah, did you write your name on it?"
            elif w_tmrtext in ["Blowing Snow", "Chance of Snow Showers", "Snow Showers", "Chance of Snow", "Snow", "Flurries", "Chace of Ice Pellets", "Ice Pellets", "Blizzard", "Very Cold"]:
               weatherbot_w_tmrtext += "Melting your frozen morning with a sound from the steam of a cup of hot coffee."
            else:
               weatherbot_w_tmrtext += "Tomorrow seems a nice day."

            weatherbot_output += "Tomorrow in " + \
                                location + \
                                " is... [ " + \
                                weathercom_result["forecasts"][1]["day"]["text"] + \
                                " ] with [ " + \
                                weathercom_result["forecasts"][1]["low"] + \
                                " - " + \
                                weathercom_result["forecasts"][1]["high"] + \
                                " C ]. Will it rain? [ " + \
                                weathercom_result["forecasts"][1]["day"]["chance_precip"] + \
                                " % ]. Sun will rise at [ " + \
                                weathercom_result["forecasts"][1]["sunrise"] + \
                                " ]. " 

            w_rain = int(weathercom_result["forecasts"][1]["day"]["chance_precip"])
            if w_rain >= 80:
               weatherbot_w_rain += "Umbrella, check."
            elif w_rain >= 50:
                weatherbot_w_rain += "I can smell some rain. I hope you brought an umbrella with you."
            elif w_rain >= 10:
                weatherbot_w_rain += "It is true that low chance for rain, but a trench coat is a good fit for today. Actually, for everyday, right?"
            else:
                weatherbot_w_rain += "I can see Mr.sunshine is here, or, on his way!"

            print ""
            print "- - - - - ( Tenkiba is checking ) - - - - - "
            print ""
            print weatherbot_w_tmrtext
            tts(weatherbot_w_tmrtext)
            print ""
            print weatherbot_output
            tts(weatherbot_output)
            print ""
            print weatherbot_w_rain
            tts(weatherbot_w_rain)
            print ""

        else:
            weatherbot_output += "Oh no. Sorry. Something wrong. Do you mind to go visit my friend, Weather.com? He is an awesome weatherman." # link



''' Weather Bot - Shiba / weatherbot.py / 
    Edited by Linn S. Huang / Tutored by Maxim & Roberto'''
