import tkinter as tk
from tkinter.ttk import *


class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.createUI()
        self.loadTable()
        self.grid(sticky=('n', 's', 'w', 'e'))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def createUI(self):
        tv = Treeview(self)
        columns = ('title', 'date', 'size', 'tags', 'creators', 'series', 'publisher', 'characters', 'storyArc')
        tv['columns'] = columns
        tv.heading("#0", text='', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('title', text='Title', anchor='w')
        tv.column('title', anchor="w")
        tv.heading('date', text='Date')
        tv.column('date', anchor='center', width=100)
        tv.heading('size', text='Size(MB)')
        tv.column('size', anchor='center', width=100)
        tv.heading('tags', text='Tags')
        tv.column('tags', anchor='center', width=100)
        tv.heading('creators', text='Creator(s)')
        tv.column('creators', anchor='center', width=200)
        tv.heading('series', text='Series')
        tv.column('series', anchor='center', width=200)
        tv.heading('publisher', text='Publisher')
        tv.column('publisher', anchor='center', width=200)
        tv.heading('characters', text='Characters')
        tv.column('characters', anchor='center', width=200)
        tv.heading('storyArc', text='Story Arc')
        tv.column('storyArc', anchor='center', width=200)
        tv.grid(sticky=('n', 's', 'w', 'e'))
        self.treeview = tv
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        for col in columns:
            tv.heading(col, text=col, command=lambda _col=col:
            treeview_sort_column(tv, _col, False))

    def loadTable(self):
        self.treeview.insert('', 'end', text="1", values=('title', '10:00',
                                                          '10:10', 'Ok', 'hello', 'goodbye', '1', '2', '3'))
        self.treeview.insert('', 'end', text="2", values=('second title', '20',
                                                          '30', 'Ok', 'hello', 'goodbye', '1', '2', '3'))


def main():
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    App(root)
    root.mainloop()


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
        treeview_sort_column(tv, col, not reverse))


if __name__ == '__main__':
    main()
