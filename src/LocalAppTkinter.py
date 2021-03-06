# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.tix import *
from tkinter import filedialog

import WebSpiderFetcher as wpf
import urllib.request as ws
import _thread
import os

class App:

    def __init__(self,master):
        self.master = master
        frame = Frame(master)
        frame.pack()

        '''
        variable definition
        '''
        self.keyword = StringVar()
        self.page = IntVar(value = 1)    
        self.statusText = StringVar()
        self.totalPages = int(1)
        self.resultList = []

        '''
        widget definition
        '''
        # Text Field
        self.textfield = Entry(frame,textvariable = self.keyword)
        # Goto text Field
        vcmd = (master.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.gotoText = Entry(frame,width=5,validate = 'key', validatecommand = vcmd)
        # Search Button
        self.btnSearch = Button(frame,text='Search',command=self.eventOnSearch)
        # Goto Button
        self.btnGoto = Button(frame, text = 'Go To', command=self.gotoPage)
        # Previous Page Button
        self.btnPrevious = Button(frame, text='Previous Page', command=self.previousPage)
        # Next Page Button
        self.btnNext = Button(frame, text='Next Page', command=self.nextPage)
        # Download Button
        self.btnDebug = Button(frame,text='Download',command=self.download)
        # Status Bar          
        self.statusBar= Label(frame, bd=1, relief=SUNKEN, anchor=W,textvariable=self.statusText)
        self.setStatusText('Thank you for using AnimeGo as your choice!')
        # CheckListBox
        self.list = CheckList(frame,width=942,height=530)
        self.list.hlist.config(bg='white', selectmode='none', selectbackground='white',selectforeground='black', font=('arial','10','normal'),drawbranch=False, header=True)
        self.list.hlist.header_create(0, itemtype=TEXT, text='Information',relief='flat')

        
        '''
        widget packing
        '''
        self.statusBar.pack(side=BOTTOM,fill = X)
        self.list.pack(side=BOTTOM)
        self.textfield.pack(side=LEFT)
        self.btnSearch.pack(side=LEFT)
        self.btnDebug.pack(side=LEFT)
        self.btnNext.pack(side=RIGHT)
        self.btnPrevious.pack(side=RIGHT)
        self.btnGoto.pack(side=RIGHT)
        self.gotoText.pack(side=RIGHT)

        '''
        binding
        '''
        self.textfield.bind('<Return>', self.eventOnSearch)
        self.gotoText.bind('<Return>', self.gotoPage)
        master.bind('<Right>', self.nextPage)
        master.bind('<Left>', self.previousPage)

        self.textfield.focus()

    def setStatusText(self,string):
        self.statusText.set(string)

    def nextPage(self,*event):
        currentPage = self.page.get()
        if currentPage < self.totalPages:
            self.page.set(self.page.get()+1)
            _thread.start_new_thread(self.search, ())
        else:
            self.setStatusText('Page Number out of Range Page: %s/%s' %(self.page.get(),self.totalPages))

    def previousPage(self,*event):
        currentPage = self.page.get()
        if currentPage > 1:
            self.page.set(self.page.get()-1)
            _thread.start_new_thread(self.search, ())
        else:
            self.setStatusText('Page Number out of Range Page: %s/%s' %(self.page.get(),self.totalPages))

    def eventOnSearch(self,*event):
        self.page.set(1)
        _thread.start_new_thread(self.search, ())

    def gotoPage(self,*event):
        pageNumber = int(self.gotoText.get())
        if pageNumber > 0 and pageNumber <= self.totalPages:
            self.page.set(pageNumber)
            _thread.start_new_thread(self.search, ())
        else:
            self.setStatusText('Page Number out of Range Page: %s/%s' %(self.page.get(),self.totalPages))

    def search(self):
        '''
        search the keyword contained in textfield
        on the given page number
        '''
        keyword = self.keyword.get()
        page = self.page.get()
        
        self.setStatusText('Searching: %s at page: %s/%s' %(keyword, self.page.get(), self.totalPages))

        self.resultList, totalPages = wpf.acess(keyword,page)
        if totalPages != -1: self.totalPages = totalPages
        self.list.hlist.delete_all()

        for id,item in enumerate(self.resultList):
            self.list.hlist.add(id, text=item)
            self.list.setstatus(id, "off")

        self.setStatusText('%s results found at Page: %s/%s' %(len(self.resultList),page,self.totalPages))

    def downloadFile(self, name, url, path):
        f = ws.urlopen(url)
        data = f.read()
        name = wpf.getCleanFileName(name)
        with open(path+name+'.torrent', "wb") as code:
            code.write(data)
            code.close()
            self.setStatusText('File: %s saved at %s'%(name, path))

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            return True
        else:
            return False

    def download(self):
        path = filedialog.askdirectory(initialdir = "./",title = "Save As") + '/'
        selection = self.list.getselection()
        if len(selection) == 0: return
        
        for index in selection:
            info = self.resultList[int(index)]
            self.downloadFile(info[2], info[4], path) #info[2] - title, info[4] - torrent address
            self.list.setstatus(index, "off")

        os.startfile(path)

def start():
    root = Tk()
    root.wm_title('AnimeGo')
    app = App(root)

    root.mainloop()