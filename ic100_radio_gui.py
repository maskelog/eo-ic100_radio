import tkinter as tk
import tkinter.font as tkfont

class MainApp():
    def __init__(self, master):
        self.state = False
        master.title("EO-IC100 FM Radio")
        master.resizable(False,False)
        freq_font = tkfont.Font(size=20)
        #freq
        self.label_freq = tk.Label(master, text='000.00MHz', font=freq_font)
        self.label_freq.grid(row=0,column=0, rowspan=2, columnspan=3)
        self.btn_freq_up_1m = tk.Button(master, text='freq_up_1m', command=lambda:self.cb_freq_up(100))
        self.btn_freq_up_1m.grid(row=0, column=3, sticky="ew")
        self.btn_freq_down_1m = tk.Button(master, text='freq_down_1m', command=lambda:self.cb_freq_down(100))
        self.btn_freq_down_1m.grid(row=1, column=3, sticky="ew")
        self.btn_freq_up_500k = tk.Button(master, text='freq_up_500k', command=lambda:self.cb_freq_up(50))
        self.btn_freq_up_500k.grid(row=0, column=4, sticky="ew")
        self.btn_freq_down_500k = tk.Button(master, text='freq_down_500k', command=lambda:self.cb_freq_down(50))
        self.btn_freq_down_500k.grid(row=1, column=4, sticky="ew")
        self.btn_freq_up_100k = tk.Button(master, text='freq_up_100k', command=lambda:self.cb_freq_up(10))
        self.btn_freq_up_100k.grid(row=0, column=5, sticky="ew")
        self.btn_freq_down_100k = tk.Button(master, text='freq_down_100k', command=lambda:self.cb_freq_down(10))
        self.btn_freq_down_100k.grid(row=1, column=5, sticky="ew")
        
        #power, vol, mute
        self.btn_power_on = tk.Button(master, text='power_on', command=self.cb_power)
        self.btn_power_on.grid(row=2, column=3, columnspan=2, sticky="ew")
        self.btn_record = tk.Button(master, text='record', command=self.cb_record)
        self.btn_record.grid(row=2, column=5, sticky="ew")
        self.vol_slider = tk.Scale(orient='horizontal', to=15, command=self.cb_vol_slider)
        self.vol_slider.grid(row=2,column=1,columnspan=2)
        self.btn_vol_mute = tk.Button(master, text='mute', command=self.cb_mute)
        self.btn_vol_mute.grid(row=2, column=0, sticky="ew")

    def cb_freq_up(self, n):
        raise NotImplementedError
    def cb_freq_down(self, n):
        raise NotImplementedError
    def cb_power(self):
        raise NotImplementedError
    def cb_record(self):
        raise NotImplementedError
    def cb_vol_slider(self, n):
        raise NotImplementedError
    def cb_mute(self):
        raise NotImplementedError


if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
