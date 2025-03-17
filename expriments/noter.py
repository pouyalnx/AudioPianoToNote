from datetime import datetime
Start_time=datetime.now()

FNAME="SZA_Kill_Bill_SLOW_EASY_1.mp4"
BASEDIR="/home/pouyalnx/Desktop/code/audioCkar"

import os
BUFFER_DIR=BASEDIR+"/"+FNAME.split('.')[0]

from PIL import Image
import numpy as np
lst=os.listdir(BUFFER_DIR)
L=len(lst)
NOTE_SAMPLE_POS=[2,16,38,62,85,105,129,148,172,193,214,237,260,285,305,330,350,370,395,416,438,460,482,500,525,550,570,595,615,640,660,680,705,725,748,768,790,815,835,860,880,900,925,945,970,990,1015]
L_NOTES=len(NOTE_SAMPLE_POS)
NOTE_LINE_BASE_VALUE=None
NOTE_LINE_IS_INITED=False
EXs=0
EYs=0
EXe=8
EYe=8
Eth=10000000

HRs=350
HRe=355

W_resize=1024

TH_PRESS=10**4

Cnt=0
Note_Cnt=0
print(f"try to process {L} samples...")
f=open("note_part.txt","w")

for l in range(L):
    img=Image.open(BUFFER_DIR+f"/{l+1}.jpg")
    px=img.load()
    E=0
    for x in range(EXs,EXe):
        for y in range(EYs,EYe):
            (a,b,c)=px[x,y]
            E+=a*a+b*b+c*c
    if E>Eth:
        Cnt+=1
    else:
        Note_Cnt+=1
        w,h=img.size
        a_img=img.resize((W_resize,h))
        w,h=a_img.size
        a_img=a_img.crop((0,350,w,355))
        arr=np.array(a_img)
        arr=arr.astype(np.float32)
        arr=arr.mean(0)
        if NOTE_LINE_IS_INITED==False:
            NOTE_LINE_BASE_VALUE=arr.copy()
            NOTE_LINE_IS_INITED=True
        sign_arr=(arr-NOTE_LINE_BASE_VALUE)**2
        sign_arr=sign_arr.sum(1)
        sign_arr=sign_arr[NOTE_SAMPLE_POS]
        sign_arr=sign_arr>TH_PRESS
        sign_arr=sign_arr.astype(int)
        st=""
        for sign in sign_arr:
            st+=f"{sign}"
        f.write(st+"\n")
    img.close()
f.close()
End_time=datetime.now()
print(f"Notes proccessd {Note_Cnt} after {(End_time-Start_time).seconds} seconds.")
