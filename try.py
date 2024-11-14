'''import os 

path = "D:\dionigi\Documents\Python scripts\WavArt\\assets"
paths=[]
for elem in os.listdir(path):
    if os.path.isfile(os.path.join(path,elem)):
        paths.append(os.path.join("assets",elem))
print(paths)'''

