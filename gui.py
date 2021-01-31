import tkinter as tk
import database
from tkinter.ttk import *


# Creates table for comic book info
def create_table(root):
    tableFrame = Frame(root)
    tableFrame.pack(fill=tk.BOTH, expand=True)
    tv = Treeview(tableFrame)
    verscrlbar = tk.Scrollbar(tableFrame,
                              orient="vertical",
                              command=tv.yview)
    verscrlbar.pack(side='right', fill='x')
    tv.configure(xscrollcommand=verscrlbar.set)
    tv.pack(fill=tk.BOTH, expand=True)
    tv.bind("<<TreeviewSelect>>", on_double_click)
    columns = ('title', 'type', 'series', 'number', 'issueID', 'date', 'writer')
    tv['columns'] = columns
    tv.heading("#0", text='')
    tv.column("#0", anchor="w")
    tv.heading('title', text='Title', anchor='center')
    tv.column('title', anchor="w")
    tv.heading('type', text='Type')
    tv.column('type', anchor='w', width=100)
    tv.heading('series', text='Series')
    tv.column('series', anchor='w', width=200)
    tv.heading('number', text='Number')
    tv.column('number', anchor='w', width=200)
    tv.heading('issueID', text='IssueID')
    tv.column('issueID', anchor='w', width=200)
    tv.heading('date', text='Date')
    tv.column('date', anchor='w', width=100)
    tv.heading('writer', text='Writer')
    tv.column('writer', anchor='w', width=200)
    root.treeview = tv
    globaltv = tv
    for col in columns:
        tv.heading(col, command=lambda _col=col:
        treeview_sort_column(tv, _col, False))


# Method for double clicking a comic
def on_double_click(event):
    print("hello")


# Creates toolbar with buttons at the top
def create_tool_bar(root):
    toolbar = Frame(root)
    btnAddComic = Button(toolbar, text='Add Comic', command=add_comic)
    btnAddComic.pack(in_=toolbar, side=tk.LEFT)
    toolbar.pack(fill=tk.X)


# Sorts table when clicking on columns
def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda:
    treeview_sort_column(tv, col, not reverse))


# Button click to add comic
def add_comic():
    print("hello")


# Populates table with all current data
def populate_table(self):
    singleComics = database.get_all_comic_info()
    for comic in singleComics:
        self.treeview.insert('', 'end', text=comic[0], values=(comic[1], comic[2], comic[3], comic[4], comic[5],
                                                               comic[6], comic[7]))


def main():
    root = tk.Tk()
    root.title('Comic Orchard')
    root.eval('tk::PlaceWindow . center')
    create_tool_bar(root)
    create_table(root)
    populate_table(root)
    root.mainloop()


if __name__ == '__main__':
    main()
