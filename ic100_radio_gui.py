import tkinter as tk
import tkinter.font as tkfont
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import json
import os

FAVORITES_FILE = "favorites.json"

class MainApp:
    def __init__(self, master):
        self.state = False
        # 내부 주파수를 백분위 단위로 저장 (예: 91.50MHz → 9150)
        self.current_freq = 9150  
        master.title("EO-IC100 FM Radio")
        master.resizable(False, False)
        freq_font = tkfont.Font(size=20)
        
        # 주파수 표시 (내부값을 100으로 나누어 MHz 단위로 출력)
        self.label_freq = tk.Label(master, text=f'{self.current_freq/100:.2f}MHz', font=freq_font)
        self.label_freq.grid(row=0, column=0, rowspan=2, columnspan=3)
        
        # 주파수 조절 버튼들
        self.btn_freq_up_1m = tk.Button(master, text='freq_up_1m', command=lambda: self.cb_freq_up(100))
        self.btn_freq_up_1m.grid(row=0, column=3, sticky="ew")
        self.btn_freq_down_1m = tk.Button(master, text='freq_down_1m', command=lambda: self.cb_freq_down(100))
        self.btn_freq_down_1m.grid(row=1, column=3, sticky="ew")
        
        self.btn_freq_up_500k = tk.Button(master, text='freq_up_500k', command=lambda: self.cb_freq_up(50))
        self.btn_freq_up_500k.grid(row=0, column=4, sticky="ew")
        self.btn_freq_down_500k = tk.Button(master, text='freq_down_500k', command=lambda: self.cb_freq_down(50))
        self.btn_freq_down_500k.grid(row=1, column=4, sticky="ew")
        
        self.btn_freq_up_100k = tk.Button(master, text='freq_up_100k', command=lambda: self.cb_freq_up(10))
        self.btn_freq_up_100k.grid(row=0, column=5, sticky="ew")
        self.btn_freq_down_100k = tk.Button(master, text='freq_down_100k', command=lambda: self.cb_freq_down(10))
        self.btn_freq_down_100k.grid(row=1, column=5, sticky="ew")
        
        # 전원, 녹음, 볼륨, 음소거 버튼들
        self.btn_power_on = tk.Button(master, text='power_on', command=self.cb_power)
        self.btn_power_on.grid(row=2, column=3, columnspan=2, sticky="ew")
        self.btn_record = tk.Button(master, text='record', command=self.cb_record)
        self.btn_record.grid(row=2, column=5, sticky="ew")
        self.vol_slider = tk.Scale(master, orient='horizontal', to=15, command=self.cb_vol_slider)
        self.vol_slider.grid(row=2, column=1, columnspan=2)
        self.btn_vol_mute = tk.Button(master, text='mute', command=self.cb_mute)
        self.btn_vol_mute.grid(row=2, column=0, sticky="ew")
        
        # 즐겨찾기 버튼 프레임 (버튼 4개 상단, 4개 하단)
        self.favorite_frame = tk.Frame(master)
        self.favorite_frame.grid(row=3, column=0, columnspan=6, pady=10)
        
        # 8개의 즐겨찾기 버튼 생성 (4개씩 2행으로 배치)
        self.favorites = []
        for i in range(8):
            row = i // 4    # 0행과 1행
            col = i % 4     # 각 행에서 0~3 열
            btn = tk.Button(self.favorite_frame, text=f"Favorite {i+1}", 
                             command=lambda idx=i: self.cb_favorite(idx),
                             width=8, height=2)
            btn.grid(row=row, column=col, padx=2, pady=2)
            btn.bind("<Button-3>", lambda event, idx=i: self.edit_favorite(idx))
            self.favorites.append({"button": btn, "name": f"Favorite {i+1}", "freq": None})
        
        # 프로그램 시작 시 즐겨찾기 파일에서 불러오기
        self.load_favorites()

    def validate_frequency(self, freq):
        """MHz 단위 주파수 검증 (76.0 ~ 107.0MHz)"""
        try:
            freq = float(freq)
            if freq < 76.0 or freq > 107.0:
                return None
            return freq
        except ValueError:
            return None

    def update_display(self):
        self.label_freq.config(text=f"{self.current_freq/100:.2f}MHz")

    def cb_freq_up(self, n):
        self.current_freq += n
        if self.current_freq > 10700:
            self.current_freq = 10700
        self.update_display()

    def cb_freq_down(self, n):
        self.current_freq -= n
        if self.current_freq < 7600:
            self.current_freq = 7600
        self.update_display()

    def cb_power(self):
        self.state = not self.state
        if self.state:
            self.btn_power_on.config(text="power_off")
            print("Power turned ON")
        else:
            self.btn_power_on.config(text="power_on")
            print("Power turned OFF")

    def cb_record(self):
        print("Record button pressed")

    def cb_vol_slider(self, n):
        volume = int(n)
        print(f"Volume set to {volume}")

    def cb_mute(self):
        current_text = self.btn_vol_mute.cget("text")
        if current_text == "mute":
            self.btn_vol_mute.config(text="unmute")
        else:
            self.btn_vol_mute.config(text="mute")
        print("Mute toggled")

    def cb_favorite(self, idx):
        if self.favorites[idx]["freq"] is not None:
            # 즐겨찾기에 저장된 값은 내부 단위 (예: 9150)입니다.
            freq_int = self.favorites[idx]["freq"]
            self.set_freq(freq_int)
        else:
            self.edit_favorite(idx)

    def set_freq(self, freq_int):
        self.current_freq = freq_int
        self.update_display()
        print(f"Frequency set to {self.current_freq/100:.2f} MHz")

    def edit_favorite(self, idx):
        current_mhz = self.current_freq / 100
        new_name = simpledialog.askstring("Edit Favorite", 
                                        "Enter station name:",
                                        initialvalue=self.favorites[idx]["name"],
                                        parent=self.favorite_frame)
        if new_name is None:
            return
        new_freq = simpledialog.askfloat("Edit Favorite", 
                                       "Enter frequency (76.0 ~ 107.0 MHz):",
                                       initialvalue=current_mhz,
                                       parent=self.favorite_frame)
        if new_freq is None:
            return
        validated_freq = self.validate_frequency(new_freq)
        if validated_freq is None:
            messagebox.showerror("Error", "Invalid frequency. Please enter a value between 76.0 and 107.0 MHz")
            return
        # 입력받은 MHz 단위를 내부 단위(백분위)로 변환하여 저장
        freq_int = int(validated_freq * 100)
        self.favorites[idx]["name"] = new_name
        self.favorites[idx]["freq"] = freq_int
        self.favorites[idx]["button"].config(text=f"{new_name}\n{validated_freq:.2f}")
        # 즐겨찾기 변경 시 저장
        self.save_favorites()

    def save_favorites(self):
        """즐겨찾기 데이터를 파일에 저장합니다."""
        data = []
        for fav in self.favorites:
            data.append({
                "name": fav["name"],
                "freq": fav["freq"]
            })
        try:
            with open(FAVORITES_FILE, "w") as f:
                json.dump(data, f)
            print("Favorites saved.")
        except Exception as e:
            print("Error saving favorites:", e)

    def load_favorites(self):
        """즐겨찾기 데이터를 파일에서 불러옵니다."""
        if os.path.exists(FAVORITES_FILE):
            try:
                with open(FAVORITES_FILE, "r") as f:
                    data = json.load(f)
                for idx, fav_data in enumerate(data):
                    if idx < len(self.favorites):
                        self.favorites[idx]["name"] = fav_data.get("name", f"Favorite {idx+1}")
                        self.favorites[idx]["freq"] = fav_data.get("freq", None)
                        if self.favorites[idx]["freq"] is not None:
                            display_freq = self.favorites[idx]["freq"] / 100
                            self.favorites[idx]["button"].config(text=f"{self.favorites[idx]['name']}\n{display_freq:.2f}")
                        else:
                            self.favorites[idx]["button"].config(text=self.favorites[idx]["name"])
                print("Favorites loaded.")
            except Exception as e:
                print("Error loading favorites:", e)

if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
