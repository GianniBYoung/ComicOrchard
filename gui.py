import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk, filedialog
import database


# Creates table for comic book info - https://stackoverflow.com/questions/22456445/how-to-imitate-this-table-using-tkinter
class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.create_table()

    def create_table(self):
        tableFrame = Frame(self.master)
        tableFrame.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("mystyle.Treeview", fieldbackground="#2d2d2d", foreground="white", highlightthickness=0, bd=0,
                        font=('Times New Roman', 11))
        style.configure("mystyle.Treeview.Heading", foreground="white", background="#4c4c4c",
                        font=('Times New Roman', 13))

        scrollbar = tk.Scrollbar(tableFrame,
                                 orient="vertical",
                                 bg="#C9C9C9",
                                 activebackground="#B7B7B7")
        scrollbar.pack(side='right', fill=tk.Y)

        tv = Treeview(tableFrame, style="mystyle.Treeview", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tv.yview)

        tv.configure(xscrollcommand=scrollbar.set)
        tv.pack(fill=tk.BOTH, expand=True)
        tv.bind("<<TreeviewSelect>>", self.on_double_click)
        columns = ('title', 'type', 'series', 'number', 'issueID', 'date', 'writer', 'path')
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
        tv.heading('writer', text='Writer(s)')
        tv.column('writer', anchor='w', width=200)
        tv.heading('path', text='Path')
        tv.column('path', anchor='w', width=200)
        self.master.treeview = tv
        tv.tag_configure('odd', background='#272626')
        tv.tag_configure('even', background='#2d2d2d')

        # Sets up the sorting for clicking the columns - number columns are sorted differently
        for col in columns:
            tv.heading(col, command=lambda _col=col: treeview_sort_column(tv, _col, False))
        tv.heading("#0", command=lambda: treeview_sort_first_column(tv, "#0", False))
        tv.heading("number", command=lambda: treeview_sort_number_column(tv, "number", False))
        tv.heading("issueID", command=lambda: treeview_sort_number_column(tv, "issueID", False))

    # Method for double clicking a comic
    def on_double_click(self, e):
        item = self.master.treeview.item(self.master.treeview.focus())
        comicPath = item['values'][7]
        database.openComicForReading(comicPath)


# Creates toolbar with buttons at the top
def create_tool_bar(root):
    toolbar = tk.Frame(root, bg="#272626")
    btnAddComic = HoverButton(root, text="Add Comic", activebackground="#C9C9C9", command=add_comic)
    btnAddComic.pack(in_=toolbar, side=tk.LEFT)
    btnImportComics = HoverButton(root, text="Import Comics", activebackground="#C9C9C9", command=import_comics)
    btnImportComics.pack(in_=toolbar, side=tk.LEFT)
    toolbar.pack(fill=tk.X)


# button class to customize hover color - https://stackoverflow.com/questions/49888623/tkinter-hovering-over-button-color-change
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


# Sorts table when clicking on columns - https://stackoverflow.com/questions/55268613/python-tkinter-treeview-sort-tree
def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def treeview_sort_first_column(tv, col, reverse):
    l = [(tv.item(k)["text"], k) for k in tv.get_children()]
    l.sort(key=lambda t: t[0], reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_first_column(tv, col, not reverse))


def treeview_sort_number_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda t: int(t[0]), reverse=reverse)
    #      ^^^^^^^^^^^^^^^^^^^^^^^

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col,
               command=lambda: treeview_sort_number_column(tv, col, not reverse))


# Populates table with all current data
def populate_table(self):
    singleComics = database.get_all_comic_info()
    count = 1
    for comic in singleComics:
        if count % 2 == 0:
            tag = "even"
        else:
            tag = "odd"
        self.treeview.insert('', 'end', text=comic[0], values=(comic[1], comic[2], comic[3], comic[4], comic[5],
                                                               comic[6], comic[7], comic[8]), tags=tag)
        count += 1


# Button click to add comic - https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
def add_comic():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=[("Comic Book Zips",
                                                      "*.cbz*")])


# button click to import comics
def import_comics():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=[("Comic Book Zips",
                                                      "*.cbz*")])


def main():
    root = tk.Tk()
    root.geometry("2000x1000")
    root.title('Comic Orchard')
    root.eval('tk::PlaceWindow . center')
    create_tool_bar(root)
    App(root)
    populate_table(root)
    root.mainloop()


if __name__ == '__main__':
    main()
