import numpy as np
Fs=44100



D_note=1/80

Notes=["C2"]
N_note=len(Notes)
N_note_echo=int(1/D_note)


L_note=int(Fs*D_note)
L=L_note*N_note*N_note_echo
data=np.zeros((L),np.float32)
index=np.linspace(0,D_note-1/Fs,L_note)
x=np.linspace(0,L-1,L)/Fs
#############################################################################

N_ptr=0
L_ptr=0

#############################################################################
NOTE_FREQ_TABLE={
    "C2":64.23,
    "C2D2":69.2957,
    "D2":73.4162,
    "D2E2":77.7817,
    "E2":82.4069,
    "F2":87.3071,
    "F2G2":92.4986,
    "G2": 97.9989,
    "G2A2":103.826,
    "A2":110.000,
    "A2B2":116.541,
    "B2":123.471,
    "C3":130.813,
    "C3D3":138.591,
    "D3": 146.832,
    "D3E3":155.563,
    "E3":164.814,
    "F3":174.614,
    "F3G3":184.997,
    "G3":195.998,
    "G3A3":207.652,
    "A3":220.000,
    "A3B3":233.082,
    "B3":246.942,
    "C4":261.626,
    "C4D4":277.183,
    "D4":293.665,
    "D4E4":311.127,
    "E4":329.628,
    "F4":349.228,
    "F4G4":369.994,
    "G4":391.995,
    "G4A4":415.305,
    "A4":440.000,
    "A4B4":466.164,
    "B4":493.883,
    "C5":523.251,
    "C5D5":554.365,
    "D5":587.330,
    "D5E5":622.254,
    "E5":659.255,
    "F5":698.456,
    "F5G5":739.989,
    "G5":783.991,
    "G5A5":830.609,
    "A5":880.000,
    "A5B5":932.328,
    "B5":987.767,
    "C6":1046.50,
    "C6D6":1108.73,
    "D6":1174.66,
    "D6E6":1244.51,
    "E6":1318.51,
    "F6":1396.91,
}

#############################################################################
def note2f(note,rep:int):
    return 4.5*NOTE_FREQ_TABLE[note]


N_note_echo_A=int(N_note_echo*32/256)
N_note_echo_B=int(N_note_echo*64/256)
N_note_echo_C=int(N_note_echo*180/256)
N_note_echo_D=int(N_note_echo*256/256)

N_note_echo_level_alpha=1
N_note_echo_level_beta=0.7

def noteAmpRep(rep:int):
    if   rep>=0 and rep<=N_note_echo_A:
        return N_note_echo_level_alpha*rep/N_note_echo_A
    elif rep>=N_note_echo_A and rep<=N_note_echo_B:
        return N_note_echo_level_alpha+(N_note_echo_level_beta-N_note_echo_level_alpha)*(rep-N_note_echo_A)/(N_note_echo_B-N_note_echo_A)
    elif rep>=N_note_echo_B and rep<=N_note_echo_C:
        return N_note_echo_level_beta
    elif rep>=N_note_echo_C and rep<=N_note_echo_D:
        return N_note_echo_level_beta+(0-N_note_echo_level_beta)*(rep-N_note_echo_C)/(N_note_echo_D-N_note_echo_C)
    else:
        return 0


#############################################################################


for note in Notes:
    ################################################################
    #       Freq Apply Machine
    rep_ptr=L_ptr
    for rep in range(N_note_echo):
        f=note2f(note,rep)
        a=noteAmpRep(rep)
        data[rep_ptr:rep_ptr+L_note]+=a*np.sin(index*2*f*np.pi)+0.9*a*np.sin(index*2*2*f*np.pi)+a*0.7*np.sin(index*2*4*f*np.pi)+a*0.5*np.sin(index*2*8*f*np.pi)
        rep_ptr+=L_note
    ################################################################
    N_ptr+=1
    L_ptr+=L_note
    if N_ptr>=(N_note-N_note_echo):
        break

###########################################################################
x=np.linspace(0,len(data)-1,len(data))/Fs
import matplotlib.pyplot as plt

plt.plot(x,data)
plt.show()
Data=np.fft.fft(data)
plt.plot(x,Data)
plt.show()
"""
############################################################################
FOUT="sound.wav"
amx=data.max()
ami=data.min()
mx=max(abs(ami),abs(amx))
if mx==0:
    mx=1
output_bytes = (32760*data/mx).astype(np.int16).tobytes()
import wave
audio=wave.open(FOUT,"wb")
audio.setframerate(Fs)
audio.setnchannels(1)
audio.setsampwidth(2)
audio.writeframesraw(output_bytes)
audio.close()
"""