import wx

class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self,parent,title = title)
        
        self.CreateStatusBar()
        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "About", "Information about this application")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "Exit", "Terminate the application")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "File")
        self.SetMenuBar(menuBar)
        
        btnSearch = wx.Button(self,wx.ID_ANY,'Search')
        
        self.Bind(wx.EVT_MENU,self.onAbout,menuAbout)
        self.Bind(wx.EVT_MENU,self.onExit,menuExit)
        self.Bind(wx.EVT_BUTTON,self.onSearch,btnSearch)
        
        #self.control = wx.TextCtrl(self)
        self.Show(True)
        
    def onSearch(self,e):
        return
    
    def onAbout(self,e):
        dlg = wx.MessageDialog(self, "A small text editor.", \
            "About Sample Editor", wx.OK)    
        dlg.ShowModal()    
        dlg.Destroy()  
        
    def onExit(self,e):
        self.Close(True)
        
app = wx.App(False)
frame = MainWindow(None,'AnimeGo')
app.MainLoop()