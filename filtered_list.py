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
                    'b': 'some text',
                    'c': [1,2,3,4]
                }

    def __str__(self):
        return self.vals


class TreeInserter:
    def __init__(self, tree):
        self.tree = tree

    def insert_in_tree(self, val, name, parent=''):
        if hasattr(val, "vals"):
            p = self.tree.insert(parent, tk.END, text=name)
            for node in val.vals:
                self.insert_in_tree(val.vals[node], node, p)
        else:
            p = self.tree.insert(parent, tk.END, text=name)

    def get_val(val, items):
        if val is not None:
            print(f'getting val of {items}')
            for node_name in items:
                val = val.vals[node_name]
                if not hasattr(val, 'vals'):
                    return val
        return ''

    def get_tree_path(self, node_id):
        items = []
        while node_id != '':
            items.append(self.tree.item(node_id)['text'])
            node_id = self.tree.parent(node_id)
        items.reverse()
        return items

    def insert_vals(self, str_val, pos, parent=None):
        children = self.tree.get_children(parent)
        for child in children:
            value = TreeInserter.get_val(str_val, self.get_tree_path(child)[1:])
            self.tree.set(child, pos, value)
            self.insert_vals(str_val, pos, child)


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
        inserter = TreeInserter(self.tre)
        inserter.insert_in_tree(STR_A(), 'STR_A')
        a = STR_A()
        a.vals['b'] = 'nothing'
        inserter.insert_vals(a, 0)
        b = STR_A()
        b.vals['b'] = 'wrong'
        inserter.insert_vals(b, 0)
        self.tre.pack()

        self.selected_node = tk.StringVar()
        self.tre_selection = tk.Label(textvariable=self.selected_node)
        self.tre_selection.pack()

    def on_lbx_selection_change(self, event):
        self.selected_val.set(''.join([self.lbx.get(i) for i in self.lbx.curselection()]))

    def on_tre_selection_change(self, event):
        val = STR_A()
        items = App.get_tree_path(self.tre, self.tre.selection()[0])
        self.selected_node.set('.'.join(items) + ' = ' + str(App.get_val(val, items[2:])))
    
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
