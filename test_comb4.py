import Payload
import json
import requests
from configparser import RawConfigParser
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import asyncio
import itertools
import ujson as json
import math
import aiohttp
import datetime
import psycopg2
from collections import defaultdict
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import socket
import tkinter as tk
from tkinter import ttk

import time

max_threads = 10 

adapter = requests.adapters.HTTPAdapter(max_retries=50)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)
diff_F = []
config = RawConfigParser()
config.read('config.properties')
PE_Url = config.get('PE', 'url')
headers = {'Content-Type': 'application/json'}
url = PE_Url+'PEService.svc/GetEP'
DB_IP = config.get('database', 'ip')
DB_User = config.get('database', 'user')
DB_PW = config.get('database', 'password')
DB_name = config.get('database', 'name')

def get_sig_ids(venue_id, floor_id):
    try:
        conn = psycopg2.connect(
            user=DB_User,
            password=DB_PW,
            host=DB_IP,
            port="5432",
            database=DB_name
        )

        cursor = conn.cursor()
        cursor.execute(
            f"SELECT DISTINCT sig_id FROM penguin.tblsignature_data WHERE venue_id = {venue_id} AND floor_id = {floor_id}")
        sig_ids = [row[0] for row in cursor.fetchall()]
        return sig_ids
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        # Check if conn exists before closing cursor and connection
        if conn:
            cursor.close()
            conn.close()


def get_data(venue_id, floor_id, sig_id):
    try:
        conn = psycopg2.connect(
            user=DB_User,
            password=DB_PW,
            host=DB_IP,
            port="5432",
            database=DB_name
        )

        cursor = conn.cursor()
        cursor.execute(
            f"SELECT time_stamp, major_minor, rssi, x, y FROM penguin.tblsignature_data WHERE venue_id = {venue_id} AND floor_id = {floor_id} AND sig_id = {sig_id} ORDER BY time_stamp ASC  ")
        results = cursor.fetchall()
        return results
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        # Check if conn exists before closing cursor and connection
        if conn:
            cursor.close()
            conn.close()


result = {}

def get_list(venue_id,floor_id,sig_id):
        
        readings_for_all_sigs = []
        readings_by_time = defaultdict(list)
        for row in get_data(venue_id, floor_id, sig_id):
            time_stamp, major_minor, rssi, x, y = row
            key = str(time_stamp)
            readings_by_time[key].append((major_minor, rssi, x, y))
        readings_for_all_sigs.append(readings_by_time)
        return readings_for_all_sigs
def send_request(sig_id, floor_id, venue_id, sig_id_n,scale_factor,montecarloIter):
    
    for combination in z:
        add = 1
        Param_MaxParticlesM = int(combination[0])
        Param_minParticlesM = int(combination[1])
        Param_distSTDM = int(combination[2])
        Param_bleRSSIcutOffM = int(combination[3])
        add = 1
        req = 1
        readings_for_all_sigs = get_list(venue_id,floor_id,sig_id)
        sig_id_n = f'{sig_id_n}_{Param_MaxParticlesM}_{Param_minParticlesM}_{Param_distSTDM}_{Param_bleRSSIcutOffM}'
        
        for time, readings in readings_for_all_sigs[0].items():
            Data = ''
            for record in readings:
                
                # Join each record with ','
                Data = ''.join(
                    [f"{record[0]},{record[1]},2_" for record in readings])
            EP = Payload.GetEP_Payload
            EP.data = Data[:-1]
            EP.session_id = str(sig_id_n)
            EP.user_id = str(sig_id_n)
            EP.fix_floor_id = str(floor_id)
            EP.orientation = "0"
            EP.barometer_reading = "0"
            EP.req_id = str(req)
            EP.steps_count = "2"
            EP.heading = "0"
            EP.orientation_status = "1"
            EP.accelerometer_status = "1"
            EP.is_wi_fi = False
            EP.reset_particles = False
            EP.device_id = "88755444"
            EP.trigger_venue_detection = False
            EP.maxParticlesSettings = Param_MaxParticlesM
            EP.minParticlesSettings = Param_minParticlesM
            EP.rssiCutOffLimitSettings = Param_bleRSSIcutOffM
            EP.standardDeviationSettings = Param_distSTDM
            payload = json.dumps(EP.to_dict(EP))
            response =session.post(url, headers=headers, data=payload)
            req = req+1
            mylist = response.text.split(",")
            my_float_val = float(mylist[2].encode('utf-8'))
            
            if my_float_val == -1 or my_float_val == -2  :
                print('hii')
            else:
                if response.text.find("-1000") != -1:
                    pass
                else:
                    diff = math.hypot(float(record[2]) - float(mylist[2].encode('utf-8')),
                                      float(record[3]) - float(mylist[3].encode('utf-8')))* scale_factor
                    if diff is not None:
                        diff_F.append(diff)
            
                   # print(diff)

        # print(scale_factor)
        if add == 1:
            lists1 = diff_F.copy()
        add = 0
        for i in range(len(lists1)):
            if lists1[i] > diff_F[i]:
                diff_F[i] = lists1[i]    
        result[combination] = lists1
def final(venue_id,floor_id,montecarloIter,scale_factor
          ,MaxParticlesM,minParticlesM,distSTDM,bleRSSIcutOffM):
    global z
    sorted_cdfs=[]
    z = [(a, b, c, d) for a in MaxParticlesM
         for b in minParticlesM
         for c in distSTDM
         for d in bleRSSIcutOffM
         if b < a]
    DiffAll = []
    DiffAll1 = []  # creating an empty list named DiffAll that may be appended later on
    DiffAll2 = []
    start_threads(venue_id,floor_id,montecarloIter,scale_factor)
    
    for combination, lists in result.items():
        print(combination)
        result_with_stats = {}
        result_with_stats1 = {}
        # Sort the lists in the dict value
        sorted_list = np.sort(lists)

        # Calculate the maximum, minimum, standard deviation, mean and median values of the sorted list
        max_value = np.max(sorted_list)
        min_value = np.min(sorted_list)
        std_value = np.std(sorted_list)
        mean_value = np.mean(sorted_list)
        median_value = np.median(sorted_list)

        # Scale the list to have values between 0 and 1
        yvals = np.arange(len(sorted_list))/float(len(sorted_list)-1)

        # Find the index and value at the 90th percentile of the sorted list
        idx_of_90th_percentile = next(
            i for i, x in enumerate(yvals) if x >= 0.9)
        value_at_90th_percentile = sorted_list[idx_of_90th_percentile]

        # Find the index and value at the 95th percentile of the sorted list
        idx_of_95th_percentile = next(
            i for i, x in enumerate(yvals) if x >= 0.95)
        value_at_95th_percentile = sorted_list[idx_of_95th_percentile]


        # Store the statistical information in a nested dictionary 'result_with_stats'
        result_with_stats[combination] = {
            'sorted_list': sorted_list,
            'max': max_value,
            'min': min_value,
            'std': std_value,
            'mean': mean_value,
            'median': median_value,
            'yvals': yvals,
            'idx_of_90th_percentile': idx_of_90th_percentile,
            'value_at_90th_percentile': value_at_90th_percentile,
            'idx_of_95th_percentile': idx_of_95th_percentile,
            'value_at_95th_percentile': value_at_95th_percentile,

            # Additionally, this code calculates the sum of max, min, std, mean, median, 90th and 95th percentile values.
        }
        
        
        for key, value in result_with_stats.items():
            min_sum = float('inf')
            # Looping over the key-value pairs in `result_with_stats`.
            curr_sum = value['max'] + value['min'] + value['std'] + value['mean'] + \
                value['median'] + value['value_at_90th_percentile'] + \
                value['value_at_95th_percentile']
            # Calculate the sum of specific values in the nested dictionary `value`
            # and assign it to `curr_sum`.
            result_with_stats[combination]['sum_of_values'] = float(curr_sum)
        result_with_stats_Sort = sorted(result_with_stats.items(), key=lambda item: item[1]['sum_of_values'], reverse=True)
        for key, value in result_with_stats_Sort:
            print(key)
            print(value['sum_of_values'])
            DiffAll = value['sorted_list']
            DiffAll1.append(DiffAll)
            DiffAll2.append(str(key))
        # Get the min 5 keys and their values
    # result_with_stats_sorted = sorted(result_with_stats.items(), key=lambda x: x[1]["sum_of_values"])
    # print(result_with_stats_Sort)
    def Draw_CDF1(Diffs, venue_id, floor_id,min_sum_keys):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for i, Diff in enumerate(Diffs):
            sorted_data = np.sort(Diff)
            yvals = np.arange(len(sorted_data))/float(len(sorted_data)-1)
            ax.plot(sorted_data, yvals, label=min_sum_keys[i])
            
        ax.set_title(f'venue_id: {venue_id} floor_id: {floor_id}')
        ax.legend()
        plt.show()
        fig.savefig(f'venue_id_{venue_id}_floor_id_{floor_id}.png', dpi=100)
# Loop over the sorted dictionary and append the sorted list to DiffAll list
    Draw_CDF1(DiffAll1[:5], 12, 35,DiffAll2[:5])



    return DiffAll, max_error_D, value, min_sum_key
threads = []
thread_pool_size = 10
def start_threads(venue_id,floor_id,montecarloIter,scale_factor):
    global add
    add = 1
    global lists
    lists = []
    global sig_ids
    sig_ids = get_sig_ids(venue_id, floor_id)


    for sig_id in sig_ids:
        for j in range(montecarloIter):
            t = threading.Thread(target=send_request,
                                 args=(sig_id, floor_id, venue_id, f"{sig_id}_{j}",scale_factor,montecarloIter))              
            t.start()
            threads.append(t)
    for t in threads:
        t.join()
    
def Draw_CDF(Diffs, venue_id, floor_id):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for i, Diff in enumerate(Diffs):
        min_sum_key = f'Diff {i+1}'
        sorted_data = np.sort(Diff)
        yvals = np.arange(len(sorted_data))/float(len(sorted_data)-1)
        ax.plot(sorted_data, yvals, label=min_sum_key)
        
    ax.set_title(f'venue_id: {venue_id}  floor_id: {floor_id}')
    ax.legend()
    plt.show()
    fig.savefig(f'venue_id_{venue_id}_floor_id_{floor_id}.png', dpi=100)

