import math
import numpy as np  
import pandas as pd  
import plotly.graph_objects as go
import plotly.express as px

# constructing the Signals
class Functions:
    #number of signals added
    numberSignalsAdded=-1
    #lists of added features of the Signals
    addedFreqs=[]
    addedAmps=[]
    addedPhases=[]
    addedSignals=[]
    composedAmp=np.zeros(1000)

tmax=1
n=1000
mainTimeAxis = np.linspace(0, tmax, n).tolist()  # Time Axis Array for all of the graphs

def show_sin (magnitude, phase, frequency):  # Add new sin Signal
    Y = np.zeros(1000)  # Array for saving sin Signals values
    for i in range(1000): 
        Y[i] = (magnitude * (math.sin((2 * np.pi * frequency * mainTimeAxis[i]) + phase)))
    return go.Figure([go.Scatter(x=mainTimeAxis, y=Y)])

def show_composed():  # Add new sin Signal
    return go.Figure([go.Scatter(x=mainTimeAxis, y=Functions.composedAmp)])

def add_signal(added_magnitude, added_phase,added_frequency):
    new_y_amplitude = np.zeros(1000)  # Array for saving sin Signals values
    for i in range(1000): 
        new_y_amplitude[i] = (added_magnitude * (math.sin((2 * np.pi * added_frequency * mainTimeAxis[i]) + added_phase))) 
    
    #updating lists
    Functions.numberSignalsAdded+=1
    Functions.addedFreqs.append(added_frequency)
    Functions.addedAmps.append(added_magnitude)
    Functions.addedPhases.append( added_phase)
    Functions.addedSignals.append(new_y_amplitude)
    Functions.composedAmp=np.add(Functions.composedAmp,new_y_amplitude)

    return go.Figure([go.Scatter(x=mainTimeAxis, y=Functions.composedAmp)])

def delete_signal(index_todelete): 

    if(Functions.numberSignalsAdded==0):
        clean_all()
        return go.Figure([go.Scatter(x=mainTimeAxis, y=Functions.composedAmp)])
    else:
        Functions.composedAmp=np.subtract(Functions.Current_amplitude,Functions.ADDED_SIGNALS[index_todelete] ) 
        Functions.addedAmps.pop(index_todelete)
        Functions.addedFreqs.pop(index_todelete)
        Functions.addedPhases.pop(index_todelete)
        Functions.addedSignals.pop(index_todelete)
        Functions.numberSignalsAdded-=1
        
        return go.Figure([go.Scatter(x=mainTimeAxis, y=Functions.composedAmp)])

def upload_signal(Clean_flag,frequinces,amplitudes,phases,numberOfSignals):
    # def upload_signal(Clean_flag,amp):
    if Clean_flag==1:
        clean_all()
    #updating lists
    num=int(numberOfSignals[0])
    
    for i in range(0,num):
        add_signal(amplitudes[i], phases[i],frequinces[i])
    return go.Figure([go.Scatter(x=mainTimeAxis, y=Functions.composedAmp)])

def save_signal(file_name):
    graph_axises = pd.DataFrame({'time':mainTimeAxis,'amp':Functions.composedAmp})
    graph_detials = pd.DataFrame({ 
        'frequencies':Functions.addedFreqs,
        'amplitudes':Functions.addedAmps,
        'phases':Functions.addedPhases,
        'numberOfSignals':Functions.numberSignalsAdded+1
        })
    graph = pd.concat([graph_axises, graph_detials], axis=1) 
    file_name=file_name+'.csv'   
    df = pd.DataFrame(graph) 
    # saving the dataframe 
    df.to_csv( file_name) 
    
def add_noise(addFlag, snrRatio):
    power = Functions.composedAmp**2
    snr_db = 10 * np.log10(snrRatio)
    signal_avg_power=np.mean(power)
    signal_avg_power_db=10 * np.log10(signal_avg_power)
    noise_db=signal_avg_power_db - snr_db
    noise_watts=10 ** (noise_db/10)
    mean_noise=0
    noise=np.random.normal(mean_noise, np.sqrt(noise_watts),len(Functions.composedAmp))
    if(addFlag):
        Functions.composedAmp = Functions.composedAmp+noise
        fig=go.Figure([go.Scatter(x=mainTimeAxis, y=Functions.composedAmp)])
    else:
        noised_signal = Functions.composedAmp+noise
        fig =go.Figure([go.Scatter(x=mainTimeAxis, y=noised_signal)])
    return fig

def layout_fig(fig):
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

def clean_all():
    #number of Signals added
    Functions.numberSignalsAdded=-1
    #lists of added features of the Signals
    Functions.addedFreqs=[]
    Functions.addedAmps=[]
    Functions.addedPhases=[]
    Functions.addedSignals=[]
    Functions.composedAmp=np.zeros(1000)
    Functions.composedAmp=np.zeros(1000)

# sampling , interpolation & converting to Freq domain 
def tofrqDomain_converter(yt):
    fs= n/tmax  
    fstep= fs/n
    f= np.linspace(0, (n-1)*fstep , n)
    yf_mag= np.abs(np.fft.fft(yt)) / n
    f_plot= f[0: int(n/2+1) ]
    y_f= 2 * yf_mag[0: int(n/2+1)]
    y_f[0]= y_f[0]/2   #dc component does't need to be multiplied by 2
    return f_plot , y_f

def sampling(samp_frq):
    # samp_frq=(factor)* max(Functions.addedFreqs)
    time_range=math.ceil(mainTimeAxis[-1]-mainTimeAxis[0])
    samp_rate=int((len(mainTimeAxis)/time_range)/samp_frq)
    samp_time=mainTimeAxis[::samp_rate]
    samp_amp= Functions.composedAmp[::samp_rate]
    return samp_time,samp_amp

def sinc_interp(samp_freq):
    samp_time,samp_amp=sampling(samp_freq)
    time_matrix= np.resize(mainTimeAxis,(len(samp_time),len(mainTimeAxis))) # to be able to sabstract nT from t
    k= (time_matrix.T - samp_time)/(samp_time[1]-samp_time[0]) 
    resulted_matrix = samp_amp* np.sinc(k)
    reconstucted_seg= np.sum(resulted_matrix, axis=1)
    reconstructed_fig = px.line(x=mainTimeAxis , y= reconstucted_seg)
    samplingPoints_fig = px.scatter(x=samp_time, y=samp_amp ,color_discrete_sequence=["red"],)
    x_f, y_f = tofrqDomain_converter(reconstucted_seg)
    return go.Figure(data = reconstructed_fig.data + samplingPoints_fig.data), go.Figure([go.Scatter(x=x_f, y=y_f)])

