from telnetlib import X3PAD
from tkinter import Y
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.graph_objects as go
import streamlit as st  # 🎈 data web app development
from pandas import *
from signal import signal
import numpy as np
import math
import matplotlib.pyplot as plt


class Functions:
    #number of signals added
    numberSignalsAdded=-1
    #lists of added signals
    ADDED_FREQUENCES=[]
    ADDED_AMPLITUDES=[]
    ADDED_PHASES=[]
    ADDED_SIGNALS=[]
    amplitude_SUM = np.zeros(1000)  # Sum of AMPLITUDE of signals
    Current_amplitude=np.zeros(1000)

x_Time = np.arange(0, 2, 0.0005).tolist()  # Time Axis Array

def SHOW_SIN(magnitude, phase, frequency):  # Add new sin signal

    Y = np.zeros(1000)  # Array for saving sin signals values
    for i in range(1000): 
        Y[i] = (magnitude * (math.sin((2 * np.pi * frequency * x_Time[i]) + phase)))
    return go.Figure([go.Scatter(x=x_Time, y=Y)])

def SHOW_RES():  # Add new sin signal
    return go.Figure([go.Scatter(x=x_Time, y=Functions.Current_amplitude)])

def ADD_SIGNAL(added_magnitude, added_phase,added_frequency):
    new_y_amplitude = np.zeros(1000)  # Array for saving sin signals values
    for i in range(1000): 
         new_y_amplitude[i] = (added_magnitude * (math.sin((2 * np.pi * added_frequency * x_Time[i]) + added_phase))) 
    
    #updating lists
    Functions.numberSignalsAdded+=1
    Functions.ADDED_FREQUENCES.append(added_frequency)
    Functions.ADDED_AMPLITUDES.append(added_magnitude)
    Functions.ADDED_PHASES.append( added_phase)
    Functions.ADDED_SIGNALS.append(new_y_amplitude)
    Functions.Current_amplitude=np.add(Functions.Current_amplitude,new_y_amplitude)
    print(Functions.ADDED_FREQUENCES)
    # print(Functions.ADDED_SIGNALS)
    print(Functions.numberSignalsAdded)
    

    return go.Figure([go.Scatter(x=x_Time, y=Functions.Current_amplitude)])

def DELETE_SIGNAL(index_todelete): 
    if(len(Functions.ADDED_SIGNALS)==0):
        Functions.Current_amplitude=0
    else:
        Functions.Current_amplitude=np.subtract(Functions.Current_amplitude,Functions.ADDED_SIGNALS[index_todelete]  )
    Functions.ADDED_FREQUENCES.pop(index_todelete)
    Functions.ADDED_AMPLITUDES.pop(index_todelete)
    Functions.ADDED_PHASES.pop(index_todelete)
    Functions.ADDED_SIGNALS.pop(index_todelete)

    Functions.numberSignalsAdded-=1
    print(Functions.ADDED_FREQUENCES) 
    # print(Functions.ADDED_SIGNALS)
    print(Functions.numberSignalsAdded)    
    return go.Figure([go.Scatter(x=x_Time, y=Functions.Current_amplitude)])

def ADD_NOISE(snrRatio):
    power = Functions.Current_amplitude**2
    snr_db = 10 * np.log10(snrRatio)
    signal_avg_power=np.mean(power)
    signal_avg_power_db=10 * np.log10(signal_avg_power)
    noise_db=signal_avg_power_db - snr_db
    noise_watts=10 ** (noise_db/10)
    mean_noise=0
    noise=np.random.normal(mean_noise, np.sqrt(noise_watts),len(Functions.Current_amplitude))
    Functions.Current_amplitude = Functions.Current_amplitude+noise
    return go.Figure([go.Scatter(x=x_Time, y=Functions.Current_amplitude)])

def SHOW_NOISE(snrRatio):
    power = Functions.Current_amplitude**2
    snr_db = 10 * np.log10(snrRatio)
    signal_avg_power=np.mean(power)
    signal_avg_power_db=10 * np.log10(signal_avg_power)
    noise_db=signal_avg_power_db - snr_db
    noise_watts=10 ** (noise_db/10)
    mean_noise=0
    noise=np.random.normal(mean_noise, np.sqrt(noise_watts),len(Functions.Current_amplitude))
    noised_signal = Functions.Current_amplitude+noise
    return go.Figure([go.Scatter(x=x_Time, y=noised_signal)])

def ysampling(tsampling):
    sampling_y=[]
    for point in tsampling:
        sampling_y.append(np.interp(point,x_Time, Functions.Current_amplitude))
    return(sampling_y)
        
def sinc_interp(factor):
    fmax= max(Functions.ADDED_FREQUENCES)
    sampling_time= np.arange(0,2,1/(fmax*factor))
    sampling_y= ysampling(sampling_time)
    print(f"time={sampling_time}")
    print(f"y={sampling_y}")

    x_timeArr= np.array(x_Time)
    # Find the period    
    T = sampling_time[1] - sampling_time[0]
    
    sincM = np.tile(sampling_time, (len(x_timeArr), 1)) - np.tile(x_timeArr[:, np.newaxis], (1, len(sampling_time)))
    newy = np.dot(sampling_y, np.sinc(sincM/T))
    return go.Figure([go.Scatter(x=x_timeArr, y=newy)])

    # sincM = np.tile(sampling_time, (len(x_timeArr), 1)) - np.tile(x_timeArr[:, np.newaxis], (1, len(sampling_time)))
    # sampling_y= np.tile(sampling_y, (len(sampling_time), len(x_timeArr)))
    # newy = np.dot(sampling_y, np.sinc(sincM/T))
    # return go.Figure([go.Scatter(x=x_timeArr, y=newy)])
