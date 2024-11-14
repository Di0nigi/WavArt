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
fontList=["fonts\BechamDisco-Regular_demo-BF6719eb856cdc2.otf","fonts\\bitwise.ttf","fonts\PlanetN-VXDV.otf","fonts\CSBishopDrawn-Regular_demo-BF6732d05f69863.otf","fonts\CSAntliaDrawn-Regular_demo-BF6732cebcc8d67.otf"]
chars= ' .\'`^",:;Il!i><¬~+_-?][}{\\1234567890)(|\\/*#MW&8%B@$£'
#title="Reptilia"
asciiPaths= ['assets\\animals1.txt', 'assets\\animals10.txt', 'assets\\animals11.txt', 'assets\\animals12.txt', 'assets\\animals13.txt', 'assets\\animals14.txt', 'assets\\animals15.txt', 'assets\\animals16.txt', 'assets\\animals17.txt', 'assets\\animals18.txt', 'assets\\animals19.txt', 'assets\\animals2.txt', 'assets\\animals3.txt', 'assets\\animals4.txt', 'assets\\animals5.txt', 'assets\\animals6.txt', 'assets\\animals7.txt', 'assets\\animals8.txt', 'assets\\animals9.txt', 'assets\\clouds1.txt', 'assets\\clouds2.txt', 'assets\\clouds3.txt', 'assets\\clouds4.txt', 'assets\\clouds5.txt', 'assets\\clouds6.txt', 'assets\\computer1.txt', 'assets\\computer10.txt', 'assets\\computer11.txt', 'assets\\computer12.txt', 'assets\\computer13.txt', 'assets\\computer14.txt', 'assets\\computer15.txt', 'assets\\computer16.txt', 'assets\\computer17.txt', 'assets\\computer18.txt', 'assets\\computer19.txt', 'assets\\computer2.txt', 'assets\\computer20.txt', 'assets\\computer21.txt', 'assets\\computer22.txt', 'assets\\computer23.txt', 'assets\\computer24.txt', 'assets\\computer25.txt', 'assets\\computer3.txt', 'assets\\computer4.txt', 'assets\\computer5.txt', 'assets\\computer6.txt', 'assets\\computer7.txt', 'assets\\computer8.txt', 'assets\\computer9.txt', 'assets\\dino1.txt', 'assets\\dino10.txt', 'assets\\dino11.txt', 'assets\\dino12.txt', 'assets\\dino13.txt', 'assets\\dino14.txt', 'assets\\dino2.txt', 'assets\\dino3.txt', 'assets\\dino4.txt', 'assets\\dino5.txt', 'assets\\dino6.txt', 'assets\\dino7.txt', 'assets\\dino8.txt', 'assets\\dino9.txt', 'assets\\monke1.txt', 'assets\\monke2.txt', 'assets\\monke3.txt', 'assets\\monke4.txt', 'assets\\monke5.txt', 'assets\\monke6.txt', 'assets\\patterns1.txt', 'assets\\patterns2.txt', 'assets\\patterns3.txt', 'assets\\patterns5.txt', 'assets\\patterns6.txt', 'assets\\patterns7.txt', 'assets\\patterns8.txt', 'assets\\patterns9.txt', 'assets\\shapes1.txt', 'assets\\shapes10.txt', 'assets\\shapes2.txt', 'assets\\shapes3.txt', 'assets\\shapes4.txt', 'assets\\shapes5.txt', 'assets\\shapes6.txt', 'assets\\shapes7.txt', 'assets\\shapes8.txt', 'assets\\shapes9.txt', 'assets\\smile1.txt', 'assets\\smile2.txt', 'assets\\smile3.txt', 'assets\\smile4.txt', 'assets\\smile5.txt', 'assets\\smile6.txt', 'assets\\smile7.txt', 'assets\\smile8.txt']
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
    
    while font.getbbox(text)[3] < targetHeight:
        if font.getbbox(text)[2] > maxSz:
            fontSize -=1
            break
        fontSize += 1
        font = ImageFont.truetype(fontPath, fontSize)
    
    return fontSize,font.getbbox(text)

def openFile(path):
    content=[]
    with open(path,mode="r",encoding="utf-8") as f:
        for line in f:
            content.append(line)
            #content+="\n"
    return content


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

def sharpen(image, strength=1.5):
    
    blurredImage = cv2.GaussianBlur(image, (0, 0), 3)
    
    sharpenedImage = cv2.addWeighted(image, 1 + strength, blurredImage, -strength, 0)

    return sharpenedImage




def processDataPipeline(data,fr,title,fnt):
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

    colors = im.copy()

    print(f"Adding Ascii art...")

    ascInd = (nSum*sum([ord(x) for x in title])) % len(asciiPaths)
    cont=openFile(asciiPaths[ascInd])
    ascPos = [im.shape[0]//30,im.shape[0]//30]
    #getFontSize(f5ontList[1],100,maxSz=im.shape[0],text=)
    for line in cont:
        im=addText(image=im,text=line,position=tuple(ascPos),font=fontList[1],size=im.shape[0]//45)
        ascPos[1]+=im.shape[0]//30



    print(f"Adding title...")

    #title ="Reptilia"
    fnt = fontList[fnt]
    sz,occ = getFontSize(fnt, im.shape[0]//7, maxSz=im.shape[0]-20, text = title)

    txy=(im.shape[0]//50,im.shape[0]-(occ[3]-occ[1])-im.shape[0]//50)
    
    
    #colors = np.sort(im,axis=1)

    highlightColor =tuple(colors[im.shape[0]//3][im.shape[0]//2]+np.array([10,10,10]))#(255,255,255)#
    shadowColor =tuple(colors[0][0]-np.array([10,10,10]))
    
    im=addText(im,title,txy,font=fnt,size=sz,color=shadowColor)
    im=addText(im,title,(txy[0]+15,txy[1]),font=fnt,size=sz,color=highlightColor)

    print(f"Adding noise...")
    #print(nSum)
    #noiseMp = np.resize(wav.copy(),new_shape=(s,s,3))
    nSum = int(sum(int(digit) for digit in str(abs(int(nSum))))*3.4)
   # print(nSum)
    im=addNoise(im,0,nSum)

    print(f"Sharpening...")

    im=sharpen(im,strength=1.5)



    return im


def main(title):
    
    #track = "D:\dionigi\Music\Synth\\RawTracks\z8.WAV"
    #track = "D:\dionigi\Music\Synth\\RawTracks\ZOOM0002.WAV"
    track = "D:\dionigi\Music\Synth\Dune3.mp3"

    d,f=openTrack(track)
   
    i = processDataPipeline(d,f,title=title,fnt=0)

    save(f"{title}.png",i)

    return "Done"




#print(main(title="Reptilia"))