import pywapi

def get_weathercom(location):

    lookup = pywapi.get_location_ids(location)
    
    for i in lookup:
        location_id = i
        
    weathercom_result = pywapi.get_weather_from_weather_com(location_id)

    #output = {}
    #output["today"] = {}
    #output["today"]["temperature"] = weathercom_result["current_conditions"]["temperature"]
    #output["today"]["text"] = weathercom_result["current_conditions"]["text"]

    #output["tomorrow"] = {}
    #output["tomorrow"][]

    return weathercom_result
