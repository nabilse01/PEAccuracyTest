# Import required libraries and read csv file
import psycopg2
from configparser import RawConfigParser
import pandas as pd
import datetime


# Create an instance of RawConfigParser to read a configuration file
config = RawConfigParser()

# Read the 'config.properties' file using the instance that was created on the Line no. 2
config.read('config.properties')

# Get the values of "ip", "user", "password" and "name" under the "database" section from the configuration file.
DB_IP = config.get('database', 'ip')
DB_User = config.get('database', 'user')
DB_PW = config.get('database', 'password')
DB_name = config.get('database', 'name')


def convert(venue_id, floor_id):
    # Establish connection to PostgreSQL database with parameters extracted above
    try:
        conn = psycopg2.connect(
            user=DB_User,
            password=DB_PW,
            host=DB_IP,
            port="5432",
            database=DB_name
        )
        cur = conn.cursor()

    # Execute the query
        now = datetime.datetime.now()
        cur.execute(f"""
            DELETE FROM penguin.tblfp_rssi_readings where floor_id = {floor_id} ;
            DELETE FROM penguin.tblfp_macs where floor_id = {floor_id};
            INSERT INTO penguin.tblfp_rssi_readings (line_id, mac, rssi, ssid, floor_id, x, y, band, active, create_date, last_update, update_status)
                SELECT line_id, major_minor, rssi, uuid, floor_id, x, y, '2', 'True', create_date, '{now}', '1' 
                FROM penguin.tblfp_data 
                WHERE venue_id = {venue_id} AND floor_id = {floor_id};
            INSERT INTO penguin.tblfp_macs (mac, ssid, floor_id, x, y, band, active, create_date)
                SELECT major_minor, uuid, floor_id, x, y, '2', 'True', create_date 
                FROM penguin.tblfp_data 
                WHERE venue_id = {venue_id} AND floor_id = {floor_id};
        """)
        
        conn.commit()      
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if conn:
            conn.close()



