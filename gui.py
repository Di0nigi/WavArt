import tkinter as tk
from tkinter import filedialog


class app:
    def __init__(self,r):
        self.currentFile=""
        self.w = 1000
        self.h = 800
        self.r = r
        self.r.title("WavArt")
        self.r.geometry(f"{self.w}x{self.h}")
        self.sideSetting= tk.Frame(self.r,bg="dark grey",height=self.h,width=self.w-self.h)
        self.sideSetting.place(x=0,y=0)
        self.sidePanel()
        self.imPanel = tk.Frame(self.r,bg="black",height=self.h,width=self.h)
        self.imPanel.place(x=self.w-self.h,y=0)
        return
    def run(self):
        self.r.mainloop()
        return
    def sidePanel(self):
        self.fileBt=tk.Button(self.sideSetting, text="Audio file", command=self.importFile)
        self.fileBt.pack(side="left")
        self.titleField=tk.Entry(self.sideSetting,width=self.w-self.h)
        self.titleField.pack(side="left")


        return
    def imagePanel(self):

        return
    def importFile(self):
        self.currentFile=filedialog.askopenfilename(
        title="Select an audio track",
        filetypes=[("All files", "*.*")]
    )
        print(self.currentFile)
        return


def main():
    root = tk.Tk()
    App = app(r=root)
    App.run()
    return



main()