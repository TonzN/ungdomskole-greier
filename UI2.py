import pygame
import math
import random
import time
import os

Bools = {
    "CD": False
}

def LinearSearch(l, n):
    # l = list
    for i, v in enumerate(l):
        if v == n:
            return i
    return False

ScreenSize = None

class Folder:
    def __init__(self):
        self.Objs = {}
        self.Size = len(self.Objs)
    def Clear(self):
        self.Objs = {}

class RenderQueue:
    def __init__(self, Queue = []):
        self.Queue = Queue
    
    def Push(self, n):
        self.Queue.append(n)

    def AddObjects(self, n):
        for i in n:
            if type(n[i]) == list:
                self.AddObjects(n[i])
            else:
                self.Push(n[i])

    def Pop(self):
        if self.Queue:
          del self.Queue[0]
        
    def Remove(self, n):
        item = LinearSearch(self.Queue, n)
        if item:
            self.Queue.pop(item)

MainRenderQueue = RenderQueue()

class NewWindow:
    def __init__(self, Name = "MyGame", BGColor = (60,60,60), Size = (800,600), TargetFps = 60):
        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen = pygame.display.set_mode(Size)
        self.prev_time = time.time()
        self.Target_fps = TargetFps
        self.Size = Size
        self.CDdel = time.time()
        self.BGColor = BGColor
        pygame.display.set_caption(Name)
    
    def RenderObjects(self, Layers = None):
        queue = RenderQueue()
        for i in MainRenderQueue.Queue:
            i.Redraw()
        if Layers:
            for i in Layers:
                queue.AddObjects(i)
            for i in queue.Queue:
                i.Redraw()
        
    def NextFrame(self, Layers = None):
        EventHandler()
        self.RenderObjects(Layers)
        pygame.display.update()

        if time.time() - self.CDdel >= 0.05: 
            CDdel = time.time()
            Bools["CD"] = False
        #-------FPS--------#
        curr_time = time.time()#
        diff = curr_time - self.prev_time#frame took this much time to process and render
        delay = max(1.0/self.Target_fps - diff, 0)
        time.sleep(delay)
        fps = 1.0/(delay + diff)#fps is based on total time ("processing" diff time + "wasted" delay time)
        prev_time = curr_time
        self.screen.fill(self.BGColor)

def runEvents(Objects = False): #Runs object functions. 
    #Objects er bare en array med alle objektene som har events so skal kjøres
    if Objects:
        for i in Objects:
            i.CheckEvents()

def EventHandler(): #Finder hendelser for vinduet
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        if e.type == pygame.MOUSEBUTTONUP:
            Bools["CD"] = False
 
class Rect:
    def __init__(self, screen, x, y, width, height, c1, c2 = False, Render = True): #innehold til en Ui
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height
        self.c1     = c1
        self.c2     = c2
        self.Render = Render
        self.screen = screen
        self.autoScale = False#AutoScale
        if Render:
            if self.autoScale:
                self.AutoScale()
            pygame.draw.rect(screen, c1, (x, y, self.width, self.height))

    def Click(self): #finner mus klikk op posisjonen returnerer True viss du klikker
        mouseP = pygame.mouse.get_pos()
        click  = pygame.mouse.get_pressed()
        if self.Render:
            if self.x + self.width > mouseP[0] > self.x and self.y + self.height > mouseP[1] > self.y:  
                # Hvis mus x og y kordnitaer er riktig/ peker på knappen
                pygame.draw.rect(self.screen, self.c2, (self.x, self.y, self.width, self.height))
                if click[0] == 1 and Bools["CD"] == False:
                    Bools["CD"] = True
                    return True
                return False

    def AutoScale(self): #In %
        self.width, self.height = (ScreenSize[0]/100)*self.width, (ScreenSize[1]/100)*self.height

    def Redraw(self):
       if self.Render:         
            pygame.draw.rect(self.screen, self.c1, (self.x, self.y, self.width, self.height))
    
    def AddText(self, tC, tT, tS):
        font = pygame.font.Font('freesansbold.ttf', tS) #font
        text = font.render(tT, Render, tC)
        textRect = text.get_rect()
        textRect.center = (x + (width // 2), y + (height // 2)) #plasserer teksten i midten
        self.screen.blit(text, textRect)

    def AddToRenderQueue(self, queue):
        if queue:
            queue.Push(self)
        else:
            MainRenderQueue.Push(self)

class Ball():
    def __init__(self, screen, x, y, radius, color1, Render = True):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color1
        self.Visible = Render
        self.Screen = screen
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def AddToRenderQueue(self, RQ = MainRenderQueue):
        RQ.Push(self)
    
    def Redraw(self):
        print(self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.Screen, self.color, (self.x, self.y), self.radius)
    
    
class TextLabel(Rect):
        #Info om varibaler
        #c1/c2 = color1/color2
        def __init__(self, screen, x, y, width, height, c1, tC, tT, tS, Render = True):
            self.tC = tC #TextColor
            self.tS = tS #tSize
            self.tT = tT #tType
            super().__init__(screen,x, y, width, height, c1, False, Render)
            if tT:
                self.AddText(tC, tT, tS)
    
class Button(Rect):
        def __init__(self,screen, x, y, width, height, c1, c2, Event = False, Input = False, RQ = MainRenderQueue, Render = True):
            self.Event = Event #Hendelse etter du trykker
            self.Input = Input #Input = funksjon input
            self.tT = None
            self.tS = None 
            self.tC = None
            super().__init__(screen, x, y, width, height, c1, c2, Render)
            self.RQ = RQ
            self.AddToRenderQueue(self.RQ)

        def CheckEvents(self): #Methods Uten return
            hit = self.Click()
            MEvent = False
            if hit :
                MEvent = True
                if self.Event:
                    if self.Input:
                        self.Event(self.Input)
                    else:
                        self.Event()
          
        def runEvent(self, event, input = False):#Method som returner 
            Hit = self.Click()
            if Hit and event:
                Output = None
                if input:
                    Output = event(input)
                else:
                    Output = event()
                return Output
            else:
                return False

class Frame(Rect):
    def __init__(self,screen, x, y, width, height, c1 ):
        super().__init__(screen,x, y, width, height, c1)    

