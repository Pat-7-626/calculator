import tkinter as tk
from tkinter import ttk
from keypad import Keypad


class CalculatorUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.display = None
        self.pad = None
        self.sym = None
        self.init_components()

    def init_components(self):
        self.display = tk.Label(self,
                                background="black",
                                text="",
                                foreground="white",
                                anchor=tk.E)
        self.display.grid(column=0,
                          row=0,
                          columnspan=self.winfo_screenwidth(),
                          sticky=tk.NSEW)
        self.pad = Keypad(self,
                          ["7", "8", "9", "4", "5", "6", "1", "2", "3", "00",
                           "0", "."], 3)
        self.pad.grid(column=0,
                      row=1,
                      sticky=tk.NSEW)
        self.pad.bind("<Button>", self.display_handler)
        self.sym = Keypad(self, ["*", "/", "+", "-", "^", "="], 1)
        self.sym.grid(column=1,
                      row=1,
                      sticky=tk.NSEW)
        self.sym.bind("<Button>", self.display_handler)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

    def display_handler(self, event):
        self.display["text"] += event.widget["text"]

    def run(self):
        self.mainloop()
