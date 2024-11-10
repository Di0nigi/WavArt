#from scipy.io import wavfile as w
import librosa as lb
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
frame = np.zeros(shape=(1000,1000,3))
outPath="output"
#chars= ' .\'`^",:;Il!i><¬~+_-?][}{\\1234567890)(|\\/*#MW&8%B@$£'
chars='0123456789'

def openTrack(path):
    data, frequency =lb.load(path)
    return data, frequency


def processData(data,f):

    #data = lb.power_to_db(data,ref=np.max)
    #data = np.absolute(data)
    
    #data = data*1000000000000000
    data.dtype=np.uint8
    

    minV = data.min()   
    maxV = data.max()
    print((minV,maxV))

    #normData = (data - min) / (max - min)
   
    #data = sorted(data)
    #map = (((data - minV))/(maxV-minV)) * 255
    map =data
   #map = sorted(map)
    s=int((len(map)//3)**(1/2))
    im=np.resize(map,new_shape=(s,s,3))
    im = np.sort(im,axis=0)
    im = np.sort(im,axis=1)
    #im = cv2.applyColorMap(im, cv2.COLORMAP_TURBO)
    im=  cv2.GaussianBlur(im, (15, 15), 0)

    return im

def normalDrawing():
    distrib=np.random.normal(loc=0,scale=1,size=1000*1000)




    return


def pixelTochar(l):
    charL=[]
    for x,y in enumerate(l):
        row=""
        for i,j in enumerate(y):
            pixB=(int(j[0])+int(j[1])+int(j[2]))/3
            #ind=(pixB/255)*len(chars)
            ind = min(int((pixB / 255) * len(chars)), len(chars) - 1)
            if ind<0:
                ind = 0
            charvalue= chars[int(ind)]
            row+=charvalue
            row+=charvalue
        charL.append(row)
    return charL

def melSpectrogram(data,freq):
    mlsp = lb.power_to_db(lb.feature.melspectrogram(y=data,sr=freq,n_mels=128),ref=np.max)
    name=f"melSpectrogram"
    #p=f"{os.path.join(path,name)}.png"
    plt.figure(figsize=(10, 4))
    lb.display.specshow(mlsp, y_axis='mel', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title(name)
   # plt.show()
    return mlsp


def drawFrame(data,dims=(1000,1000,3)):
    font = None
    for elem in data:
        
        return
    return

def drawChars(blankframe,charList):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontSize = 0.5 # Adjust font scale for readability
    
    lineHeight = 10
    lineSpace = 10
    for ind,elem in enumerate(charList):
        y = 20 + ind * lineHeight  # Calculate y position for each line
        for i, e in enumerate(elem):
            textColor = (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255))
            x = 20 + i * lineSpace
            cv2.putText(blankframe, e, (x, y), font, fontSize, textColor, 1, cv2.LINE_AA)
    return blankframe

def save(name, file):
    cv2.imwrite(os.path.join(outPath,name), file)
    return


def main():
    
    
    #save("try.png",frame)
    d,f=openTrack("D:\dionigi\Music\Synth\Dune3.mp3")
    onset_env = lb.onset.onset_strength(y=d, sr=f)
    #tempo, beat_frames = lb.beat.beat_track(y=d, sr=f, onset_envelope=onset_env)
    #beat_times = lb.frames_to_time(beat_frames, sr=f)
    m = processData(d,f)
    #c=pixelTochar(m)
    #b=drawChars(np.zeros(shape=m.shape),c)
    #
    # b=np.resize(b,(800,800,3))
    save("bw.png",m)
    #fft_out = lb.stft(d)
    #freq =  lb.fft_frequencies(sr=f)
    #colors = np.abs(fft_out)
    #colors = (colors - colors.min()) / (colors.max() - colors.min())
    #plt.figure(figsize=(10, 6))
    #for i in range(colors.shape[1]):  # Iterating over time frames
    #    plt.scatter(freq, colors[:, i], c=colors[:, i], cmap='hsv', alpha=0.6)

    #plt.show()






    return "done"




print(main())