"""
Implementation of waveshare v3 touch screnn
"""
import asyncio
from waveshare.v3.epd2in13_V3 import EPD
from waveshare.v3.gt1151 import GT_Development, GT1151

def is_waveshare():
    #TODO : test waveshare HW presence
    return True

class WaveshareV3:

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        self._flag_t = 1
        self._layout = {
            "width": 250,
            "height": 122,
        }

        self.init_display()

    def clear(self):
        self._flag_t = 0
        self._display.Clear(0xff)


    def init_display(self):
        print("initializing waveshare v3 display")
        
        self._display = EPD()
        self._display.init(self._display.FULL_UPDATE)
        self._display.Clear(0xff)
        self._display.init(self._display.PART_UPDATE)

        print("intializing waveshare v3 touch display")
            
        self._gt = GT1151()
        self._GT_Dev = GT_Development()
        self._GT_Old = GT_Development()
        self._gt.GT_Init()

        asyncio.run_coroutine_threadsafe(self.pthread_irq(), loop=self._loop)

        asyncio.run_coroutine_threadsafe(self.pthread_touch(), loop=self._loop)

    def pthread_irq(self) :
        #touch irq thread running
        while self._flag_t == 1 :
            if(self._gt.digital_read(self._gt.INT) == 0) :
                self._GT_Dev.Touch = 1
            else :
                self._GT_Dev.Touch = 0
        print("waveshare touch irq thread stopping")

    def pthread_touch(self):
        #touch thread running
        while self._flag_t == 1 :
            # Read the touch input
            self._gt.GT_Scan(self._GT_Dev, self._GT_Old)
            if (self._GT_Old.X[0] == self._GT_Dev.X[0] and self._GT_Old.Y[0] == self._GT_Dev.Y[0] and self._GT_Old.S[0] == self._GT_Dev.S[0]):
                continue
        
            if (self._GT_Dev.TouchpointFlag):
                self._GT_Dev.TouchpointFlag = 0

                #if 3 points, shutdown
                if self._GT_Dev.TouchCount > 2:
                    self.clear()
                    #TODO shutdown
                    break

                #change to same scale as display
                x = self._layout['width'] - self._GT_Dev.Y[0]
                y = self._GT_Dev.X[0]

                #touch keyboard layout
                if x > 210 and x < 250 and y > 109 and y < 122 :
                    #TODO
                    continue
                
        
