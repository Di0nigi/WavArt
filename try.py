import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Load the audio file
filename = 'D:\dionigi\Music\Synth\Dune3.mp3'
y, sr = librosa.load(filename)

# Extract tempo and beat frames
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Convert the beat frames to time values (in seconds)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

print("Estimated Tempo:", tempo)
print("Beat times (in seconds):", beat_times)

# Optionally, plot the waveform with beat markers
plt.figure(figsize=(10, 4))
librosa.display.waveshow(y, sr=sr, alpha=0.6)
plt.vlines(beat_times, -1, 1, color='r', linestyle='--', label='Beats')
plt.title("Waveform with Beat Times")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()
