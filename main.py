import functions
from telnetlib import X3PAD
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import plotly.graph_objects as go
import streamlit as st  # 🎈 data web app development
import csv

from pandas import *


# general styling and tab name
st.set_page_config(
    page_title="Sampling Studio",
    page_icon="✅",
    layout="wide",
)
 
# title
st.title("Sampling studio")
st.write("our web application about signal sampling or nyequist theroem which defines the min sample rate for highest frequency, it is principle to reproduce pure waves which must be at least twice its frequency. it is show how add, delete, generate signal and show noise")
  
#initiating df(dataframe) and empty fig
TOADD_fig= px.density_heatmap(
         data_frame=[{}])
samp_fig= px.density_heatmap(
         data_frame=[{}])
sampfreq_fig=  px.density_heatmap(
         data_frame=[{}])
res_fig= px.density_heatmap(
         data_frame=[{}])
TOADD_fig= functions.updateFigLayout(TOADD_fig)
samp_fig= functions.updateFigLayout(samp_fig)
sampfreq_fig= functions.updateFigLayout(sampfreq_fig)
res_fig= functions.updateFigLayout(res_fig)




res_fig=functions.SHOW_RES()
res_fig= functions.updateFigLayout(res_fig)

#sidebar components
with st.sidebar:
    # st.title('Generate, reconstruct and sample your signal')
    tab_gen,tab_snr, tab_del, tab_save, tab_samp = st.tabs(["Generate", "SNR" ,"Delete","Save" ,"Sample"])

    with tab_gen:
        frq_value =st.number_input('signal frequancy', min_value= 0.01,value=1.0, step=1.0)
        amplitude_value =st.number_input('signal amplitude', min_value= 0.01,value=1.0, step=1.0)
        phase_value     =st.number_input('phase shift', min_value= 0,max_value=360,value=0, step=5)
        if st.button('ADD signal'):
            res_fig=functions.ADD_SIGNAL(amplitude_value,phase_value,frq_value)
            res_fig= functions.updateFigLayout(res_fig)
            
        uploaded_file =st.file_uploader('upload the signal file',['csv'] , help='upload your signal file' )
        if(uploaded_file):
            df = pd.read_csv(uploaded_file)
            if st.button('Upload to existing'):
                res_fig=functions.Uploaded_signal(0,df['amp'],df['frequencies'],df['amplitudes'],df['phases'],df['numberOfSignals'])
            if st.button('Clear then upload'):
                res_fig=functions.Uploaded_signal(1,df['amp'],df['frequencies'],df['amplitudes'],df['phases'],df['numberOfSignals'])

    with tab_snr:
        snr_value =st.slider('SNR ratio',0 , 10000,10000)
        res_fig=functions.SHOW_NOISE(snr_value)     
        res_fig= functions.updateFigLayout(res_fig)

        if st.button('ADD noise'):
            res_fig=functions.ADD_NOISE(snr_value)
            res_fig= functions.updateFigLayout(res_fig)
            st.success("File is saved successfully as " + file_name + ".csv", icon="✅")
#             st.balloons()
            
    with tab_del:
        if(len(functions.Functions.ADDED_SIGNALS)):
            todelete_list=[]
            for signal in range(len(functions.Functions.ADDED_SIGNALS)):
                todelete_list.append(f"freq={functions.Functions.ADDED_FREQUENCES[signal]}, amp={functions.Functions.ADDED_AMPLITUDES[signal] }, phase={functions.Functions.ADDED_PHASES[signal]}",)
            todelete_list=st.multiselect("choose the signal you want to delete",options=todelete_list,key='disabled' ,default=None)
            if st.button(' DELETE '):
                for todeleteSigindex in range(len(todelete_list)):
                    if(todelete_list[todeleteSigindex]):
                        functions.DELETE_SIGNAL(todeleteSigindex)
        else:
            st.title("You have no added signals to delete")

    
    # with tab_save: 
    #     file_name=st.text_input('Write file name to be saved')
    #     if st.button('Save the current constructed signal'): 
    #         functions.save_signal(file_name)       
    # #     if(len(functions.Functions.ADDED_FREQUENCES)>0):
    #         maxFreq= max(functions.Functions.ADDED_FREQUENCES)
    #         st.title(f'max freq= {maxFreq}') 
    #         st.write('the sampling freq = sampling factor*max feq')
    #         samp_factor= st.slider('sampling factor', 0.0 , 20.0 , 2.0, 0.5)
    #         samp_fig=functions.sinc_interp(samp_factor)
    #     else:
    #         st.title("Construct your signal you want to sample first")
        


# if(uploaded_file):
#     df = pd.read_csv(uploaded_file)
#     TOADD_fig= go.Figure([go.Scatter(x=df['time'], y=df['amp'],)])
# else:
    with tab_samp:
        if(len(functions.Functions.ADDED_FREQUENCES)>0):
            maxFreq= max(functions.Functions.ADDED_FREQUENCES)
            st.title(f'max freq= {maxFreq}') 
            st.write('the sampling freq = sampling factor*max feq')
            samp_freq= st.slider('sampling freq', min_value=  1.000001 , value= 1.000001, max_value=10*maxFreq)
            st.write(f'Your sampling factor = {samp_freq/maxFreq}')
            samp_fig, sampfreq_fig =functions.sinc_interp(samp_freq)
            samp_fig= functions.updateFigLayout(samp_fig)
            sampfreq_fig= functions.updateFigLayout(sampfreq_fig)
        else:
            st.title("Construct your signal you want to sample first")
        
    
TOADD_fig=functions.SHOW_SIN(amplitude_value,phase_value ,frq_value )
TOADD_fig= functions.updateFigLayout(TOADD_fig)


#STREAMLIT COLUMNS AND ROWS 
composer_cont= st.container()
sampling_cont= st.container()

with composer_cont:

    st.markdown("## Constructing your signal")
    fig_toadd ,fig_res = st.columns((2))
    
    with fig_toadd:
        st.markdown("#### Generated signal")
        st.write(TOADD_fig)
    
    with fig_res:
        st.markdown("#### Resulted signal")
        st.write(res_fig)     

with sampling_cont:
    
    st.markdown("## Sampling the resulted signal")
    fig_sampled, fig_freqsampled = st.columns((2))
        
    with fig_sampled:
        st.markdown("#### time domain")
        st.write(samp_fig)

    with fig_freqsampled:
        st.markdown("#### freq domain")
        st.write(sampfreq_fig)
