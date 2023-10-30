import tkinter as tk
from tkinter import ttk


class MyFrame:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("WIEGAND")
        self.win.geometry("400x140+450+220")
        self.win.resizable(False, False)
        self.win.grid_columnconfigure(0, minsize=200)
        self.win.grid_columnconfigure(1, minsize=200)
        self.win.grid_rowconfigure(0, minsize=30)
        self.win.grid_rowconfigure(1, minsize=30)
        self.win.grid_rowconfigure(2, minsize=40)

        self.lable_code = tk.Label(self.win, text="CODE:")
        self.lable_wiegand = tk.Label(self.win, text="WIEGAND:")
        self.lable_code.grid(row=0, column=0)
        self.lable_wiegand.grid(row=0, column=1)

        self.lst_wiegand = ("Wiegand 26", "Wiegand 34")
        self.comb_wiegand = ttk.Combobox(self.win, values=self.lst_wiegand)
        self.comb_wiegand.current(0)
        self.comb_wiegand.grid(row=2, column=0, columnspan=2)

        self.empt_code = tk.Entry(self.win)
        self.empt_wiegand = tk.Entry(self.win)
        self.empt_code.grid(row=1, column=0)
        self.empt_wiegand.grid(row=1, column=1)

        self.btn_code = tk.Button(self.win, text='GET CODE', command=self.GET_code)
        self.btn_wiedand = tk.Button(self.win, text='GET WIEGAND', command=self.GET_wiegand)
        self.btn_code.grid(row=3, column=0)
        self.btn_wiedand.grid(row=3, column=1)

    def GET_wiegand(self):
        if self.comb_wiegand.get() == "Wiegand 26":
            if self.empt_wiegand.get() != '':
                self.empt_wiegand.delete(0, "end")
            self.empt_wiegand.insert(0, f"{Wiegand26(BitCode(f'{self.empt_code.get()}')).get_wiegand26()}")
        if self.comb_wiegand.get() == "Wiegand 34":
            if self.empt_wiegand.get() != '':
                self.empt_wiegand.delete(0, "end")
            self.empt_wiegand.insert(0, f"{Wiegand34(BitCode(f'{self.empt_code.get()}')).get_wiegand34()}")

    def GET_code(self):
        if self.comb_wiegand.get() == "Wiegand 26":
            if self.empt_code.get() != "":
                self.empt_code.delete(0, "end")
            self.empt_code.insert(0, f"{Wiegand26(BitCode(f'{self.empt_wiegand.get()}')).get_codecard26()}")
        if self.comb_wiegand.get() == "Wiegand 34":
            if self.empt_code.get() != "":
                self.empt_code.delete(0, "end")
            self.empt_code.insert(0, f"{Wiegand34(BitCode(f'{self.empt_wiegand.get()}')).get_codecard34()}")

    def DEL_code(self):
        self.empt_code.delete(0, "end")

    def DEL_wiegand(self):
        self.empt_wiegand.delete(0, "end")


class BitCode:

    def __init__(self, code):
        self.code = int(code, 16)

    @staticmethod
    def check_grup(grup):
        x = grup
        act_bit = 1
        while x:
            act_bit ^= x & 1
            x >>= 1
        return bool(act_bit)


class Wiegand26:

    def __init__(self, bitcode):
        self.bitcode = bitcode.code

    def get_codecard26(self):
        return hex((self.bitcode & 0x1FFFFFF) >> 1)

    def get_wiegand26(self):
        c = self.bitcode
        c |= (BitCode.check_grup(self.s_grup26()) ^ 1) << 24
        c = (c << 1) | BitCode.check_grup(self.m_grup26())
        return hex(c)

    def s_grup26(self):
        c = self.bitcode
        c >>= 12
        return c

    def m_grup26(self):
        c = self.bitcode
        mask = 0xFFF << 12
        c |= mask
        return c


class Wiegand34:

    def __init__(self, bitcode):
        self.bitcode = bitcode.code

    def get_codecard34(self):
        return hex((self.bitcode & 0x1FFFFFFFF) >> 1)

    def get_wiegand34(self):
        c = self.bitcode
        c |= (BitCode.check_grup(self.s_grup34()) ^ 1) << 32
        c = (c << 1) | BitCode.check_grup(self.m_grup34())
        return hex(c)

    def s_grup34(self):
        c = self.bitcode
        c >>= 16
        return c

    def m_grup34(self):
        c = self.bitcode
        mask = 0xFFFF << 16
        c |= mask
        return c


frame = MyFrame()
frame.win.mainloop()
