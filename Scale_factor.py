# Import the random module to generate random numbers for our lists
import psycopg2
from configparser import RawConfigParser
import pandas as pd
# penguin
config = RawConfigParser()
config.read('config.properties')
DB_IP = config.get('database', 'ip')
DB_User = config.get('database', 'user')
DB_PW = config.get('database', 'password')
DB_name = config.get('database', 'name')
pd.set_option('display.max_columns', None)


def get_scale_factor(floor_id,venue_id):
    try:
        conn = psycopg2.connect(
            user=DB_User,
            password=DB_PW,
            host=DB_IP,
            port="5432",
            database=DB_name
        )
        cursor = conn.cursor()
        # tblfp_rssi_readings
        # query = "SELECT * FROM penguin.tblfp_macs "
        query = f"SELECT scale_factor FROM penguin.tblfloors where venue_id={venue_id} and id = {floor_id}  "

        # query = "SELECT * FROM penguin.tblpennav_pe_simulation"
        cursor.execute(query)
        result = cursor.fetchone()[0]

        # query = "SELECT  * FROM penguin.tblfp_data  "

        return result
        # for row in rows:
        #     print(row)

    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if conn:
            cursor.close()
            conn.close()
