'''
ImagePanel.py
Authors: afraser
'''

import wx
import ImageTools
from Properties import Properties
from DropTarget import DropTarget

p = Properties.getInstance()



class ImagePanel(wx.Panel, DropTarget):
    def __init__(self, imgs, chMap, parent, scale=1.0, brightness=1.0):
        self.chMap       = chMap
        self.toggleChMap = chMap[:]
        self.images      = imgs                                         # image channel arrays
        self.bitmap      = ImageTools.MergeToBitmap(imgs,
                                                    chMap = chMap,
                                                    scale = scale,
                                                    brightness = brightness)   # displayed wx.Bitmap
        
        wx.Panel.__init__(self, parent, wx.NewId(), size=self.bitmap.Size)
        
        self.scale          = scale
        self.brightness     = brightness
        self.selected       = False
        self.selectedPoints = []
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        
    def OnPaint(self, evt):
        self.SetClientSize((self.bitmap.Width, self.bitmap.Height))
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.bitmap, 0, 0)
        
        for (x,y) in self.selectedPoints:
#            x*=self.scale
#            y*=self.scale
            x = x * self.scale - 2
            y = y * self.scale - 2
            w = h = 4
            
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("WHITE",1))
            dc.SetBrush(wx.Brush("WHITE", style=wx.TRANSPARENT))
#            dc.DrawLine(x-2,y-2,x+2,y+2)
#            dc.DrawLine(x+2,y-2,x-2,y+2)
            dc.DrawRectangle(x,y,w,h)
            dc.EndDrawing()
        
        if self.selected:
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("WHITE",1))
            dc.SetBrush(wx.Brush("WHITE", style=wx.TRANSPARENT))
            dc.DrawRectangle(1,1,self.bitmap.Width-1,self.bitmap.Height-1)
            dc.EndDrawing()


    def UpdateBitmap(self):
        self.bitmap = ImageTools.MergeToBitmap(self.images,
                                               chMap = self.chMap,
                                               brightness = self.brightness,
                                               scale = self.scale)
        self.Refresh()
            
    
    def MapChannels(self, chMap):
        ''' Recalculates the displayed bitmap for a new channel-color map. '''
        self.chMap = chMap
        self.UpdateBitmap()
        

    def SetScale(self, scale):
        if scale != self.scale:
            self.scale = scale
            self.UpdateBitmap()
            self.SetClientSize((self.bitmap.Width, self.bitmap.Height))

        
    def SetBrightness(self, brightness):
        if brightness != self.brightness:
            self.brightness = brightness
            self.UpdateBitmap()
        

    def ReceiveDrop(self, data):
        # Pass drop data on to parent if it is a DropTarget
        if issubclass(self.GetParent().__class__, DropTarget):
            self.GetParent().ReceiveDrop(data)

    
    def SelectPoints(self, coordList):
        self.selectedPoints = coordList
        self.Refresh()
            


