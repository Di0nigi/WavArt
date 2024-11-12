#from scipy.io import wavfile as w
import librosa as lb
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from random import randint
frame = np.zeros(shape=(1000,1000,3))
outPath="output"
#chars= ' .\'`^",:;Il!i><¬~+_-?][}{\\1234567890)(|\\/*#MW&8%B@$£'
#chars='0123456789'

def openTrack(path):
    data, frequency =lb.load(path)
    return data, frequency



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



def extrude(im, xStart, yStart, size, layers, dist = 10):
    workingRegion = im[yStart:yStart + size, xStart:xStart + size].copy()

    for i in range(layers):
        #r1 = randint(0,2)
        
        #if(r1 == 0):
        posX= xStart + i * dist//8
        #else:
         #   posX= xStart - i * dist//2
        posY= yStart - i * dist 

        if posX < 0:
            break
        if posY  <0:
            break
        currentLayer = workingRegion
        layerHeight, layerWidth = currentLayer.shape[:2]
        
       
        maxHeight = min(layerHeight, im.shape[0] - posY)
        maxWidth = min(layerWidth, im.shape[1] - posX)
        
        if maxHeight <= 0 or maxWidth <= 0:
            continue 
        currentLayer = currentLayer[:maxHeight, :maxWidth]

        
        im[posY:posY + maxHeight, posX:posX + maxWidth] = currentLayer

        #edgeWidth = 1  
        #im[posY:posY + edgeWidth, posX:posX + maxWidth] = (0,0,0)

    return im

def waveDistort(image, waveform, amplitude=200):
   
    height, width = image.shape[:2]
    
    scaledWaveform = cv2.resize(waveform.reshape(1, -1), (width, 1), interpolation=cv2.INTER_LINEAR).flatten()
    
    mapY, mapX = np.indices((height, width), dtype=np.float32)
    
    mapY = mapY + amplitude * scaledWaveform
    mapX = mapX + amplitude * scaledWaveform[:, np.newaxis]
    
    distortedImage = cv2.remap(image, mapX, mapY, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return distortedImage





def processDataPipeline(data,fr):
    print(f"Processing data...")

    bpm, beats = lb.beat.beat_track(y=data, sr=fr)

    dSum = int(np.absolute(sum(data)*10000000000000000))

    wav  = data.copy() #data / np.max(np.abs(data))
   
    data.dtype=np.uint8
    map =data

    print(f"Aplying color map...")

    s=int((len(map)//3)**(1/2))

    im = np.resize(map,new_shape=(s,s,3))
    im = np.sort(im,axis=0)
    im = np.sort(im,axis=1)
    clMap = dSum % 22
    #print(clMap)
    im = cv2.applyColorMap(im, clMap)

    print(f"Extruding beatwise...")
    
    stx =500 
    sty = 0
    div= int(sum(int(digit) for digit in str(abs(int(bpm)))) * 1.5)
    #print(div)
    for elem in beats:
        extrude(im, stx, sty, size=int(bpm)*3, layers= int(elem//100))
        if (stx<im.shape[1]):
            stx +=im.shape[0]//div
        else:
            stx = 0
            sty +=int(bpm) + 100
    
    print(f"Applying waveform distortion...")
    ampl = div= int(sum(int(digit) for digit in str(abs(int(fr)))))
    #print(fr)
    im = waveDistort(im, wav,ampl*50)



    

    return im


def main():
    
    #track = "D:\dionigi\Music\Synth\\RawTracks\z8.WAV"
    track = "D:\dionigi\Music\Synth\Dune3.mp3"
    #save("try.png",frame)
    d,f=openTrack(track)
    #tempo, beat_frames = lb.beat.beat_track(y=d, sr=f, onset_envelope=onset_env)
    #beat_times = lb.frames_to_time(beat_frames, sr=f)
    i = processDataPipeline(d,f)
    #c=pixelTochar(m)
    #b=drawChars(np.zeros(shape=m.shape),c)
    #
    # b=np.resize(b,(800,800,3))
    save("bw.png",i)
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