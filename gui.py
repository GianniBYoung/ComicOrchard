import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
import database


# Creates table for comic book info
def create_table(root):
    tableFrame = Frame(root)
    tableFrame.pack(fill=tk.BOTH, expand=True)

    style = ttk.Style()
    style.configure("mystyle.Treeview", fieldbackground="#2d2d2d", foreground="white", highlightthickness=0, bd=0, font=('Times New Roman', 11))
    style.configure("mystyle.Treeview.Heading", foreground="white", background="#4c4c4c", font=('Times New Roman', 13))

    tv = Treeview(tableFrame, style="mystyle.Treeview")
    scrollbar = tk.Scrollbar(tableFrame,
                              orient="vertical",
                              command=tv.yview)
    scrollbar.pack(side='right', fill='x')
    tv.configure(xscrollcommand=scrollbar.set)
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
    tv.tag_configure('odd', background='#272626')
    tv.tag_configure('even', background='#2d2d2d')
    for col in columns:
        tv.heading(col, command=lambda _col=col:
        treeview_sort_column(tv, _col, False))


# Method for double clicking a comic
def on_double_click(event):
    print("hello")


# Creates toolbar with buttons at the top
def create_tool_bar(root):
    toolbar = tk.Frame(root, bg="#272626")
    classButton = HoverButton(root, text="Add Comic", activebackground="#C9C9C9")
    classButton.pack(in_=toolbar, side=tk.LEFT)
    toolbar.pack(fill=tk.X)


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


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
    count = 1;
    tag = "odd"
    for comic in singleComics:
        if count % 2 == 0:
            tag = "even"
        else:
            tag = "odd"
        self.treeview.insert('', 'end', text=comic[0], values=(comic[1], comic[2], comic[3], comic[4], comic[5],
                                                               comic[6], comic[7]), tags=tag)
        count += 1


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