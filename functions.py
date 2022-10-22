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
import math
import matplotlib.pyplot as plt
import pandas as pd  
  


class Functions:
    #number of signals added
    numberSignalsAdded=-1
    #lists of added features of the signals
    ADDED_FREQUENCES=[]
    ADDED_AMPLITUDES=[]
    ADDED_PHASES=[]
    ADDED_SIGNALS=[]
    amplitude_SUM = np.zeros(1000)  # Sum of AMPLITUDE of signals
    Current_amplitude=np.zeros(1000)


x_Time = np.arange(0, 2, 2/1000).tolist()  # Time Axis Array for all of the graphs

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
    # print(Functions.ADDED_FREQUENCES)
    # # print(Functions.ADDED_SIGNALS)
    # print(Functions.numberSignalsAdded)
    

    return go.Figure([go.Scatter(x=x_Time, y=Functions.Current_amplitude)])
# function name:DELETE_SIGNAL
# input: a flag that indecates if it is the last signal to be deleted or not 
# output: it returns the figure after deleteing the signal .
# describtion: it clear the resulted signal if it is the last signal ,
#              if not it will subtract it from current resu;ted signal
def DELETE_SIGNAL(index_todelete): 

    if(Functions.numberSignalsAdded==0):
        Clean_intialize()
        return go.Figure([go.Scatter(x=x_Time, y=Functions.Current_amplitude)])
    else:
        print(type(Functions.ADDED_SIGNALS[index_todelete]))

        Functions.Current_amplitude=np.subtract(Functions.Current_amplitude,Functions.ADDED_SIGNALS[index_todelete] ) 
        Functions.ADDED_FREQUENCES.pop(index_todelete)
        Functions.ADDED_AMPLITUDES.pop(index_todelete)
        Functions.ADDED_PHASES.pop(index_todelete)
        Functions.ADDED_SIGNALS.pop(index_todelete)
        Functions.numberSignalsAdded-=1


        return go.Figure([go.Scatter(x=x_Time, y=Functions.Current_amplitude)])

def Uploaded_signal(Clean_flag,amp,frequinces,amplitudes,phases,numberOfSignals):
    # def Uploaded_signal(Clean_flag,amp):
    if Clean_flag==1:
        Clean_intialize()
    #updating lists
    num=int(numberOfSignals[0])
    
    for i in range(0,num):
        ADD_SIGNAL(amplitudes[i], phases[i],frequinces[i])
    return go.Figure([go.Scatter(x=x_Time, y=Functions.Current_amplitude)])

def save_signal(file_name):

    graph_axises = pd.DataFrame({'time':x_Time,'amp':Functions.Current_amplitude})
    graph_detials = pd.DataFrame({ 
        'frequencies':Functions.ADDED_FREQUENCES,
        'amplitudes':Functions.ADDED_AMPLITUDES,
        'phases':Functions.ADDED_PHASES,
        'numberOfSignals':Functions.numberSignalsAdded+1
        })

    graph = pd.concat([graph_axises, graph_detials], axis=1) 
    file_name=file_name+'.csv'   
    df = pd.DataFrame(graph) 
    # saving the dataframe 
    df.to_csv( file_name) 
    
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
        sampling_y.append(np.interp(point, Functions.Current_amplitude,x_Time))
    return(sampling_y)

def sampling(factor):
    samp_frq=(factor)* max(Functions.ADDED_FREQUENCES)
    time_range=math.ceil(x_Time[-1]-x_Time[0])
    samp_rate=int((len(x_Time)/time_range)/samp_frq)
    samp_time=x_Time[::samp_rate]
    samp_amp= Functions.Current_amplitude[::samp_rate]
    return samp_time,samp_amp

    # sincM = np.tile(sampling_time, (len(x_timeArr), 1)) - np.tile(x_timeArr[:, np.newaxis], (1, len(sampling_time)))
    # sampling_y= np.tile(sampling_y, (len(sampling_time), len(x_timeArr)))
    # newy = np.dot(sampling_y, np.sinc(sincM/T))
    # return go.Figure([go.Scatter(x=x_timeArr, y=newy)])




def sinc_interp(factor):
    samp_time,samp_amp=sampling(factor)
    time_matrix= np.resize(x_Time,(len(samp_time),len(x_Time)))
    k= (time_matrix.T - samp_time)/(samp_time[1]-samp_time[0])
    resulted_matrix = samp_amp* np.sinc(k)
    reconstucted_seg= np.sum(resulted_matrix, axis=1)
    return  go.Figure([go.Scatter(x=x_Time, y=reconstucted_seg)])

# def sinc_interp(factor):
#     samp_time,samp_amp=sampling(factor)
#     time_matrix= np.resize(x_Time,(len(samp_time),len(x_Time)))
#     k= (time_matrix.T - samp_time)/(samp_time[1]-samp_time[0])
#     resulted_matrix = samp_amp* np.sinc(k)
#     reconstucted_seg= np.sum(resulted_matrix, axis=1)

#     return  go.Figure([go.Scatter(x=x_Time, y=reconstucted_seg)])

# function name:Clean_initialize
# input: no input
# output: no return value
# describtion: it clear all the lists and intilize the graphs (i.e restart)
def Clean_intialize():
    #number of signals added
    Functions.numberSignalsAdded=-1
    #lists of added features of the signals
    Functions.ADDED_FREQUENCES=[]
    Functions.ADDED_AMPLITUDES=[]
    Functions.ADDED_PHASES=[]
    Functions.ADDED_SIGNALS=[]
    Functions.amplitude_SUM = np.zeros(1000)  # Sum of AMPLITUDE of signals
    Functions.Current_amplitude=np.zeros(1000)