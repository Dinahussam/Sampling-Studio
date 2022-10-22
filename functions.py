import re
from telnetlib import X3PAD
from tkinter import Y
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.graph_objects as go
import plotly.express as px
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

x_Time = np.arange(0, 2, 2/1000).tolist()  # Time Axis Array

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

def updateFigLayout(fig):
    fig.update_layout(
        # autosize=False,
        width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
    )
    return fig

def toFreqDomain(yt):
    y_f = np.fft.fft(yt)
    x_f = np.linspace(0.0, 2/(2.0*(2/1000)), 1000//2).tolist()
    return y_f, x_f  

def sampling(factor):
    samp_frq=(factor)* max(Functions.ADDED_FREQUENCES)
    time_range=math.ceil(x_Time[-1]-x_Time[0])
    samp_rate=int((len(x_Time)/time_range)/samp_frq)
    samp_time=x_Time[::samp_rate]
    samp_amp= Functions.Current_amplitude[::samp_rate]
    return samp_time,samp_amp

def sinc_interp(factor):
    samp_time,samp_amp=sampling(factor)
    time_matrix= np.resize(x_Time,(len(samp_time),len(x_Time)))
    k= (time_matrix.T - samp_time)/(samp_time[1]-samp_time[0])
    resulted_matrix = samp_amp* np.sinc(k)
    reconstucted_seg= np.sum(resulted_matrix, axis=1)
    y_f,x_f = toFreqDomain(reconstucted_seg)
    return  go.Figure([go.Scatter(x=x_Time, y=reconstucted_seg)]) , go.Figure([go.Scatter(x=x_f, y=y_f)]) 