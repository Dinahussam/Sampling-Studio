from statistics import mode
from turtle import color
import functions
import pandas as pd 
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import plotly.graph_objects as go




# general styling and tab name
st.set_page_config(
    page_title="Sampling Studio",
    page_icon="✅",
    layout="wide",
)

# styles from css file
with open(r"style.css") as design:
    st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)
 
# title
st.title("Sampling studio")
# st.write("This application is used to show how applying different frequencies affects signal sampling and recovering  according to nyquist theorem and Sinc interpolation ")

# Save and upload

#end of Save and upload

#initiating df(dataframe) and empty fig
toadd_fig= px.density_heatmap(
         data_frame=[{}])
composed_fig= px.density_heatmap(
         data_frame=[{}])
samp_fig= px.density_heatmap(
         data_frame=[{}])
sampfreq_fig=  px.density_heatmap(
         data_frame=[{}])
shown_fig=  px.density_heatmap(
         data_frame=[{}])
shown_fig=go.Figure()

toadd_fig= functions.layout_fig(toadd_fig)
composed_fig= functions.layout_fig(composed_fig)
samp_fig= functions.layout_fig(samp_fig)
sampfreq_fig= functions.layout_fig(sampfreq_fig)
composed_fig=functions.show_composed()
composed_fig= functions.layout_fig(composed_fig)
shown_fig= functions.layout_fig(shown_fig)

sampling_freq=00.1

functions.default_fun()
#sidebar components
with st.sidebar:

    col_upload, empty=st.columns([2, 2])
    
    uploaded_file = st.file_uploader('upload the Signal file', ['csv'], help='upload your Signal file', label_visibility='collapsed')
    if (uploaded_file):
        df = pd.read_csv(uploaded_file)
        if col_upload.button('Upload to existing'):
            composed_fig = functions.upload_signal(0, df['frequencies'], df['amplitudes'], df['phases'],
                                                    df['numberOfSignals'])
        if st.button('Clear then upload'):
            composed_fig = functions.upload_signal(1, df['frequencies'], df['amplitudes'], df['phases'],
                                                    df['numberOfSignals'])




    col_freq, col_amp, col_phase, col_add = st.columns([2, 2, 2,2])
    frq_value = col_freq.number_input('frequancy', min_value=0.01, value=1.0, step=1.0)
    amplitude_value = col_amp.number_input('amplitude', min_value=0.01, value=1.0, step=1.0)
    phase_value = col_phase.number_input('phase shift', min_value=0, max_value=360, value=0, step=5)
    col_add.write('')
    col_add.write('')
    if col_add.button('ADD Signal'):
        composed_fig = functions.add_signal(amplitude_value, phase_value, frq_value)
        composed_fig = functions.layout_fig(composed_fig)
    st.write("SNR:")
    col_snr_slider, col_space, col_btn_noise = st.columns([5.5,0.5, 2])
    snr_value = col_snr_slider.slider('SNR ratio', 0, step=1, max_value=10000, value=10000, label_visibility='collapsed')
    if (snr_value != 10000):
        composed_fig = functions.add_noise(False, snr_value)
    composed_fig = functions.layout_fig(composed_fig)

    if col_btn_noise.button('ADD noise'):
        composed_fig = functions.add_noise(True, snr_value)
        composed_fig = functions.layout_fig(composed_fig)

    col_choose_delete,col_space ,col_btn_delete = st.columns([6,0.5, 2])
    if (len(functions.Functions.addedSignals)):
        todelete_list = []
        for signal in range(len(functions.Functions.addedSignals)):
            todelete_list.append(
                f"freq={functions.Functions.addedFreqs[signal]}, amp={functions.Functions.addedAmps[signal]}, phase={functions.Functions.addedPhases[signal]}", )
        todelete_list = col_choose_delete.multiselect("choose the signal you want to delete", options=todelete_list, key='disabled',label_visibility='collapsed',
                                       default=None)
    
       
        if col_btn_delete.button(' DELETE '):
            for todeleteSigindex in range(len(todelete_list)):
                if (todelete_list[todeleteSigindex]):
                    functions.delete_signal(todeleteSigindex)
    else:
        st.title("You have no added signals to Sample or Delete")

    if (len(functions.Functions.addedFreqs) > 0):
        maxFreq = max(functions.Functions.addedFreqs)
        samp_freq = st.slider('sampling freq', min_value=1, value=1, max_value=10 * int(maxFreq))
        # st.write(f"note: current max freq= {maxFreq}")
        samp_fig, sampfreq_fig = functions.sinc_interp(samp_freq)
        samp_fig = functions.layout_fig(samp_fig)
        sampfreq_fig = functions.layout_fig(sampfreq_fig)
   
   
        file_name = st.text_input('Write file name to be saved')
        if st.button('Save the current resulted Signal'):
            functions.save_signal(file_name)
            # st.success("File is saved successfully as " + file_name + ".csv", icon="✅")
        
    
toadd_fig=functions.show_sin(amplitude_value,phase_value ,frq_value )
toadd_fig= functions.layout_fig(toadd_fig)


#STREAMLIT COLUMNS AND ROWS 


# Selecting graph
options=[0,0,0,0]

composer_cont= st.container()
col_check,col_figure=st.columns([1,4])

Y_toaddfig=toadd_fig.data[0]['y']
Y_composed_fig=composed_fig.data[0]['y']
Y_samp_fig=samp_fig.data[0]['y']
time,Y_samp_points=functions.sampling(sampling_freq)

with composer_cont:
    with col_check:
        st.write('')
        st.write('')
        st.write('')
        st.markdown("## Signal Mixer")
        options[0]=st.checkbox('Generated signal', value=False)

        options[1]=st.checkbox('composed signal', value=True)

        options[2]=st.checkbox('Sampled signal', value=False)

        options[3]=st.checkbox('Sampling points', value=False)

    
    with col_figure:
        
        if(options[0]):
            shown_fig.add_trace(go.Scatter(x=functions.Functions.commonXaxis ,y=Y_toaddfig , name= 'generated signal'))
        if(options[1]):
            shown_fig.add_trace(go.Scatter(x=functions.Functions.commonXaxis ,y=Y_composed_fig , name='composed signal'))
        if(options[2]):
            shown_fig.add_trace(go.Scatter(x=functions.Functions.commonXaxis ,y=Y_samp_fig , name='interpolated signal'))
        if(options[3]):
            if(len(functions.Functions.addedSignals)>0):
                samp_time, samp_frq= functions.sampling(samp_freq)
                shown_fig.add_trace(go.Scatter(x=samp_time , y= samp_frq, mode="markers" ,name='sampling points'))
            else:
                 shown_fig.add_trace(go.Scatter(x=functions.Functions.commonXaxis ,y=Y_samp_fig , name='interpolated signal'))
        st.write(shown_fig)    
# end of selecting graphs






