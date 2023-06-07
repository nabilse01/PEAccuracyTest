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


def insert(min_sum_key, floor_id):
    # Establish connection to PostgreSQL database with parameters extracted above
    try:
        conn = psycopg2.connect(
            user=DB_User,
            password=DB_PW,
            host=DB_IP,
            port="5432",
            database=DB_name
        )

        # Create a cursor object to execute SQL queries on the established connection
        cursor = conn.cursor()

        sql0 = f"Update penguin.tblsystem_settings set value = {min_sum_key[3]} ,last_update = now()  where parameter_group = 'Position Engine' and settings_type_id = 2 and description = 'BleRSSIcutOff' and reference_id = {floor_id};"
        sql1 = f"Update penguin.tblsystem_settings set value = {min_sum_key[1]} ,last_update = now()where parameter_group = 'Position Engine' and settings_type_id = 2 and description = 'MinParticles' and reference_id = {floor_id};"
        sql2 = f"Update penguin.tblsystem_settings set value = {min_sum_key[0]} ,last_update = now() where parameter_group = 'Position Engine' and settings_type_id = 2 and description = 'MaxParticles' and reference_id = {floor_id};"
        sql3 = f"Update penguin.tblsystem_settings set value = {min_sum_key[2]} ,last_update = now() where parameter_group = 'Position Engine' and settings_type_id = 2 and description = 'StandardDeviation' and reference_id = {floor_id}; "

        cursor.execute(sql0)
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)

        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        # Check if conn exists before closing cursor and connection
        if conn:
            cursor.close()
            conn.close()
