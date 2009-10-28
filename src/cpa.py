import wx
import logging
import threading
from util import get_icon
from ClassifierGUI import *
from ImageViewer import ImageViewer
from wx.lib.embeddedimage import PyEmbeddedImage
try:
    from version import VERSION as __version__
except ImportError:
    __version__ = 'unknown revision'

# Toolbar icons
imviewer_icon = PyEmbeddedImage('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')
datatable_icon = PyEmbeddedImage('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')
classifier_icon = PyEmbeddedImage('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')
pmb_icon = PyEmbeddedImage('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')
scatter_icon = PyEmbeddedImage('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')

ID_CLASSIFIER = wx.NewId()
ID_PLATE_MAP_BROWSER = wx.NewId()
ID_DATA_TABLE = wx.NewId()
ID_SCATTER = wx.NewId()
ID_IMAGE_VIEWER = wx.NewId()


class FuncLog(logging.Handler):
    '''
    A logging handler that sends logs to an update function
    '''
    def __init__(self, update):
        logging.Handler.__init__(self)
        self.update = update
                
    def emit(self, record):
        self.update(self.format(record))


class MainGUI(wx.Frame):
    '''
    GUI for CellProfiler Analyst
    '''
    def __init__(self, properties, parent, id=-1, **kwargs):
        wx.Frame.__init__(self, parent, id=id, title='CellProfiler Analyst 2.0', **kwargs)
        
        self.properties = properties
        self.tbicon = wx.TaskBarIcon()
        self.tbicon.SetIcon(get_icon(), 'CellProfiler Analyst 2.0')
        self.Center(wx.HORIZONTAL)
        self.CreateStatusBar()
        
        #
        # Setup toolbar
        #
        self.tb = self.CreateToolBar(wx.TB_HORIZONTAL|wx.NO_BORDER|wx.TB_FLAT)
        self.tb.SetToolBitmapSize((32,32))
        self.tb.AddTool(ID_CLASSIFIER, classifier_icon.GetBitmap(), shortHelpString='Classifier', longHelpString='Launch Classifier')
        self.tb.AddTool(ID_PLATE_MAP_BROWSER, pmb_icon.GetBitmap(), shortHelpString='Plate Viewer', longHelpString='Launch Plate Viewer')
        self.tb.AddTool(ID_DATA_TABLE, datatable_icon.GetBitmap(), shortHelpString='DataTable', longHelpString='Launch DataTable')
        self.tb.AddTool(ID_SCATTER, scatter_icon.GetBitmap(), shortHelpString='Scatter Plot', longHelpString='Launch Scatter Plot')
        self.tb.AddTool(ID_IMAGE_VIEWER, imviewer_icon.GetBitmap(), shortHelpString='ImageViewer', longHelpString='Launch ImageViewer')
        self.tb.Realize()
        
        #
        # Setup menu items
        #
        self.SetMenuBar(wx.MenuBar())
        fileMenu = wx.Menu()
        saveLogMenuItem = fileMenu.Append(-1, 'Save Log\tCtrl+S', help='Save the contents of the log window.')
        fileMenu.AppendSeparator()
        self.exitMenuItem = fileMenu.Append(ID_EXIT, 'Exit\tCtrl+Q', help='Exit classifier')
        self.GetMenuBar().Append(fileMenu, 'File')

        toolsMenu = wx.Menu()
        classifierMenuItem  = toolsMenu.Append(ID_CLASSIFIER, 'Classifier\tCtrl+Shift+C', help='Launches Classifier.')
        plateMapMenuItem    = toolsMenu.Append(ID_PLATE_MAP_BROWSER, 'Plate Viewer\tCtrl+Shift+P', help='Launches the Plate Viewer tool.')
        dataTableMenuItem   = toolsMenu.Append(ID_DATA_TABLE, 'Data Table\tCtrl+Shift+T', help='Launches the Data Table tool.')
        scatterMenuItem     = toolsMenu.Append(ID_SCATTER, 'Scatter Plot\tCtrl+Shift+A', help='Launches the Scatter Plot tool.')
        imageViewerMenuItem = toolsMenu.Append(ID_IMAGE_VIEWER, 'Image Viewer\tCtrl+Shift+I', help='Launches the ImageViewer tool.')
        self.GetMenuBar().Append(toolsMenu, 'Tools')

        logMenu = wx.Menu()        
        debugMenuItem    = logMenu.AppendRadioItem(-1, 'Debug\tCtrl+1', help='Logging window will display debug-level messages.')
        infoMenuItem     = logMenu.AppendRadioItem(-1, 'Info\tCtrl+2', help='Logging window will display info-level messages.')
        warnMenuItem     = logMenu.AppendRadioItem(-1, 'Warnings\tCtrl+3', help='Logging window will display warning-level messages.')
        errorMenuItem    = logMenu.AppendRadioItem(-1, 'Errors\tCtrl+4', help='Logging window will display error-level messages.')
        criticalMenuItem = logMenu.AppendRadioItem(-1, 'Critical\tCtrl+5', help='Logging window will only display critical messages.')
        infoMenuItem.Check()
        self.GetMenuBar().Append(logMenu, 'Logging')
        
        # console and logging
        self.console = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.console.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.console.SetBackgroundColour('#111111')
        
        self.console.SetForegroundColour('#DDDDDD')
        log_level = logging.DEBUG
        self.logr = logging.getLogger()
        self.log_text = ''
        def update(x):
            self.log_text += x+'\n'
        hdlr = FuncLog(update)
#        hdlr.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
#        hdlr.setFormatter(logging.Formatter('%(levelname)s | %(name)s | %(message)s [@ %(asctime)s in %(filename)s:%(lineno)d]'))
        self.logr.addHandler(hdlr)
        # hackish: log_levels ids are 10,20,30,40,50
        logMenu.GetMenuItems()[(log_level/10)-1].Check()
        logging.info('Logging level: %s'%(logging.getLevelName(log_level)))
        
        self.Bind(wx.EVT_MENU, lambda(_):self.set_log_level(logging.DEBUG), debugMenuItem)
        self.Bind(wx.EVT_MENU, lambda(_):self.set_log_level(logging.INFO), infoMenuItem)
        self.Bind(wx.EVT_MENU, lambda(_):self.set_log_level(logging.WARN), warnMenuItem)
        self.Bind(wx.EVT_MENU, lambda(_):self.set_log_level(logging.ERROR), errorMenuItem)
        self.Bind(wx.EVT_MENU, lambda(_):self.set_log_level(logging.CRITICAL), criticalMenuItem)
        self.Bind(wx.EVT_MENU, self.save_log, saveLogMenuItem)
        self.Bind(wx.EVT_MENU, self.launch_classifier, classifierMenuItem)
        self.Bind(wx.EVT_MENU, self.launch_plate_map_browser, plateMapMenuItem)
        self.Bind(wx.EVT_MENU, self.launch_data_table, dataTableMenuItem)
        self.Bind(wx.EVT_MENU, self.launch_scatter_plot, scatterMenuItem)
        self.Bind(wx.EVT_MENU, self.launch_image_viewer, imageViewerMenuItem)
        self.Bind(wx.EVT_TOOL, self.launch_classifier, id=ID_CLASSIFIER)
        self.Bind(wx.EVT_TOOL, self.launch_plate_map_browser, id=ID_PLATE_MAP_BROWSER)
        self.Bind(wx.EVT_TOOL, self.launch_data_table, id=ID_DATA_TABLE)
        self.Bind(wx.EVT_TOOL, self.launch_scatter_plot, id=ID_SCATTER)
        self.Bind(wx.EVT_TOOL, self.launch_image_viewer, id=ID_IMAGE_VIEWER)        
        self.Bind(wx.EVT_MENU, self.on_close, self.exitMenuItem)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_IDLE, self.on_idle)

        
    def launch_classifier(self, evt=None):
        classifier = wx.FindWindowByName('Classifier')
        if classifier:
            classifier.Show()
            classifier.SetFocus()
            logging.warn('You may only run one instance of Classifier at a time.')
            return
        classifier = ClassifierGUI(parent=self, properties=self.properties)
        classifier.Show(True)
        
    def launch_plate_map_browser(self, evt=None):
        self.pmb = PlateMapBrowser(parent=self)
        self.pmb.Show(True)
    
    def launch_data_table(self, evt=None):
        table = DataGrid(parent=self)
        table.Show(True)
        
    def launch_scatter_plot(self, evt=None):
        scatter = Scatter(parent=self)
        scatter.Show(True)
#        import cellprofiler.gui.cpfigure as cpfig
#        figure = cpfig.create_or_find(self, -1, 'scatter', subplots=(1,1), name='scatter')
#        table = np.random.randn(5000,2)
#        figure.panel.subplot_scatter(0, 0, table)

    def launch_image_viewer(self, evt=None):
        imviewer = ImageViewer(parent=self)
        imviewer.Show(True)
        
    def save_log(self, evt=None):
        logging.error('"Save Log" feature not yet implemented')
        
    def set_log_level(self, level):
        self.logr.setLevel(level)
        # cheat the logger so these always get displayed
        self.console.AppendText('Logging level: %s\n'%(logging.getLevelName(level)))

    def on_close(self, evt=None):
        # Classifier needs to be told to close so it can clean up it's threads
        classifier = wx.FindWindowByName('Classifier') or wx.FindWindowById(ID_CLASSIFIER)
        if classifier and classifier.Close() == False:
            return
        self.Destroy()
        
    def on_idle(self, evt=None):
        if self.log_text != '':
            self.console.AppendText(self.log_text)
            self.log_text = ''
        




def load_properties():
    dlg = wx.FileDialog(None, "Select a the file containing your properties.", style=wx.OPEN|wx.FD_CHANGE_DIR)
    if dlg.ShowModal() == wx.ID_OK:
        filename = dlg.GetPath()
        os.chdir(os.path.split(filename)[0])      # wx.FD_CHANGE_DIR doesn't seem to work in the FileDialog, so I do it explicitly
        p.LoadFile(filename)
    else:
        print 'CellProfiler Analyst requires a properties file.  Exiting.'
        exit()




if __name__ == "__main__":
    import sys
    import logging

    logging.basicConfig(level=logging.DEBUG)
    
    global defaultDir
    defaultDir = os.getcwd()
    
    # Handles args to MacOS "Apps"
    if len(sys.argv) > 1 and sys.argv[1].startswith('-psn'):
        del sys.argv[1]

    # Initialize the app early because the fancy exception handler
    # depends on it in order to show a dialog.
    app = wx.PySimpleApp()
    
    # Install our own pretty exception handler unless one has already
    # been installed (e.g., a debugger)
    if sys.excepthook == sys.__excepthook__:
        sys.excepthook = show_exception_as_dialog

    p = Properties.getInstance()
    db = DBConnect.DBConnect.getInstance()
    dm = DataModel.getInstance()

    # Load a properties file if passed in args
    if len(sys.argv) > 1:
        propsFile = sys.argv[1]
        p.LoadFile(propsFile)
    else:
        load_properties()
        
    dm.PopulateModel()
    MulticlassSQL.CreateFilterTables()


    cpa = MainGUI(p, None)
    cpa.Show(True)
    app.MainLoop()
    
    
    
    