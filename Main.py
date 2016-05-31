import pygame
from pygame.locals import *
import math

pygame.init()
pygame.key.set_repeat(1,0)

class Main(object):

    def __init__(self):
        
        #define play area
        screenSize = [650,400]
        surface = pygame.display.set_mode(screenSize)

        #define variables such as colours and initial conditions
        background = [255,255,255]

        #define objects
        box = Box(0)

        #object initial conditions
        box.centre = [75,75]

        done = False
        
        while not done:
            
            #draw background
            surface.fill(background)

            #update objects
            box.update(screenSize)
            box.draw(surface)
            
            #display screen
            

            events = pygame.event.get()

            try: inputMap = inputMap
            except: inputMap = [0, 0]

            for e in events:
                if e.type is QUIT:
                    done = True
                if e.type is KEYDOWN:
                    if e.key == K_q:
                        done = True
                    elif e.key == K_w:
                        inputMap[1] = -1
                    elif e.key == K_s:
                        inputMap[1] = 1
                    elif e.key == K_a:
                        inputMap[0] = -1
                    elif e.key == K_d:
                        inputMap[0] = 1
                    elif e.key == K_SPACE:
                        box.attacking = True
                if e.type is KEYUP:
                    if e.key == K_w:
                        inputMap[1] = 0
                    elif e.key == K_s:
                        inputMap[1] = 0
                    elif e.key == K_a:
                        inputMap[0] = 0
                    elif e.key == K_d:
                        inputMap[0] = 0
                
                        

                
            if inputMap[0] == 1:
                box.vel[0] = 5
            elif inputMap[0] == -1:
                box.vel[0] = -5
            else:
                box.vel[0] = 0
            if inputMap[1] == 1:
                box.vel[1] = 2
            elif inputMap[1] == -1:
                if box.jumpcount > 0:
                    box.vel[1] = -10
                    box.jumpcount -= 1
                
                
            #update and wait tick time
            pygame.display.flip()
            pygame.time.wait(25)


class Box(object):
    
    def __init__(self, ident):
        self.hp = 10
        self.centre = [25,25]
        self.size = 50
        self.colour = [0,0,0]
        self.weaponcolour = [165,0,0]
        self.vel = [0,0]
        self.identity = ident
        self.wepang = 0
        self.attacking = False
        self.angle = 0
        self.direction = 0 #1 = moving right 0= idle -1 = moving left
        self.jumpcount = 1

    def update(self, screenSize):
        self.vel[1] += 0.445
        if(self.centre[0]+(self.size/2)+self.vel[0] > screenSize[0] or self.centre[0]-(self.size/2)+self.vel[0] < 0):
            self.vel[0] *= -0.4
        if(self.centre[1]+(self.size/2)+self.vel[1] > screenSize[1]):
            self.vel[1] *= -0.2
            self.jumpcount = 1
        if(self.centre[1]-(self.size/2)+self.vel[1] < 0):
            self.vel[1] *= -0.4
        if self.vel[1]*self.vel[1] < 0.05:
            self.vel[1] = 0
        if self.vel[0] > 0:
            self.direction = 1
        if self.vel[0] == 0:
            self.direction = 0
        if self.vel[0] < 0:
            self.direction = -1

        self.centre = (self.centre[0]+self.vel[0],self.centre[1]+self.vel[1])

        
    def draw(self, surface):
        #define variables
        self.topleft = (self.centre[0]-(self.size/2),self.centre[1]-(self.size/2))
        self.dimensions = (self.size,self.size)
        if(self.direction == 0 or self.direction == 1):
            self.weaponanchor = [self.topleft[0]+self.size-5, self.topleft[1]]
        else:
            self.weaponanchor = [self.topleft[0]-10, self.topleft[1]]

        #draw it
        body = pygame.Rect(self.topleft,self.dimensions)
        pygame.draw.rect(surface, self.colour, body)

        weapon = pygame.image.load('sword.png')
        if(self.attacking == True):
            self.wepang += 10
            if self.wepang > 240:
                self.attacking = False
                self.wepang = 0

        if self.wepang <= 120:
            self.angle = self.wepang
        else:
            self.angle = 240-self.wepang
        prex, prey = weapon.get_size()
        if(self.direction >= 0):
            weapon = pygame.transform.rotate(weapon, -self.angle)
            postx, posty = weapon.get_size()
            surface.blit(weapon,[round(self.weaponanchor[0]+(prex+postx)/7-5),round(self.weaponanchor[1]-(prey+posty)/2+40+self.angle/7)])
        else:
            weapon = pygame.transform.rotate(weapon, self.angle)
            postx, posty = weapon.get_size()
            surface.blit(weapon,[round(self.weaponanchor[0]-(prex+postx)+30),round(self.weaponanchor[1]-(prey+posty)/2+40+self.angle/7)])        
        
        

        #debug
        velstr = str(("hp:",self.hp,"x:",self.vel[0],"y:",str(self.vel[1])[0:4],"id:",self.identity))
        font = pygame.font.SysFont("monospace", 15)
        label = font.render(velstr.encode(), 1, (0,0,0))
        surface.blit(label, (0,self.identity*20))
        
    def paint(self, surface):
        painting = pygame.image.load('sword.png')
        surface.blit(painting, [100,100])
        
Main()
pygame.quit()