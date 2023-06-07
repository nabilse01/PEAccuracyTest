from flask import Flask,request
import sig
import stabel_FP
import numpy as np
import itertools
import PE_parameter_update
import Scale_factor
import datetime
import Payload
import json
import requests
from configparser import RawConfigParser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
    
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import test_comb3
import test_comb4
app = Flask(__name__)

@app.route("/",methods = ["POST","GET"])
def result():
    config = RawConfigParser()
    config.read('config.properties')

    PE_Url = config.get('PE', 'url')
    url = PE_Url+'PEService.svc/Initialize'
    root = tk.Tk()
    root.title("CDF")
    # Creating lists of different values
    # meters  # creating a list of multiples of 50 in the range starting from 100 and ending at 250. Also providing a comment describing what the range represents
    MaxParticlesM = list(range(100, 151, 50))  # meters
    minParticlesM = list(range(50, 151, 50))
    distSTDM = list(range(3, 8, 2))
    bleRSSIcutOffM = [-95, -200]
    data = request.json # assuming the values are sent in JSON format
    venue_id = int(data.get(('venue_id')))
    floor_id = int(data.get('floor_id'))
    montecarloIter = int(data.get('montecarloIter')) 
    max_error = int(data.get('max_error'))
    ninety_five_percent_error = int(data.get('max_error')) 
    output = 1
    # Using a function to get a scale factor based on the given Floor_Id
    scale_factor = Scale_factor.get_scale_factor(
        floor_id=floor_id, venue_id=venue_id)
    # Converting data into the given format and saving
    stabel_FP.convert(venue_id=venue_id, floor_id=floor_id)
    response = requests.request("GET", url)
    print('okk')
    # Printing the Venue and Floor ID
    print(f"____________________VENUE_ID: {venue_id}____________________")
    print(f"#############\tFloor_Id: {floor_id}")
    print(f'the scale factor for this venue and floor is {scale_factor}')
    start = datetime.datetime.now()
    DiffAll, max_error_D, value, min_sum_key = test_comb3.final(venue_id, floor_id, montecarloIter, scale_factor,
                                                                MaxParticlesM, minParticlesM, distSTDM, bleRSSIcutOffM)
    draw_cdf_method = test_comb3.Draw_CDF
    end2 = datetime.datetime.now()
    end_2 = end2 - start
    print(end_2)

    if max_error_D < max_error or value['value_at_95th_percentile'] < ninety_five_percent_error:
        PE_parameter_update.insert(min_sum_key, floor_id=floor_id)
        draw_cdf_method(DiffAll, min_sum_key, venue_id, floor_id)

    else:
        sorted_data = np.sort(DiffAll)
        yvals = np.arange(len(sorted_data))/float(len(sorted_data)-1)
        # Create the confirmation window
        window = tk.Tk()
        fig, ax = plt.subplots()
        ax.plot(sorted_data, yvals)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        # Function to print action for button
    return 'Success'
if __name__ == '__main__':
    app.run()

