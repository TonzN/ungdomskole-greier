import math
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Quick Sort")

class Prop:
  RectW = 3
  length = 255
  delay = 0
  mult = 2
  MaxMult = 1
  screenL = 600
  speed = 95

  def Cspeed(self):
    self.delay = 100 - self.speed
  def Cmult(self):
    placeH = self.length // 100
    if placeH <= 1:
      return
    else:
      for i in range(0, placeH-1):
        placeH -= 2
        print(i)
        if placeH <= 1:
          placeH = 1
        self.MaxMult = placeH
      if self.mult > self.MaxMult:
        self.mult = self.MaxMult 

Prop.Cspeed(Prop)
  
class Ui:
    def __init__(self, x, y, w, h, c1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h 
        self.c1 = c1
    def draw(self):
      pygame.draw.rect(screen, self.c1, (self.x, self.y, self.w, self.h))
    def switch(self, h):
      self.h = h
      self.y = Prop.screenL - self.h 
    def Color(self, C):
      self.c1 = C

def QuickSort(A, left, right, Rect):
  if left < right:  
    p = partition(A, left, right, Rect)
    QuickSort(A, left, p-1, Rect) 
    QuickSort(A, p+1, right, Rect) 
def partition(A, left, right, Rect):
  mid = (left+right)//2
  pivitV = A[mid]
  L = left
  R = right 
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
    screen.fill((0,0,0)) 
    if Prop.speed < 100 :
      pygame.time.delay(Prop.delay)
      Ui.Color(Rect[R], (255,0,0))
      Ui.Color(Rect[L], (255,0,0))
      Ui.Color(Rect[mid], (0,255,0))
      for i in range (0, len(Rect)-1):
        Ui.draw(Rect[i])
      pygame.display.update()
      Ui.Color(Rect[R], (255,255,255))
      Ui.Color(Rect[L], (255,255,255))
    while A[L] < pivitV:
      L += 1 
    while A[R] > pivitV: 
      R -=1  
    if L < R:
      if A[L] == A[R]:
        L += 1
      A[R], A[L] = A[L], A[R]
      placeholder = Rect[R].h
      Ui.switch(Rect[R], Rect[L].h)
      Ui.switch(Rect[L], placeholder)
    else:
      Ui.Color(Rect[mid], (255, 255, 255))
      return L

Stats = []
Rect = []

#Genererer Søyler
def ran():
  Stats.clear()
  Rect.clear()
  Temp = []
  for i in range(1, Prop.length):
    list.append(Temp, i*Prop.mult)
  for i in range(1, Prop.length):
    N = random.randint(0, random.randint(0, len(Temp)-1)) 
    list.append(Stats, Temp[N])
    D = Ui(Prop.RectW * i * 1.05, Prop.screenL-Temp[N], Prop.RectW-0.5, Temp[N],(255,255,255))
    list.append(Rect, D)
    del Temp[N]
  Temp.clear()

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    if event.type == pygame.MOUSEBUTTONUP:
      CD = False
  pygame.time.delay(50)
  ran()
  QuickSort(Stats, 0, len(Stats)-1, Rect) 
  pygame.time.delay(500)
  screen.fill((0,0,0))
  for i in range(0, len(Rect)-1):
    Ui.draw(Rect[i]) 
  pygame.display.update()





