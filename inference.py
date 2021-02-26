import matplotlib
from scipy.io.wavfile import write

matplotlib.use('Agg')
import matplotlib.pylab as plt
import IPython.display as ipd
import sys
import os
sys.path.append('waveglow/')
import numpy as np
import torch

from hparams import create_hparams
from model import Tacotron2
from layers import TacotronSTFT, STFT
from audio_processing import griffin_lim
from train import load_model
from text import text_to_sequence
from waveglow.denoiser import Denoiser


def plot_data(data, figsize=(16, 4)):
    fig, axes = plt.subplots(1, len(data), figsize=figsize)
    for i in range(len(data)):
        axes[i].imshow(data[i], aspect='auto', origin='bottom',
                       interpolation='none')

def inference():
    hparams = create_hparams()
    hparams.sampling_rate = 22050


    checkpoint_path = "./output2/checkpoint_16000_male.pt"
    model = load_model(hparams)
    model.load_state_dict(torch.load(checkpoint_path)['state_dict'])
    _ = model.cuda().eval()


    waveglow_path =  './waveglow/nvidia_waveglowpyt_fp32_20190427'
    waveglow = torch.load(waveglow_path)['state_dict']
    waveglow.to('cuda').eval()
    # for k in waveglow.convinv:
    #     k.float()
    denoiser = Denoiser(waveglow)

    text = "Xin chào các bạn"
    sequence = np.array(text_to_sequence(text, ['basic_cleaners']))[None, :]
    print(sequence)
    # sequence = torch.autograd.Variable(
    #     torch.from_numpy(sequence)).cuda().long()
    sequence = torch.from_numpy(sequence).to(device='cuda', dtype=torch.int64)
    print(sequence)


    with torch.no_grad():
        mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
        print(mel_outputs_postnet)
        # plot_data((mel_outputs.float().data.cpu().numpy()[0],
        #            mel_outputs_postnet.float().data.cpu().numpy()[0],
        #            alignments.float().data.cpu().numpy()[0].T))
        audio = waveglow.infer(mel_outputs_postnet)
    audio_numpy = audio[0].data.cpu().numpy()
    #ipd.Audio(audio[0].data.cpu().numpy(), rate=hparams.sampling_rate)
    write("demo2.wav", hparams.sampling_rate, audio_numpy.astype('int16'))

inference()