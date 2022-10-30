# Sampling Studio 
![repo 1-1](https://github.com/alaayasser01/DSP_Task1_14/blob/main/photos/home.jpg)
## Description:
our web application about signal sampling or nyequist theroem which defines the min sample rate for highest frequency, it is principle to reproduce pure waves which must be at least twice its frequency. it is show how add, delete, generate signal and show noise.

## Table of contents

* [Features](#features)
* [File_structure](#file_structure)
* [Technology_used](#technology_used)

## Features
* [Generate signal](#generate_signal)
* [Add_SNR](#add_snr)
* [Save signal as CSV file](#save_signal_as_CSV_file)
* [Sampling and recover signal](#sampling_and_recover_signal)
* [Save signal as png photo](#save_signal_as_png_photo)
* [Zoom in and out](#zoom_in_and_out)

### Generate_signal:
You can generate a signal by choosing the frequency, amplitude, and phase shift that you want to generate it or upload it from your browser and also you can add several signals to each other to generate a new signal from them.

![repo 1-1](https://github.com/alaayasser01/DSP_Task1_14/blob/main/photos/generate.jpg)


### Add_SNR:
You can add SNR and showing how the noise changes the signal.

![repo 1-1](https://github.com/alaayasser01/DSP_Task1_14/blob/main/photos/snr.jpg)


### Save_signal_as_CSV_file:
You can save your signal as CSV file in your browser and you can complete your process in your signal when you upload it.

![repo 1-1](https://github.com/alaayasser01/DSP_Task1_14/blob/main/photos/save.jpg)


### Sampling_and_recover_signal:
You can show max frequency and changing sample frequency, show over-sampling and aliasing conditions.

![repo 1-1](https://github.com/alaayasser01/first-dsp-task/blob/main/photos/sampling.png)


### Save_signal_as_png_photo:
You can save the signal as png photo in your browser.

![repo 1-1](https://github.com/alaayasser01/DSP_Task1_14/blob/main/photos/dwonload_png.png)


### Zoom_in_and_out:
You can zoom in and out in your signal.

![repo 1-1](https://github.com/alaayasser01/DSP_Task1_14/blob/main/photos/zoom_in.jpg)
![repo 1-1](https://github.com/alaayasser01/DSP_Task1_14/blob/main/photos/zoom_out.jpg)


## File_structure:
We have only 2 files one is the main file where we run the whole ui and call the required functions 
the other is the fuctions file which devided into 3 sections : 
1- the signal composer (add/delete /snr /...). 
2- the sampling &interpolation section.
3- downloading & uploading.


## Technology_used:
Streamlit link.
