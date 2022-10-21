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
st.text("Change Your analog Signal into digital & See How the Sampling frequancy affect")
  
#initiating df(dataframe) and empty fig
TOADD_fig= px.density_heatmap(
         data_frame=[{}])
samp_fig= px.density_heatmap(
         data_frame=[{}])
res_fig= px.density_heatmap(
         data_frame=[{}])

res_fig=functions.SHOW_RES()
#sidebar components
with st.sidebar:
    # st.title('Generate, reconstruct and sample your signal')
    tab0,tab1, tab2, tab3 = st.tabs(["Generate","Delete", "SNR" , "Sample"])
    with tab0:
        frq_value =st.number_input('signal frequancy', min_value= 0.0,value=0.0, step=1.0)
        amplitude_value =st.number_input('signal amplitude', min_value= 0.01,value=1.0, step=1.0)
        phase_value     =st.number_input('phase shift', min_value= 0,max_value=360,value=0, step=5)
        if st.button('ADD signal'):
            res_fig=functions.ADD_SIGNAL(amplitude_value,phase_value,frq_value)
    with tab1:
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
    with tab2:
        snr_value =st.slider('SNR ratio',0 , 10000,10000)
        res_fig=functions.SHOW_NOISE(snr_value)     
        if st.button('ADD noise'):
            res_fig=functions.ADD_NOISE(snr_value)
    with tab3: 
        if(len(functions.Functions.ADDED_FREQUENCES)>0):
            maxFreq= max(functions.Functions.ADDED_FREQUENCES)
            st.title(f'max freq= {maxFreq}') 
            st.write('the sampling freq = sampling factor*max feq')
            samp_factor= st.slider('sampling factor', 1 , 20, 2, 1)
            samp_fig=functions.sinc_interp(samp_factor)
        else:
            st.title("Construct your signal you want to sample first")


TOADD_fig=functions.SHOW_SIN(amplitude_value,phase_value ,frq_value )


#STREAMLIT COLUMNS AND ROWS 
# fig_uploaded,fig_sampled= st.columns((2))
empty1, fig_toadd ,emplty2, empty3 = st.columns((4))
empty1, fig_res ,emplty2, empty3 = st.columns((4))
empty1, fig_sampled ,emplty2, empty3 = st.columns((4))
 
with fig_toadd:
    st.markdown("### Generating a signal")
    st.write(TOADD_fig)
 
with fig_res:
    st.markdown("### Resulted signal")
    st.write(res_fig)    
 
with fig_sampled:
    st.markdown("### Sampled signal")
    st.write(samp_fig)

