# -*- coding: utf-8 -*-
"""
@author: SON
"""
#Import libraries for data analysis and to help create graphs
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Prompt user for csv input
CSV = input("Please enter full csv name: ")

#read in user input, create variable for packet size and time
test_file =pd.read_csv(CSV)
last_row = len(test_file)
total_packets = test_file['Packet length'].sum()
total_time = test_file['Time'].iloc[-1]
avg_packet_length = total_packets/total_time

#create graph using numpy
test_file_graph = test_file.copy()

a = test_file_graph['Packet length'].to_numpy()
b = test_file_graph['Time'].to_numpy()


bins = int(total_time)

totals,edges = np.histogram(b,weights=a,bins=bins)

edges = np.resize(edges, edges.size - 1)

#plot graph
plt.figure(figsize=(9, 6))
plt.plot(edges, 
        totals)
plt.title('')
plt.xlabel('Time')
plt.ylabel('Packet length')
plt.ticklabel_format(style='plain')

plt.show()


#First section of code to catch large file downloads immediately and save the code processing time
if avg_packet_length > 600000:
    
    print('A large file download has been detected in this capture')

#Second section of the code if the previous threshold is not met, check for size
elif (avg_packet_length < 600000):
    #create last index variable to return an absolute value of time in order to iterate through 120 seconds
    last_index = abs(test_file['Time'] - (total_time - 120)).idxmin()
    #For loop to check eveery 120 seconds by iterating 0-120 and then 1-121 and so on
    i = 0
    maximum = 0
    for i in range (i,last_index):
        
        start_time = test_file['Time'].iloc[i]
        end_time = start_time + 120
        index = abs(test_file['Time'] - end_time).idxmin()
        packet_size = test_file.iloc[i:index, 8].sum()
        #create finish time variable
        finish_time = end_time - start_time
        #calculate the average bytes per second in variable
        average_length = (packet_size/finish_time)
        if (average_length > maximum):
            maximum = average_length
        
    #final ifs checks to see if the bytes per second for any 120 seconds has hit the thresholds
    if (maximum > 600000):
        
        print('A large file download has been detected in this capture over 120 Seconds')
               
        
    elif (maximum < 600000) and (maximum > 100000):
            
        print('A video stream was detected in this capture over 120 Seconds')
        
            
    else:
    
        print('Size of Bytes per second is consistent with Web Page Browsing')