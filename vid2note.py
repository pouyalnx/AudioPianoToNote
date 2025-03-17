#about
"""
    this version only designed for
    for one star piano (simplest level) from skoove channel of youtube
    accepted quality only


    #req
    pip install ffmeg

"""
###################################################
# 0-->Convert Video to pictures
FNAME="tp3.mp4"
FOUT="note3.txt"
BASEDIR="/home/pouyalnx/Desktop/code/audioCkar"

import os
BUFFER_DIR=BASEDIR+"/"+FNAME.split('.')[0]
os.mkdir(BUFFER_DIR)

import ffmpeg
(ffmpeg.input(BASEDIR+"/"+FNAME).filter('fps',fps=60,round='up').output(BUFFER_DIR+"/"+"%d.jpg").run())

###################################################

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

###################################################

from datetime import datetime
Start_time=datetime.now()


import os
BUFFER_DIR=BASEDIR+"/"+FNAME.split('.')[0]

from PIL import Image
import numpy as np
lst=os.listdir(BUFFER_DIR)
L=len(lst)
NOTE_SAMPLE_POS_V0=[2,32,56,80,104,129,148,172,193,216,237,260,285,305,330,350,379,400,426,450,472,495,515,540,560,585,610,630,656,677,700,725,748,768,790,815,835,860,884,905,930,950,975,999,1018]
NOTE_SAMPLE_NAME_V0=["C2","C2D2","D2","D2E2","E2","F2","F2G2","G2" ,"G2A2","A2","A2B2","B2","C3","C3D3","D3","D3E3","E3","F3","F3G3","G3","G3A3","A3","A3B3","B3","C4","C4D4","D4","D4E4","E4","F4","F4G4","G4","G4A4","A4","A4B4","B4","C5","C5D5","D5","D5E5","E5","F5","F5G5","G5","G5A5","A5","A5B5","B5","C6","C6D6","D6","D6E6","E6","F6",]
L_NOTES_V0=len(NOTE_SAMPLE_POS_V0)

NOTE_SAMPLE_POS_V1=[2,18,38,61,82,104,126,145,172,191,215,239,260,281,302,327,350,370,393,414,435,455,480,500,526,550,568,596,610,635,660,680,701,722,747,765,795,812,838,860,880,903,924,945,970,990,1015]
NOTE_SAMPLE_NAME_V1=["C2D2","D2","D2E2","E2","F2","F2G2","G2" ,"G2A2","A2","A2B2","B2","C3","C3D3","D3","D3E3","E3","F3","F3G3","G3","G3A3","A3","A3B3","B3","C4","C4D4","D4","D4E4","E4","F4","F4G4","G4","G4A4","A4","A4B4","B4","C5","C5D5","D5","D5E5","E5","F5","F5G5","G5","G5A5","A5","A5B5","B5","C6","C6D6","D6","D6E6","E6","F6",]
L_NOTES_V1=len(NOTE_SAMPLE_POS_V1)

NOTE_KIND=-1

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
back_note_init=False
back_note=None

Cnt=0
Note_Cnt=0
print(f"try to process {L} samples...")
f=open(FOUT,"w")



for l in range(L):
    if NOTE_LINE_IS_INITED==True and l%64==0:
        printProgressBar(l, L, prefix = 'Progress:', suffix = 'Complete', length = 50)
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
            smp=arr[0,0]+arr[0,1]+arr[0,2]
            print(arr.shape)
            if smp>600:
                NOTE_KIND=0
                print("NOTE STARTS FROM C2")
            else:
                NOTE_KIND=1
                print("NOTE STARTS FROM C2D2")
            printProgressBar(0, L, prefix = 'Progress:', suffix = 'Complete', length = 50)
            
        if NOTE_KIND==0:
            sign_arr=(arr-NOTE_LINE_BASE_VALUE)**2
            sign_arr=sign_arr.sum(1)
            sign_arr=sign_arr[NOTE_SAMPLE_POS_V0]
            sign_arr=sign_arr>TH_PRESS
            sign_arr=sign_arr.astype(int)
            if back_note_init==False:
                back_note=sign_arr.copy()
                back_note_init=True
            pos_ar=sign_arr-back_note
            pos_ar=pos_ar>=1
            st=""
            locs=np.where(pos_ar==1)[0]
            for loc in locs:
                st+=f"{NOTE_SAMPLE_NAME_V0[loc]} "
        elif NOTE_KIND==1:
            sign_arr=(arr-NOTE_LINE_BASE_VALUE)**2
            sign_arr=sign_arr.sum(1)
            sign_arr=sign_arr[NOTE_SAMPLE_POS_V1]
            sign_arr=sign_arr>TH_PRESS
            sign_arr=sign_arr.astype(int)
            if back_note_init==False:
                back_note=sign_arr.copy()
                back_note_init=True
            pos_ar=sign_arr-back_note
            pos_ar=pos_ar>=1
            st=""
            locs=np.where(pos_ar==1)[0]
            for loc in locs:
                st+=f"{NOTE_SAMPLE_NAME_V1[loc]} "            
        f.write(st+"\n")
        back_note=sign_arr
    img.close()
f.close()
End_time=datetime.now()
print(f"Notes proccessd {Note_Cnt} after {(End_time-Start_time).seconds} seconds.")


import shutil
shutil.rmtree(BUFFER_DIR)