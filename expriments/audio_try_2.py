import numpy as np
Fs=8000
f_arr=[100,0,200,5,300,0,400,1000]
D_cut=0.5 #per sec
volume=1

L_cut=int(Fs*D_cut)
L=int(Fs*D_cut*len(f_arr))
data=np.zeros((L),np.float32)
index=np.linspace(0,D_cut-1/Fs,L_cut)

ptr=0
for f in f_arr:
    data[ptr:ptr+L_cut]=np.sin(index*2*f*np.pi)
    ptr+=L_cut

output_bytes = (volume * data*32760).astype(np.int16).tobytes()


import wave
audio=wave.open("sound.wav","wb")
audio.setframerate(Fs)
audio.setnchannels(1)
audio.setsampwidth(2)
audio.writeframesraw(output_bytes)
audio.close()