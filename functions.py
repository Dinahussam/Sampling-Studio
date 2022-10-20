from telnetlib import X3PAD
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

x_Time = np.arange(0, 0.5, 0.0005).tolist()  # Time Axis Array

def SHOW_SIN(magnitude, phase, frequency):  # Add new sin signal

    Y = np.zeros(1000)  # Array for saving sin signals values
    for i in range(1000): 
        Y[i] = (magnitude * (math.sin((2 * np.pi * frequency * x_Time[i]) + phase)))
    return go.Figure([go.Scatter(x=x_Time, y=Y)])

def SHOW_ADDED():  # Add new sin signal
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

def DELETE_SIGNAL():  
    Functions.Current_amplitude=Functions.ADDED_SIGNALS[Functions.numberSignalsAdded]  
    Functions.ADDED_FREQUENCES.pop(Functions.numberSignalsAdded)
    Functions.ADDED_AMPLITUDES.pop(Functions.numberSignalsAdded)
    Functions.ADDED_PHASES.pop(Functions.numberSignalsAdded)
    Functions.ADDED_SIGNALS.pop(Functions.numberSignalsAdded)

    Functions.numberSignalsAdded-=1
    print(Functions.ADDED_FREQUENCES) 
    # print(Functions.ADDED_SIGNALS)
    print(Functions.numberSignalsAdded)    
    return go.Figure([go.Scatter(x=x_Time, y=Functions.Current_amplitude)])

def ADD_NOISE(signal, snrRatio):
    power = signal**2
    snr_db = 10 * np.log10(snrRatio)
    signal_avg_power=np.mean(power)
    signal_avg_power_db=10 * np.log10(signal_avg_power)
    noise_db=signal_avg_power_db - snr_db
    noise_watts=10 ** (noise_db/10)
    mean_noise=0
    noise=np.random.normal(mean_noise, np.sqrt(noise_watts),len(signal))
    noise_signal = signal+noise
    return noise_signal
