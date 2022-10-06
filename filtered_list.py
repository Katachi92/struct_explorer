import tkinter as tk
import re

class Field:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.sv = tk.StringVar()
        self.sv.trace("w", self.handle_change)
        self.entry = tk.Entry(textvariable=self.sv)
        self.entry.pack()

        self.values = [Field(11, 'a'), Field(22, 'aa'), Field(33, 'bc')]

        self.var = tk.Variable(value=self.values)
        self.lbx = tk.Listbox(listvariable=self.var, selectmode=tk.SINGLE)
        self.lbx.bind('<<ListboxSelect>>', self.on_lbx_selection_change)
        self.lbx.pack()

        self.selected_val = tk.StringVar()
        self.lbl_selection = tk.Label(textvariable=self.selected_val)
        self.lbl_selection.pack()

    def on_lbx_selection_change(self, event):
        self.selected_val.set(''.join([self.lbx.get(i) for i in self.lbx.curselection()]))
    
    def handle_change(self, *args):
        self.var.set(self.get_filtered_values(self.sv.get()))

    def get_filtered_values(self, text_field_val):
        try:
            def filter_by_id(id_val):
                return [var for var in self.values if var.id == id_val]
            if text_field_val.isdigit():
                return filter_by_id(int(text_field_val))
            elif text_field_val.startswith('0x'):
                return filter_by_id(int(text_field_val[2:], 16))
            else:
                re_filter = re.compile(text_field_val)
                return [var for var in self.values if re_filter.fullmatch(str(var)) != None]
        except:
            return self.values



if __name__ == '__main__':
    App().mainloop()
