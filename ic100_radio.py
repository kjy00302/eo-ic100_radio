#!/usr/bin/env python

import ic100_radio_gui
import tkinter as tk
import besfm
import time
import usb.core

'''
GUI FM radio control program
'''

class MainApp(ic100_radio_gui.MainApp):
    def __init__(self, master):
        super().__init__(master)
        dev = usb.core.find(
            idVendor=0x04e8,
            custom_match=lambda x: x.idProduct in [0xa054, 0xa059, 0xa05b]
        )
        if dev is None:
            print("Device not found. Quitting.")
            quit()
        self.fm = besfm.BesFM(dev)
        self.update_power()
        self.volume = tk.IntVar(master, value=6)
        self.freq = 9150
        self.vol_slider['variable'] = self.volume
        self.btn_freq_up_1m['text'] = "+1M"
        self.btn_freq_down_1m['text'] = "-1M"
        self.btn_freq_up_500k['text'] = "+500K"
        self.btn_freq_down_500k['text'] = "-500K"
        self.btn_freq_up_100k['text'] = "+100K"
        self.btn_freq_down_100k['text'] = "-100K"
        self.btn_record['text'] = "Record"
        if self.power or self.record:
            self.update_frequency()
            self.update_volume()
            self.update_mute()

    def cb_power(self):
        if self.power:
            self.fm.set_power(False)
        elif self.record:
            self.fm.set_recording(False)
        else:
            self.fm.set_power(True)
            time.sleep(0.2)
            self.fm.set_volume(6)
            self.reset()
        self.update_power()

    def cb_record(self):
        self.fm.set_recording(True)
        time.sleep(0.2)
        self.fm.set_volume(15)
        self.reset()
        self.update_power()

    def cb_vol_slider(self, n):
        self.fm.set_volume(int(n))

    def cb_freq_up(self, n):
        self.freq += n
        self.freq = min(self.freq, 10700)
        self.set_freq(self.freq)

    def cb_freq_down(self, n):
        self.freq -= n
        self.freq = max(self.freq, 7600)
        self.set_freq(self.freq)

    def cb_mute(self):
        if self.mute:
            self.fm.set_mute(False)
        else:
            self.fm.set_mute(True)
        self.update_mute()

    def reset(self):
        self.set_freq(self.freq)
        self.update_volume()
        self.mute = False
        self.btn_vol_mute['text'] = "Mute"

    def set_freq(self, f):
        self.fm.set_channel(f/100)
        self.update_frequency()

    def update_frequency(self):
        res = self.fm.get_channel()
        self.freq = int(res*100)
        self.label_freq['text'] = f'{res:.2f}MHz'
        if res <= 76:
            self.btn_freq_down_1m['state'] = 'disabled'
            self.btn_freq_down_500k['state'] = 'disabled'
            self.btn_freq_down_100k['state'] = 'disabled'
        else:
            self.btn_freq_down_1m['state'] = 'normal'
            self.btn_freq_down_500k['state'] = 'normal'
            self.btn_freq_down_100k['state'] = 'normal'
        
        if res >= 107:
            self.btn_freq_up_1m['state'] = 'disabled'
            self.btn_freq_up_500k['state'] = 'disabled'
            self.btn_freq_up_100k['state'] = 'disabled'
        else:
            self.btn_freq_up_1m['state'] = 'normal'
            self.btn_freq_up_500k['state'] = 'normal'
            self.btn_freq_up_100k['state'] = 'normal'
        

    def update_mute(self):
        self.mute = self.fm.get_mute()
        if self.mute:
            self.btn_vol_mute['text'] = "Unmute"
        else:
            self.btn_vol_mute['text'] = "Mute"

    def update_volume(self):
        self.volume.set(self.fm.get_volume())

    def update_power(self):
        self.power = self.fm.get_power()
        self.record = self.fm.get_recording()

        if self.power or self.record:
            self.btn_power_on['text'] = "Power off"
            self.btn_record['state'] = 'disabled'
            self.vol_slider['state'] = 'normal'
            self.btn_vol_mute['state'] = 'normal'
        else:
            self.btn_power_on['text'] = "Power on"
            self.btn_record['state'] = 'normal'
            self.label_freq['text'] = f'---.--MHz'
            self.btn_freq_up_1m['state'] = 'disabled'
            self.btn_freq_up_500k['state'] = 'disabled'
            self.btn_freq_up_100k['state'] = 'disabled'
            self.btn_freq_down_1m['state'] = 'disabled'
            self.btn_freq_down_500k['state'] = 'disabled'
            self.btn_freq_down_100k['state'] = 'disabled'
            self.vol_slider['state'] = 'disabled'
            self.btn_vol_mute['state'] = 'disabled'

        if self.record:
            self.btn_record['relief'] = 'sunken'
        else:
            self.btn_record['relief'] = 'raised'


if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
