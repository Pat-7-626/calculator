import tkinter as tk
from tkinter import ttk


class Keypad(tk.Frame):

    def __init__(self, parent, keynames=[], columns=1, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.keynames = keynames
        self.columns = columns
        self.list_button = None
        self.init_components(columns)

    def init_components(self, columns) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        :param columns: number of columns to use
        """
        self.list_button = self.make_buttons(columns, self.keynames)

    def make_buttons(self, columns, key):
        list_button = []
        row = 0
        col = 0
        count = 0
        for i in key:
            button = tk.Button(self,
                               text=i)
            button.grid(row=row,
                        column=col,
                        padx=2,
                        pady=2,
                        sticky=tk.NSEW)
            list_button.append(button)
            self.columnconfigure(col, weight=1)
            count += 1
            col += 1
            if count == columns:
                self.rowconfigure(row, weight=1)
                count = 0
                col = 0
                row += 1
        return list_button

    def bind(self, sq=None, todo=None, add=None):
        """Bind an event handler to an event sequence."""
        for i in self.list_button:
            i.bind(sq, todo)

    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.
        """
        for i in self.list_button:
            i.config({key: value})

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.
        """
        if not self.list_button:
            raise ValueError("No buttons in the Keypad.")
        return self.list_button[0].cget(key)

    def configure(self, cnf=None, **kwargs):
        """Apply configuration settings to all buttons.

        To configure properties of the frame that contains the buttons,
        use `keypad.frame.configure()`.
        """
        for i in self.list_button:
            i.configure(**kwargs)

    @property
    def frame(self):
        return super()


if __name__ == '__main__':
    keys = list('789456123 0.')  # = ['7','8','9',...]

    root = tk.Tk()
    root.title("Keypad Demo")
    keypad = Keypad(root, keynames=keys, columns=3)
    keypad.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
