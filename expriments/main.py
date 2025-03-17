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
BASEDIR="/home/pouyalnx/Desktop/code/audioCkar"

import os
BUFFER_DIR=BASEDIR+"/"+FNAME.split('.')[0]
os.mkdir(BUFFER_DIR)

import ffmpeg
(ffmpeg.input(BASEDIR+"/"+FNAME).filter('fps',fps=60,round='up').output(BUFFER_DIR+"/"+"%d.jpg").run())




import shutil
#shutil.rmtree(BUFFER_DIR)