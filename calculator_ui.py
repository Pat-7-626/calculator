import tkinter as tk
import copy
from tkinter import ttk
from keypad import Keypad
from math import *
from winsound import *


class CalculatorUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.past_val = None
        self.past = None
        self.display = None
        self.re = None
        self.pad = None
        self.sym = None
        self.input_spe = None
        self.com = None
        self.list_display = []
        self.list_eq = []
        self.list_input = []
        self.list_past = []
        self.change = {"ln": "log", "mod": "%", "π": "pi", "^": "**"}
        self.init_components()

    def init_components(self):
        self.input_spe = tk.StringVar()
        self.past_val = tk.StringVar()
        self.display = tk.Label(self,
                                background="black",
                                text="",
                                foreground="white",
                                anchor=tk.E,
                                font=('Tahoma', 15))
        self.display.grid(column=0,
                          row=0,
                          columnspan=self.winfo_screenwidth(),
                          sticky=tk.NSEW)
        self.com = ttk.Combobox(self,
                                textvariable=self.input_spe,
                                values=("exp", "ln", "log10",
                                        "log2", "sqrt", "sin",
                                        "cos", "tan"),
                                font=('Tahoma', 15))
        self.com.grid(column=2,
                      row=1,
                      sticky=tk.NSEW)
        self.com.bind('<<ComboboxSelected>>', self.display_handler_com)
        self.com.bind('<Return>', self.display_handler_com)
        self.past = ttk.Combobox(self,
                                 textvariable=self.past_val,
                                 font=('Tahoma', 15))
        self.past.grid(column=0,
                       row=1,
                       columnspan=2,
                       sticky=tk.NSEW)
        self.past.bind('<<ComboboxSelected>>', self.past_handler)
        self.re = Keypad(self, ["CLR", "DEL", "(", ")", "="], 1)
        self.re.grid(column=0,
                     row=2,
                     sticky=tk.NSEW)
        self.re.bind("<Button>", self.display_handler)
        self.pad = Keypad(self,
                          ["7", "8", "9", "4",
                           "5", "6", "1", "2",
                           "3", "00", "0", "."],
                          3)
        self.pad.grid(column=2,
                      row=2,
                      sticky=tk.NSEW)
        self.pad.bind("<Button>", self.display_handler)
        self.sym = Keypad(self,
                          ["π", "e",
                           "*", "/", "+",
                           "-", "^", "mod"],
                          2)
        self.sym.grid(column=1,
                      row=2,
                      sticky=tk.NSEW)
        self.sym.bind("<Button>", self.display_handler)
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=5)
        self.re.configure(bg="steel blue",
                          fg="white",
                          activebackground="white",
                          activeforeground="steel blue",
                          font=('Tahoma', 15))
        self.sym.configure(bg="dark goldenrod",
                           fg="white",
                           activebackground="white",
                           activeforeground="dark goldenrod",
                           font=('Tahoma', 15))
        self.pad.configure(bg="MediumPurple4",
                           fg="white",
                           activebackground="white",
                           activeforeground="MediumPurple4",
                           font=('Tahoma', 15))

    def display_handler(self, event):
        val = event.widget["text"]
        val_dis = event.widget["text"]
        for i, j in self.change.items():
            if i == val:
                val = j
        if val == "CLR":
            self.clear_handler()
        elif val == "DEL":
            self.del_handler()
        elif val == "=":
            self.eq_handler()
        else:
            self.list_eq.append(val)
            self.list_display.append(val_dis)
            self.list_input.append(val_dis)
            self.display["text"] = "".join(self.list_display)

    def display_handler_com(self, *args):
        val = self.input_spe.get()
        val_dis = self.input_spe.get()
        if val_dis not in ["exp", "ln", "log10",
                           "log2", "sqrt", "sin",
                           "cos", "tan"]:
            self.com["foreground"] = "red"
            Beep(500, 100)
        else:
            self.com["foreground"] = "black"
            for i, j in self.change.items():
                if i == val:
                    val = j
            if not self.list_eq:
                self.list_input.append("normal_spe")
                self.list_input.append("(")
                self.list_eq.append(val)
                self.list_eq.append("(")
                self.list_display.append(val_dis)
                self.list_display.append("(")
            elif self.list_display[-1] in ["mod", "*", "/", "+", "-", "^"]:
                self.list_input.append("normal_spe")
                self.list_input.append("(")
                self.list_eq.append(val)
                self.list_eq.append("(")
                self.list_display.append(val_dis)
                self.list_display.append("(")
            else:
                self.list_eq.insert(0, "(")
                self.list_eq.insert(0, val)
                self.list_eq.append(")")
                self.list_display.insert(0, "(")
                self.list_display.insert(0, val_dis)
                self.list_display.append(")")
                self.list_input.append(val_dis)
            self.display["text"] = "".join(self.list_display)

    def past_handler(self, *args):
        val = self.past_val.get()
        for i in self.list_past:
            if i[0] == val:
                self.list_input = copy.deepcopy(i[1])
                self.list_eq = copy.deepcopy(i[2])
                self.list_display = copy.deepcopy(i[3])
                break
        self.display["text"] = "".join(self.list_display)
        self.past.set("")

    def clear_handler(self):
        self.com.set("")
        self.display["foreground"] = "white"
        self.list_eq.clear()
        self.list_display.clear()
        self.list_input.clear()
        self.display["text"] = "".join(self.list_display)

    def del_handler(self):
        self.com.set("")
        if not self.list_eq:
            pass
        elif (self.list_input[-1] in ["exp", "ln", "log10",
                                      "log2", "sqrt",
                                      "sin", "cos", "tan"]
              and self.list_input[-1] != "normal_spe"):
            self.list_input.pop()
            self.list_eq.pop()
            self.list_eq.pop(0)
            self.list_eq.pop(0)
            self.list_display.pop()
            self.list_display.pop(0)
            self.list_display.pop(0)
        else:
            self.list_input.pop()
            self.list_eq.pop()
            self.list_display.pop()
        self.display["text"] = "".join(self.list_display)

    def eq_handler(self):
        count = 0
        try:
            eval("".join(self.list_eq))
        except (SyntaxError, NameError, ValueError):
            self.com.set("")
            self.display["foreground"] = "red"
            Beep(500, 100)
            count = 1
        if count == 0:
            self.com.set("")
            self.display["foreground"] = "white"
            ans = eval("".join(self.list_eq))
            if ans.is_integer():
                ans = int(ans)
            self.display["text"] = ans
            self.list_past.append([f"{"".join(self.list_display)} = {ans}",
                                   copy.deepcopy(self.list_input),
                                   copy.deepcopy(self.list_eq),
                                   copy.deepcopy(self.list_display)])
            self.past["values"] = [i[0] for i in self.list_past]

    def run(self):
        self.mainloop()
