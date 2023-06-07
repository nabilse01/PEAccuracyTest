# Importing modules needed for the code

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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import test_comb3
import test_comb4


config = RawConfigParser()
config.read('config.properties')

PE_Url = config.get('PE', 'url')
url = PE_Url+'PEService.svc/Initialize'
root = tk.Tk()
root.title("CDF")
# Creating lists of different values
# meters  # creating a list of multiples of 50 in the range starting from 100 and ending at 250. Also providing a comment describing what the range represents
MaxParticlesM = list(range(100, 251, 50))  # meters
minParticlesM = list(range(50, 201, 50))
distSTDM = list(range(3, 10, 2))
bleRSSIcutOffM = [-95, -200]


def calculate():
    venue_id = int(E1.get())
    floor_id = int(E2.get())
    montecarloIter = int(E3.get()) if str(E3.get()).isnumeric() else 10
    max_error = int(E4.get()) if str(E4.get()).isnumeric() else 10
    ninety_five_percent_error = int(
        E5.get()) if str(E5.get()).isnumeric() else 5
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
    print('wooow')
    print(min_sum_key)
    if max_error_D < max_error or value['value_at_95th_percentile'] < ninety_five_percent_error:
        PE_parameter_update.insert(min_sum_key, floor_id=floor_id)
        draw_cdf_method(DiffAll, min_sum_key, venue_id, floor_id)
    else:
        sorted_data = np.sort(DiffAll)
        yvals = np.arange(len(sorted_data))/float(len(sorted_data)-1)
        # Create the confirmation window
        window = tk.Tk()
        fig, ax = plt.subplots()
        ax.plot(sorted_data, yvals,label=min_sum_key)
        plt.legend()
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        # Function to print action for button

        def action(button):
            if button == 'Yes':
                fig.savefig(
                    f'venue_id_{venue_id}  floor_id_{floor_id}'+'.png', dpi=100)
                print('hello2')
                PE_parameter_update.insert(min_sum_key, floor_id=floor_id)
                print('hello3')
                pass
            else:
                fig.savefig(
                    f'venue_id_{venue_id}  floor_id_{floor_id}'+'.png', dpi=100)
                pass
            window.destroy()
        # Creating the 'Yes' button
        label = tk.Label(window, text="Do you Approve this CDF ?",
                         fg="blue", font=("Helvetica", 16))
        label.pack(padx=10, pady=10)
        yes_button = tk.Button(
            window, text="Yes", command=lambda: action('Yes'))
        yes_button.pack()
        # Creating the 'No' button
        no_button = tk.Button(window, text="No", command=lambda: action('No'))
        no_button.pack()

L1 = tk.Label(root, text='Venue id:', font=40)
L1.grid(row=0, column=0)
E1 = tk.Entry(root, fg='red')
E1.grid(row=0, column=1)

L2 = tk.Label(root, text='Floor id:', font=40)
L2.grid(row=1, column=0)
E2 = tk.Entry(root, fg='red')
E2.grid(row=1, column=1)


L3 = tk.Label(root, text='Number of Repetions :', font=40)
L3.grid(row=2, column=0)
E3 = tk.Entry(root, fg='red')
E3.insert(tk.END, '10')
E3.grid(row=2, column=1)


L4 = tk.Label(root, text='Max Accepted Error:', font=40)
L4.grid(row=3, column=0)
E4 = tk.Entry(root, fg='red')
E4.insert(tk.END, '10')
E4.grid(row=3, column=1)

L5 = tk.Label(root, text='95 percent error:', font=40)
L5.grid(row=4, column=0)
E5 = tk.Entry(root, fg='red')
E5.insert(tk.END, '5')
E5.grid(row=4, column=1)

submit_button = tk.Button(root, text="Submit", command=calculate)
submit_button.grid(row=5, column=1)

# Create the output label widget
output_label = tk.Label(root, text="")
output_label.grid(row=7, column=0, columnspan=2)


labels = [L3, L4, L5]
entries = [E3, E4, E5]
for label in labels:
    label.grid_remove()
for entry in entries:
    entry.grid_remove()


def toggle_entries():
    for label in labels:
        if label.winfo_ismapped():
            submit_button = tk.Button(root, text="Submit", command=calculate)
            submit_button.grid(row=5, column=1)
            label.grid_remove()
            entries[labels.index(label)].grid_remove()
        else:
            label.grid()
            entries[labels.index(label)].grid()


toggle_button = tk.Button(
    root, text="Advanced Options", command=toggle_entries)
toggle_button.grid(row=6, columnspan=3)


root.mainloop()


# 0:22:23.442985

# 107  333             2      BleRSSIcutOff  -200  Position Engine
# 108  339             2       MinParticles   200  Position Engine
# 109  338             2       MaxParticles   250  Position Engine
# 110  384             2  StandardDeviation     9  Position Engine
