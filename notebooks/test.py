import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

import mne
from mne.channels import read_layout

board_id = BoardIds.GANGLION_BOARD.value
eeg_channels = BoardShim.get_eeg_channels(board_id)

df = pd.read_csv("../data/ganglion.csv", sep=",")

channels_columns = ["chan {}".format(i+1) for i in range(len(eeg_channels))]
# BrainFlow returns uV, convert to V for MNE
df[channels_columns] = df[channels_columns].apply(lambda x: x/1000000 , axis=1)
ch_types = ['eeg'] * len (eeg_channels)
# ch_names = BoardShim.get_eeg_names(board_id)
sfreq = BoardShim.get_sampling_rate(board_id)
info = mne.create_info(ch_names = ['C3', 'C4', 'F3', 'F4'], sfreq = sfreq, ch_types = ch_types)
raw = mne.io.RawArray(np.transpose(df[channels_columns].to_numpy()), info)
# raw.plot(n_channels=4, scalings='auto', show=True, block=True)

info = mne.create_info(['STI 1', 'STI 2'], raw.info['sfreq'], ['stim', 'stim'])
stim_raw = mne.io.RawArray(np.transpose(df[['stim_channel1', 'stim_channel2']]), info)
raw.add_channels([stim_raw], force_update_info=True)
# raw.copy().pick_types(eeg=False, stim=True).plot(show=True, block=True)

# events = mne.find_events(raw, stim_channel=['STI 1', 'STI 2'])
events = mne.find_events(raw, stim_channel='STI 1')
raw.plot(n_channels=4, events=events, scalings='auto', show=True, block=True)