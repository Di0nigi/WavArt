'''import librosa
import numpy as np
import cv2

# Load the audio file
audio_path = 'D:\dionigi\Music\Synth\Dune3.mp3'
y, sr = librosa.load(audio_path)

# Parameters for frame processing
frame_length = 2048
hop_length = 512

# Step 1: Calculate RMS energy for each frame
rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

# Step 2: Create a 2D "height map" by tiling RMS values
height_map = np.tile(rms, (50, 1))      # Duplicate rows to create a 2D matrix
height_map = np.log1p(height_map)        # Optional log transform to enhance contrast

# Normalize the height map for image display
height_map_normalized = cv2.normalize(height_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Step 3: Apply a color map to simulate a terrain look
colored_terrain = cv2.applyColorMap(height_map_normalized, cv2.COLORMAP_TURBO)

# Step 4: Add shadows to simulate depth
shadow_map = cv2.GaussianBlur(height_map_normalized, (15, 15), 0)

# Convert shadow_map to 3 channels to match colored_terrain
shadow_map_3ch = cv2.cvtColor(shadow_map, cv2.COLOR_GRAY2BGR)

# Blend the shadow map with the color terrain image
shadow_intensity = 0.5  # Intensity of the shadow effect
terrain_with_shadows = cv2.addWeighted(colored_terrain, 1, shadow_map_3ch, shadow_intensity, 0)

# Step 5: Overlay ASCII characters at peak locations
ascii_symbols = "@#%*+=-."
threshold = 200  # Threshold to detect peaks for ASCII overlay

# Iterate over columns (time frames) and overlay ASCII symbols on high peaks
for i in range(height_map.shape[1]):
    if height_map[0, i] > threshold:
        # Select an ASCII symbol based on the amplitude
        symbol = ascii_symbols[min(int(height_map[0, i] / 255 * (len(ascii_symbols) - 1)), len(ascii_symbols) - 1)]
        # Overlay symbol on the image at peak positions
        cv2.putText(terrain_with_shadows, symbol, (i, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

# Step 6: Display and save the result
cv2.imshow('Audio Terrain', terrain_with_shadows)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the resulting image
cv2.imwrite('audio_terrain_map.png', terrain_with_shadows)
'''

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load audio file
audio_path = 'D:\dionigi\Music\Synth\Dune3.mp3'
y, sr = librosa.load(audio_path)

# Compute onset strength envelope
onset_env = librosa.onset.onset_strength(y=y, sr=sr)

# Estimate tempo and find beat frames
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onset_env)

# Convert beat frames to time
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Plot waveform and overlay detected beats
plt.figure(figsize=(14, 5))
librosa.display.waveshow(y, sr=sr, alpha=0.6)
plt.vlines(beat_times, -1, 1, color='r', alpha=0.8, linestyle='--', label='Beats')
plt.xlabel('Time (s)')
plt.title(f'Waveform with Detected Beats (Tempo: {tempo:.2f} BPM)')
plt.legend()
plt.show()
