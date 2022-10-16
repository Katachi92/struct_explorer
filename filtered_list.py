import tkinter as tk
from tkinter import ttk
import re

class STR_B:
    def __init__(self):
        self.vals = {
                    'a': 0,
                    'b': 0,
                    'c': 'Ala'
                }


class STR_A:
    def __init__(self):
        self.vals = {
                    'a': STR_B(),
                    'b': '',
                    'c': [1,2,3,4]
                }


class TreeInserter:
    def __init__(self, tree):
        self.tree = tree

    def insert_in_tree(self, val, name, parent=''):
        if hasattr(val, "vals"):
            p = self.tree.insert(parent, tk.END, text=name)
            for node in val.vals:
                self.insert_in_tree(val.vals[node], node, p)
        else:
            p = self.tree.insert(parent, tk.END, text=name, values=val)
        self.tree.set(p, 0, value=14)


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

        self.tre = ttk.Treeview(columns=("field", "value"), show="tree")
        self.tre.column('#0', width=120, stretch=0)
        self.tre.column('#1', width=120, stretch=0)
        TreeInserter(self.tre).insert_in_tree(STR_A(), 'STR_A')
        self.tre.bind('<<TreeviewSelect>>', self.on_tre_selection_change)
        self.tre.pack()

        self.selected_node = tk.StringVar()
        self.tre_selection = tk.Label(textvariable=self.selected_node)
        self.tre_selection.pack()

    def on_lbx_selection_change(self, event):
        self.selected_val.set(''.join([self.lbx.get(i) for i in self.lbx.curselection()]))

    def on_tre_selection_change(self, event):
        node_id = self.tre.selection()[0]
        node = self.tre.item(node_id)
        p_node_txt = self.tre.item(self.tre.parent(node_id))['text']
        self.selected_node.set(p_node_txt)
    
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
