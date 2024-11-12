#from scipy.io import wavfile as w
import librosa as lb
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from random import randint
from PIL import Image, ImageDraw, ImageFont

frame = np.zeros(shape=(1000,1000,3))
outPath="output"
fontList=["fonts\\bitwise.ttf","fonts\PlanetN-VXDV.otf"]
chars= ' .\'`^",:;Il!i><¬~+_-?][}{\\1234567890)(|\\/*#MW&8%B@$£'
title=""
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

def getFontSize(fontPath, targetHeight, maxSz ,text):
    
    fontSize = 1
    font = ImageFont.truetype(fontPath, fontSize)
    
    while font.getbbox(text[0])[3] < targetHeight:
        if font.getbbox(text)[2] > maxSz:
            fontSize -=1
            break
        fontSize += 1
        font = ImageFont.truetype(fontPath, fontSize)
    
    return fontSize



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

def addNoise(image, m , std):

    noise = np.random.normal(m, std, image.shape[:2]).astype(np.float32)
    
    
    noise = np.repeat(noise[:, :, np.newaxis], 3, axis=2)
    
   
    noisyImage = cv2.add(image.astype(np.float32), noise)
    

    noisyImage = np.clip(noisyImage, 0, 255).astype(np.uint8)
    
    return noisyImage

def addText(image, text, position, font, size, color=(255, 255, 255)):
    
    imagePil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    font = ImageFont.truetype(font, size)
    
    draw = ImageDraw.Draw(imagePil)
    
    draw.text(position, text, font=font, fill=color)
    
    image = cv2.cvtColor(np.array(imagePil), cv2.COLOR_RGB2BGR)
    
    return image





def processDataPipeline(data,fr):
    print(f"Processing data...")

    bpm, beats = lb.beat.beat_track(y=data, sr=fr)

    dSum = int(np.absolute(sum(data)*10000000000000000))
    nSum = int(np.absolute(sum(data)*10))

    wav  = data.copy() #data / np.max(np.abs(data))
   
    data.dtype=np.uint8
    map =data

    print(f"Applying color map...")

    s=int((len(map)//3)**(1/2))

    im = np.resize(map,new_shape=(s,s,3))
    im = np.sort(im,axis=0)
    im = np.sort(im,axis=1)
    clMap = dSum % 22
    #print(clMap)
    im = cv2.applyColorMap(im, clMap)
    
    print(f"Extruding according to beat...")
    
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

    ampl = int(sum(int(digit) for digit in str(abs(int(fr)))))
    #print(fr)
    im = waveDistort(im, wav,ampl*50)

    print(f"Adding title...")

    title ="Dune3"
    txy=(0,im.shape[0]//2)
    fnt = fontList[1]
    sz = getFontSize(fnt, im.shape[0]//5, maxSz=im.shape[0]-20, text = title)

    im=addText(im,title,txy,font=fnt,size=sz)

    print(f"Adding noise...")
    #print(nSum)
    #noiseMp = np.resize(wav.copy(),new_shape=(s,s,3))
    nSum = int(sum(int(digit) for digit in str(abs(int(nSum))))*3.4)
   # print(nSum)
    im=addNoise(im,0,nSum)

    return im


def main():
    
    track = "D:\dionigi\Music\Synth\\RawTracks\z8.WAV"
    #track = "D:\dionigi\Music\Synth\\RawTracks\ZOOM0002.WAV"
    #track = "D:\dionigi\Music\Synth\Dune3.mp3"

    d,f=openTrack(track)
   
    i = processDataPipeline(d,f)

    save("bw.png",i)
  






    return "Done"




print(main())