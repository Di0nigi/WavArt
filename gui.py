import tkinter as tk
from tkinter import filedialog
import artGen as aG

class app:
    def __init__(self,r):
        self.currentFile=""
        self.currentFont = tk.StringVar()
        self.currentFont.set("BechamDisco")
        self.fonts=["BechamDisco","bitwise","PlanetN","CSBishopDrawn","CSAntliaDrawn"]
        self.fileName="None"
        self.fontInd=0
        self.w = 1000
        self.h = 800
        self.r = r
        self.r.title("WavArt")
        self.r.geometry(f"{self.w}x{self.h}")
        self.sideSetting= tk.Frame(self.r,bg="grey",height=self.h,width=self.w-self.h)
        self.sideSetting.place(x=0,y=0)
        self.sidePanel()
        self.imPanel = tk.Frame(self.r,bg="dark grey",height=self.h,width=self.h)
        self.imPanel.place(x=self.w-self.h,y=0)
        return
    def run(self):
        self.r.mainloop()
        return
    def sidePanel(self):
        self.fileBt=tk.Button(self.sideSetting, text="Audio file", command=self.importFile,width=28)
        self.fileBt.place(x=0,y=0)
        self.nameFile = tk.Label(text=self.fileName, font=("TkDefaultFont",10),width=25,anchor="w")
        self.nameFile.place(x=0,y=25)
        self.titleField=tk.Entry(self.sideSetting,width=33)
        self.titleField.place(x=0,y=47)
        self.fontMenu = tk.OptionMenu(self.sideSetting, self.currentFont, *self.fonts, command=self.onSelect)
        self.fontMenu.config(width=26)
        self.fontMenu.place(x=0,y=67)
        self.genBt = tk.Button(self.sideSetting, text="Generate", command=self.gen,width=28)
        self.genBt.place(x=0,y=100)
        return
    def imagePanel(self):

        return
    def importFile(self):
        self.currentFile=filedialog.askopenfilename(
        title="Select an audio track",
        filetypes=[("Audio files", "*.mp3"),("Audio files", "*.WAV")]
        
    )
        self.nameFile.config(text=self.currentFile.split("/")[-1])
        print(self.currentFile)
        return
    def onSelect(self,value):
        self.fontInd = self.fonts.index(value)

        return
    def gen(self):
        if self.currentFile:
            d,f=aG.openTrack(self.currentFile)
            titl=self.titleField.get()
            if titl:
                i = aG.processDataPipeline(d,f,title=titl,fnt=self.fontInd)
                aG.save(f"{titl}.png",i)


        return


def main():
    root = tk.Tk()
    App = app(r=root)
    App.run()
    return



main()