from SimConnect import *
import sqlite3
from datetime import datetime
import time

sm = SimConnect()
ae = AircraftEvents(sm)
aq = AircraftRequests(sm, _time=10)


            


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
    
    if aq.get('BRAKE_PARKING_POSITION') !=1:
    
        for dp in datapoints: ## iterating over the provided datapoints


            result = aq.get(dp)
            
        
            
            if type(result) == bytes: ## some returns are bites, we convert them to strings
                result = result.decode('UTF-8')
            
            else:
                result = result
            
            print(dp+': '+str(result))
            results.append(result)
            time.sleep(0.1)


        ## adding non simconnect data

        #current 
        datapoints.append('COMPUTER_HOUR')
        results.append(datetime.now().strftime("%H:%M:%S"))

        datapoints.append('COMPUTER_DAY')
        results.append(datetime.now().strftime("%Y-%m-%d"))   

        datapoints.append('EPOCH_TIMESTAMP')
        results.append(datetime.now().timestamp())   




        ##creating table creation string
        table_name = 'fs2020_6'

        sqlstring = 'CREATE TABLE IF NOT EXISTS '+table_name+'('
        for d in datapoints:
            if type(results[datapoints.index(d)]) == str:

                sqlstring = sqlstring+d+' TEXT , ' 
            else:
                sqlstring = sqlstring+d+' real ,' 

        sqlstring = sqlstring[:-2]+')' ##remove last trailing coma and close the bracket

        ## sql string for inserting
        sqlinsert = 'INSERT INTO '+table_name+' VALUES '+str(tuple(results))


        con = sqlite3.connect('test.db')
        cur = con.cursor()
        cur.execute(sqlstring)
        cur.execute(sqlinsert)
        con.commit()
    
    else:
        print('parking brake on, no data recorded')
    time.sleep(5)

