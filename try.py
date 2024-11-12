import cv2
import numpy as np
import librosa

def loadWaveformFromAudio(audioFilePath):
    # Load audio file with librosa
    y, sr = librosa.load(audioFilePath, sr=None)
    
    # Normalize the waveform to a range between -1 and 1
    y = y / np.max(np.abs(y))
    return y

def applyAudioWaveDistortion(image, waveform, amplitude=200):
    # Get image dimensions
    height, width = image.shape[:2]
    
    # Scale waveform to match the width of the image
    scaledWaveform = cv2.resize(waveform.reshape(1, -1), (width, 1), interpolation=cv2.INTER_LINEAR).flatten()
    
    # Create distortion maps
    mapY, mapX = np.indices((height, width), dtype=np.float32)
    
    # Apply the waveform as a vertical distortion
    mapY = mapY + amplitude * scaledWaveform
    
    # Remap the image using the distortion maps
    distortedImage = cv2.remap(image, mapX, mapY, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return distortedImage

# Load the image and audio
imagePath = 'D:\dionigi\Documents\Python scripts\WavArt\output\\bw.png'
audioPath = 'D:\dionigi\Music\Synth\Dune3.mp3'
image = cv2.imread(imagePath)

# Get waveform from audio file
waveform = loadWaveformFromAudio(audioPath)

# Apply wave distortion to the image based on the audio waveform
distortedImage = applyAudioWaveDistortion(image, waveform)

cv2.imwrite("warped.png",distortedImage)