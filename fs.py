from SimConnect import *
import sqlite3
from datetime import datetime
import time

sm = SimConnect()
ae = AircraftEvents(sm)
aq = AircraftRequests(sm, _time=10)


            
##list of variables that need to be converted to INT  
listofints = ['PLANE_ALTITUDE',
              'PLANE_ALT_ABOVE_GROUND',
              'SIM_ON_GROUND',
              'AIRSPEED_INDICATED',
              'HEADING_INDICATOR',
              'BRAKE_PARKING_POSITION',
              'FUEL_TOTAL_CAPACITY',
              'TOTAL_WEIGHT',
              'FUEL_TOTAL_QUANTITY',
              'AMBIENT_WIND_VELOCITY',
              "AMBIENT_WIND_DIRECTION", 
              'AMBIENT_VISIBILITY',
               "BAROMETER_PRESSURE",
               "AMBIENT_TEMPERATURE"]

while True:
    results = []
    datapoints= ['PLANE_LATITUDE',
                 'PLANE_LONGITUDE',
                 'PLANE_ALTITUDE',
                 'PLANE_ALT_ABOVE_GROUND',
                 'SIM_ON_GROUND',
                 'AIRSPEED_INDICATED',
                 'AIRSPEED_MACH',
                 'VERTICAL_SPEED',
                 'HEADING_INDICATOR',
                 'AUTOPILOT_MASTER', 
                  "GPS_WP_NEXT_LAT",
                  "GPS_WP_NEXT_LON",
                  'GEAR_TOTAL_PCT_EXTENDED',
                  'BRAKE_PARKING_POSITION',
                  'TOTAL_WEIGHT',
                  'FUEL_TOTAL_QUANTITY',
                  'FUEL_TOTAL_CAPACITY', 
                 'AMBIENT_WIND_VELOCITY',
                 "AMBIENT_WIND_DIRECTION", 
                 'AMBIENT_VISIBILITY',
                 "BAROMETER_PRESSURE",
                 "AMBIENT_TEMPERATURE",
                 'GPS_WP_PREV_ID',
                  "GPS_WP_NEXT_ID", 
                  "ATC_MODEL",
                  'ZULU_TIME',
                 ]
  

    ##pulling all datapoints from simconnect
    for dp in datapoints:


        result = aq.get(dp)
        if type(result) == bytes: ## some returns are bites, we convert them to strings
            result = result.decode('UTF-8')
        if dp in listofints:
            result = int(result)
        print(dp+': '+str(result))
        results.append(result)


    ## adding non simconnect data to both lists

    #current 
    datapoints.append('COMPUTER_HOUR')
    results.append(datetime.now().strftime("%H:%M:%S"))

    datapoints.append('COMPUTER_DAY')
    results.append(datetime.now().strftime("%Y-%m-%d"))   

    datapoints.append('EPOCH_TIMESTAMP')
    results.append(datetime.now().timestamp())   

    con = sqlite3.connect('test.db')

 

    cur = con.cursor()
    #cur.execute("CREATE TABLE IF NOT EXISTS fs2020_4( PLANE_LATITUDE real ,PLANE_LONGITUDE real ,PLANE_ALTITUDE real ,PLANE_ALT_ABOVE_GROUND real ,SIM_ON_GROUND real ,AIRSPEED_INDICATED real ,AIRSPEED_MACH real ,VERTICAL_SPEED real ,HEADING_INDICATOR real ,AUTOPILOT_MASTER real ,GPS_WP_NEXT_LAT real ,GPS_WP_NEXT_LON real ,GEAR_TOTAL_PCT_EXTENDED real ,BRAKE_PARKING_POSITION real ,TOTAL_WEIGHT real ,FUEL_TOTAL_QUANTITY real ,FUEL_TOTAL_CAPACITY real ,AMBIENT_WIND_VELOCITY real ,AMBIENT_WIND_DIRECTION real ,AMBIENT_VISIBILITY real ,BAROMETER_PRESSURE real ,AMBIENT_TEMPERATURE real ,GPS_WP_PREV_ID TEXT , GPS_WP_NEXT_ID TEXT , ATC_MODEL TEXT , ZULU_TIME real ,COMPUTER_HOUR TEXT , COMPUTER_DAY TEXT , EPOCH_TIMESTAMP real)")
    cur.execute('INSERT INTO fs2020_4 VALUES '+str(tuple(results)))
    con.commit()
    time.sleep(5)

