# _______          __                 
# \      \   _____/  |_  ____   ______
# /   |   \ /  _ \   __\/ __ \ /  ___/
#/    |    (  <_> )  | \  ___/ \___ \ 
#\____|__  /\____/|__|  \___  >____  >
#        \/                 \/     \/
#
##room designs [3/10]
##room_0-st ei saa tagasi liikuda, room_1-st ka
##leiutada mingid teleporterid?
##HELITUGEVUSED!
##Lisa 9_corrupted.wav
##Lisa l6pp, aktiveerub kui k6ik teibid l2bi [mitte kui viimane yles korjata]
##Muuda spawn_chance 6igeks
##vt kas saad panna reseti staffi mingisse funkziooni
##1x1 gapi ei saa sisse hypata
##lvl0->lvl99 lvl99->lvl0
##[space] - shoot on controls screenilt puudu
##
##turret on OP
##vb kontrollida kas player.y ja turret.y vahe on abs v2iksem mingi 16-st v6i nii, siis ei lase nii lambist ehk
##kuuli v6ib ka aeglasemaks teha

import os;
import random;
import pygame;
from math import sqrt

def sign(x):
    if x==0:
        return 0
    return(x/abs(x))
    
def point_distance(x1,y1,x2,y2):
    l1=abs(x2-x1);
    l2=abs(y2-y1);
    return(sqrt(l1**2+l2**2))    
    
def table_add_entry(table,name,xcoord,ycoord,scale=1):
    if table==enemytable:
        table[curlev].append(name+"(("+str(xcoord)+","+str(ycoord)+"),"+str(scale)+")")
    else:
        table[curlev].append(name+"(("+str(xcoord)+","+str(ycoord)+"))")
    ##DEBUG
    if table==loottable:
        print("added entry: "+name+"(("+str(xcoord)+","+str(ycoord)+"))"+" to table: loottable, location: "+str(curlev))
    elif table==traptable:
        print("added entry: "+name+"(("+str(xcoord)+","+str(ycoord)+"))"+" to table: traptable, location: "+str(curlev))
    elif table==enemytable:
        print("added entry: "+name+"(("+str(xcoord)+","+str(ycoord)+"),"+str(scale)+")"+" to table: enemytable, location: "+str(curlev))
        
def table_remove_entry(table,name,xcoord,ycoord,scale=1):
    if table==enemytable:
        table[curlev].remove(name+"(("+str(xcoord)+","+str(ycoord)+"),"+str(scale)+")")
    else:
        table[curlev].remove(name+"(("+str(xcoord)+","+str(ycoord)+"))")
    if table==loottable:
        print("removed entry: "+name+"(("+str(xcoord)+","+str(ycoord)+"))"+" from table: loottable, location: "+str(curlev))
    elif table==traptable:
        print("removed entry: "+name+"(("+str(xcoord)+","+str(ycoord)+"))"+" from table: traptable, location: "+str(curlev))
    elif table==enemytable:
        print("removed entry: "+name+"(("+str(xcoord)+","+str(ycoord)+"),"+str(scale)+")"+" from table: enemytable, location: "+str(curlev))

def load_level(num,d):
    TOTAL_WIDTH = 0
    TOTAL_HEIGHT = 0
    x = y = 0
    print("____________\nloading room layout from: data/rooms/room"+str(num)+".txt"+"\nposition in list: "+str(curlev))
    print(traptable)
    print(enemytable)
    print(loottable)
    f=open(FLD_ROOM+"room"+str(num)+".txt")
    try:
        for i in traptable[curlev]:
            eval(i)
            print(i)
            print("loaded entry: "+i+" from table: traptable, location "+str(curlev))
        for i in loottable[curlev]:
            eval(i)
            print("loaded entry: "+i+" from table: loottable, location "+str(curlev))
        for i in enemytable[curlev]:
            eval(i)
            print("loaded entry: "+i+" from table: enemytable, location "+str(curlev))
        enemytable[curlev] = []
        print("table enemytable cleared")
        generated = True
        print("loading tables for level ",curlev)
    except:
        generated=False
        traptable[curlev] = []
        loottable[curlev] = []
        enemytable[curlev] = []
        print("creating tables for level",curlev)
        
    for row in f:
        for col in row:
            if col=="W":
                Wall((x, y))
            elif col=="F":
                Exit((x, y),1)
            elif col=="B":
                Exit((x, y),-1)
            elif col=="I":
                if not generated:
                    rnum=random.randint(0,100)
                    if rnum<25:
                        Ammunition((x,y));
                        table_add_entry(loottable,"Ammunition",x,y)
                    elif rnum<95:           ##VAHETA 2RA!
                        TriggerAudio((x,y));
                        table_add_entry(loottable,"TriggerAudio",x,y)
            elif col=="a":
                WaterTop((x,y))
            elif col=="A":
                WaterBody((x,y))
            elif col=="!":
                Spike((x,y))
            elif col=="_":
                Badfloor((x,y))
            elif col=="E":
                if not generated:   ##random VA?
                    #Walker((x, y),1)
                    Turret((x,y),1)
            elif col=="r":
                EnemyBlocker((x, y))
            elif col=="S":
                if d==1:
                    player.rect.x = x
                    player.rect.y = y
            elif col=="s":
                if d==-1:
                    player.rect.x = x
                    player.rect.y = y
            elif col=="T":
                if not generated:
                    rnum=random.randint(0,100)
                    if (rnum<25):
                        Wall((x,y))
                        table_add_entry(traptable,"Wall",x,y)
                    elif (rnum<50):
                        Spike((x,y))
                        table_add_entry(traptable,"Spike",x,y)      
            elif col=="D":
                if not generated:
                    rnum=random.randint(0,100)
                    if (rnum<25):
                        DecCross((x,y))
                        table_add_entry(traptable,"DecCross",x,y)
                    elif (rnum<50):
                        DecGrass((x,y))
                        table_add_entry(traptable,"DecGrass",x,y)      
                    elif (rnum<75):
                        DecFence((x,y))
                        table_add_entry(traptable,"DecFence",x,y)               
            x += 32
            if TOTAL_HEIGHT==0:
                TOTAL_WIDTH += 32
        y += 32
        x = 0
        TOTAL_HEIGHT += 32
    f.close()
    global cam
    cam = Camera(TOTAL_WIDTH-32,TOTAL_HEIGHT)
 
def image_animate(self):
    if (self.image_index<len(self.images)*30-self.image_speed):
        self.image_index += self.image_speed
    else:
        self.image_index = 0
    i=self.image_index

    self.image = self.images[(i//30)]
    if (self.image_xscale==-1):
        self.image = pygame.transform.flip(self.image, 1, 0)
        
def spriteobject(self,img,p):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(FLD_SPR+img+".bmp").convert()
    self.image.set_colorkey((0,128,0))
    self.rect = self.image.get_rect()
    self.rect.x = p[0]
    self.rect.y = p[1]
    
def animated_spriteobject(self,img,p,spd=0,xscale=1):
    pygame.sprite.Sprite.__init__(self)
    self.images = []
    for i in img:
        self.images.append(pygame.image.load(FLD_SPR+i+".bmp"))
    self.image=self.images[0]
    for i in self.images:
        i.set_colorkey((0,128,0))
    self.rect = self.image.get_rect()
    self.rect.x = p[0]
    self.rect.y = p[1]
    
    self.image_speed = spd
    self.image_index = 0
    self.image_xscale = xscale
    
#Klassid
        
class Player(pygame.sprite.Sprite):
    
    def __init__(self,pos):
        animated_spriteobject(self,["nih_sub_1","nih_sub_2","nih_sub_3","nih_sub_4"],pos)
        
        self.ground = False
        self.vspeed = 0
        self.maxspeed = 2
        self.speed = 0
    
    def move(self, dx, dy):
        
        self.rect.x += dx
        self.rect.y += dy

        if (dx!=0):
            if (self.image_xscale!=dx/abs(dx)):
                if not hand==None:
                    hand.image = pygame.transform.flip(hand.image, 1, 0)
                self.image_xscale *= -1;

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                    self.vspeed = 0;
                    self.ground = True;
                if dy < 0:
                    self.rect.top = wall.rect.bottom
                    self.vspeed = 0;
        if self.vspeed>0:
            self.ground = False
                    
    def gravity(self):
        self.vspeed += 0.2
        self.move(0,self.vspeed)

    def jump(self):
        if (self.ground):
            self.vspeed = -4.8
            self.ground = False

    def update(self):
        self.gravity()
        if not self.speed==0:
            self.move(self.speed,0)
        image_animate(self)

class Camera(object):
    
    def __init__(self, w, h):
        self.pos = pygame.Rect(0, 0, w, h)          #Loo kaamera jaoks rect, mis on sama suur kui level

    def shift(self, target):
        return target.rect.move(self.pos.topleft)   #Liiguta objekti s6ltuvalt kaamera positsioonist

    def update(self):                               #Liiguta kaamerat m2ngija j2rgi
        l, t = player.rect.left,player.rect.y
        w, h = self.pos.w,self.pos.h
        l = max(min(0,-l+320),-(w-640))
        t = max(min(0,-t+240),-(h-480))

        return pygame.Rect(l, t, w, h)

class Wall(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        walls.append(self);
        spriteobject(self,"sein",pos)

class Hand(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        animated_spriteobject(self,["revolver1","revolver2","revolver3"],pos,0)
        self.openimage=pygame.image.load(FLD_SPR+"revolver_open.bmp")
        self.openimage.set_colorkey((0,128,0))
        self.gunsound = pygame.mixer.Sound(FLD_SND+"shoot.wav")
        if (player.image_xscale==-1):
            self.image = pygame.transform.flip(self.image, 1, 0)

    def update(self):
        image_animate(self)
        self.image_xscale = player.image_xscale
        if self.image_xscale == 1:
            self.rect.x = player.rect.x
        else:
            self.rect.x=player.rect.x-24
        self.rect.y=player.rect.y
        if self.image_index>78:
            self.image_speed=0
            self.image_index=0

    def shoot(self):
        global loadedammo
        if loadedammo>0 and self.image_speed==0:
            pygame.mixer.Channel(1).play(self.gunsound)
            Bullet((player.rect.x-8,player.rect.y+14),player.image_xscale*8)
            loadedammo -= 1
            self.image_speed=6

class Badfloor(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        non_solids.append(self);
        spriteobject(self,"badfloor",pos)

class WaterBody(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        non_solids.append(self);
        spriteobject(self,"water_body",pos)

class WaterTop(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        traps.append(self);
        spriteobject(self,"water_top",pos)
        
class DecCross(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        non_solids.append(self)
        spriteobject(self,"cross",pos)

class DecGrass(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        non_solids.append(self)
        spriteobject(self,"grass",pos)
        
class DecFence(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        non_solids.append(self)
        spriteobject(self,"fence",pos)
        
class Ammunition(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        loot.append(self);
        spriteobject(self,"ammo",pos)
        
    def pickup(self):
        global ammo
        ammo += random.randint(3,6)
        table_remove_entry(loottable,"Ammunition",self.rect.x,self.rect.y)
        loot.remove(self)
        
class TriggerAudio(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        loot.append(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(FLD_SPR+"tape.bmp").convert()
        self.image.set_colorkey((0,128,0))
        self.rect = self.image.get_rect()
        self.start = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
    def pickup(self):
        if len(tapelist)>0:
            if pygame.mixer.Channel(0).get_busy()==0:
                self.tape = pygame.mixer.Sound(tapeaudio[tapelist[0]])
                pygame.mixer.Channel(0).play(self.tape)
                print("playing audio from: "+tapeaudio[tapelist[0]])
            else:
                tapequeue.append(tapeaudio[tapelist[0]])
                print("adding audio from: "+tapeaudio[tapelist[0]]+" to the queue")
            tapelist.remove(tapelist[0])
            table_remove_entry(loottable,"TriggerAudio",self.rect.x,self.rect.y)
            loot.remove(self)
        
class Spike(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        traps.append(self);
        spriteobject(self,"spikes",pos)

class Exit(pygame.sprite.Sprite):
    
    def __init__(self, pos, s):
        exits.append(self)
        self.s = s
        spriteobject(self,"exit",pos)

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, pos, hspeed):
        bullets.append(self)
        spriteobject(self,"bullet",pos)
        self.hspeed = hspeed

    def update(self):
        self.rect.x += self.hspeed
        for wall in walls:
            if (self.rect.colliderect(wall)):
                bullets.remove(self)

class Walker(pygame.sprite.Sprite):
    
    def __init__(self,pos,scale):
        exterminators.append(self)
        self.name = "Walker"
        animated_spriteobject(self,["walker1","walker2","walker3","walker4"],pos,4)
        self.image_xscale = scale
        self.hp = 2
    
    def update(self):
        self.rect.x += 2*self.image_xscale        ###!!! 2 == good difficulty, 1 == better looks [?]
        image_animate(self)
    
    def turn_around(self):
        self.image_xscale *= -1
        self.image = pygame.transform.flip(self.image, 1, 0)
        
class Turret(pygame.sprite.Sprite):
    
    def __init__(self,pos,xscale):
        exterminators.append(self)
        self.name = "Turret"
        spriteobject(self,"ext_turret",pos)
        self.shootdelay = 0
        self.image_xscale = xscale
        self.hp = 1
        
    def update(self):
        if self.shootdelay>0:
            self.shootdelay-=1
        else:
            if point_distance(self.rect.x,self.rect.y,player.rect.x,player.rect.y)<128:
                EnemyBullet((self.rect.x+12,self.rect.y+14),8)
                EnemyBullet((self.rect.x+12,self.rect.y+14),-8)
                self.shootdelay=30
        
class EnemyBullet(pygame.sprite.Sprite):
    
    def __init__(self, pos, hspeed):
        enemybullets.append(self)
        spriteobject(self,"enemybullet",pos)
        self.hspeed = hspeed

    def update(self):
        self.rect.x += self.hspeed
        for wall in walls:
            if (self.rect.colliderect(wall)):
                enemybullets.remove(self)
        
class EnemyBlocker(pygame.rect.Rect):
    
    def __init__(self,pos):
        blockers.append(self)
        self.rect = pygame.Rect(pos[0],pos[1],32,32)
        
class PlayerExplode(pygame.sprite.Sprite):
    
    def __init__(self,pos):
        animated_spriteobject(self,["explosion0","explosion1","explosion2","explosion3",
                                    "explosion4","explosion5","explosion6"],pos,6)
        player.speed=0
        global hand, tapequeue
        hand = None
        tapequeue = []
        pygame.mixer.Channel(0).stop()
    
    def update(self):
        global explosion
        image_animate(self)
        if self.image_index>192:
            explosion = None
        

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("DECEIT")
screen = pygame.display.set_mode((640, 480))

TAPE_END = pygame.USEREVENT + 1
FLD_SPR = "data/sprites/"
FLD_SND = "data/sound/"
FLD_ROOM = "data/rooms/"

pygame.mixer.Channel(0).set_endevent(TAPE_END)

hud_ammo_image = pygame.image.load(FLD_SPR+"hud_bullet.bmp").convert()
hud_ammo_image.set_colorkey((0,128,0))

restartimage = pygame.image.load(FLD_SPR+"restartimage.bmp").convert()
restartimage.set_colorkey((0,128,0))

snd_load = pygame.mixer.Sound(FLD_SND+"load_cartridge.wav")
snd_open = pygame.mixer.Sound(FLD_SND+"cylinder_open.wav")
snd_close = pygame.mixer.Sound(FLD_SND+"cylinder_close.wav")

cylinderimage = []
for i in range(7):
    cylinderimage.append(pygame.image.load(FLD_SPR+"cylinder000"+str(i)+".bmp"))
    cylinderimage[i].set_colorkey((0,128,0))
    print("loaded cylinder000"+str(i))
    
clock = pygame.time.Clock()
        
walls = []
traps = []
blockers = []
exterminators = []
exits = []
loot = []
bullets = []
enemybullets = []
non_solids = []
hand = None
player = Player((32,32))
curlev = 50;
explosion = None

loottable = {101:["loot"]}
traptable = {101:["trap"]}
enemytable = {101:["enemy"]}

ammo = random.randint(3,7)
loadedammo = random.randint(2,6)
draw_gui = False

levellist = []
for i in range(100):
    levellist.append(random.randint(0,9))
    
tapeaudio = {1:FLD_SND+"1_projection.wav",2:FLD_SND+"2_exterminators.wav",3:FLD_SND+"3_infection.wav",
             4:FLD_SND+"4_altered_reality.wav",5:FLD_SND+"5_mind_realm.wav",6:FLD_SND+"6_extinction.wav",
             7:FLD_SND+"7_impact.wav",8:FLD_SND+"8_eradication.wav"}

tapelist = [1,2,3,4,5,6,7,8]
random.shuffle(tapelist)

tapes_listened = 0

pygame.mixer.music.load(FLD_SND+"music.mp3")
pygame.mixer.music.play(-1)

tapequeue = []


dead = False          #Surnud
finished = False      #L6petatud

load_level(levellist[curlev],1)

#menyy
images_menu=[pygame.image.load(FLD_SPR+"menu.bmp"),pygame.image.load(FLD_SPR+"menu_controls.bmp")]
images_menu[0]=pygame.transform.scale(images_menu[0],(640,480))
images_menu[1]=pygame.transform.scale(images_menu[1],(640,480))

bgimage = pygame.image.load(FLD_SPR+"bg1.bmp")
bgimage = pygame.transform.scale(bgimage,(640,480))

bgimage2 = pygame.image.load(FLD_SPR+"bg2.bmp")
bgimage2 = pygame.transform.scale(bgimage2,(640,480))

menuimage=0
showmenu=True
running = True

while showmenu:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            showmenu = False
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                showmenu = False
            elif e.key == pygame.K_z:
                if menuimage==0:
                    menuimage = 1
                else:
                    menuimage = 0
    screen.blit(images_menu[menuimage], (0, 0))
    pygame.display.flip()
    

#P6hitsykkel
while running:

    clock.tick(60)
    cam.pos = cam.update()                  #Uuenda kaamerat
    if not dead and not finished:
        player.update()                             #Uuenda m2ngijat
    
    #Klahvi alla vajutamine
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
            if not dead and not finished:
                if e.key == pygame.K_SPACE:
                    if not hand==None and not draw_gui:
                        hand.shoot()
                if e.key == pygame.K_z:
                    if hand==None:
                        hand = Hand((0,0))
                        player.maxspeed = 1
                    else:
                        if not draw_gui and hand.image_speed==0:
                            hand = None
                            player.maxspeed = 2
                if e.key == pygame.K_x:
                    if ammo>0 and loadedammo<6 and draw_gui:
                        pygame.mixer.Channel(1).play(snd_load)
                        ammo -= 1
                        loadedammo += 1
                if e.key == pygame.K_v:
                    if not hand==None and hand.image_speed==0:
                        draw_gui = not draw_gui
                        if draw_gui:
                            pygame.mixer.Channel(1).play(snd_open)
                        else:
                            pygame.mixer.Channel(1).play(snd_close)
                
        if e.type == TAPE_END:
            if len(tapequeue)>0:
                tape = pygame.mixer.Sound(tapequeue[0])
                pygame.mixer.Channel(0).play(tape)
                print("playing audio "+tapequeue[0]+" from queue")
                print("removing audio from tapelist")
                tapequeue.remove(tapequeue[0])
                print(tapequeue)
            else:
                if len(tapelist)==0:
                    finished = True;
                print("tape playback ended")
            tapes_listened += 1
                
    #Klahvi all hoidmine

    key = pygame.key.get_pressed()
    if not dead and not finished:
        if key[pygame.K_LEFT]:
            player.speed = max(-player.maxspeed,-player.maxspeed-0.4)
        if key[pygame.K_RIGHT]:
            player.speed = min(player.maxspeed,player.maxspeed+0.4)
        if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
            player.image_speed = 3
        else:
            player.image_speed = 0
            player.image_index = 0
            if (player.speed>0):
                player.speed -= 0.2
            elif (player.speed<0):
                player.speed += 0.2
            player.speed=round(player.speed,1) #ymarda kuna 2-10*0.2 ei ole 0
        if key[pygame.K_UP]:
            player.jump()
            
    if key[pygame.K_SPACE]:
        if (dead):
            walls = []
            traps = []
            blockers = []
            exterminators = []
            exits = []
            loot = []
            bullets = []
            enemybullets = []
            non_solids = []
            hand = None
            explosion = None
            player = Player((32,32))
            curlev = 50;
            
            loottable = {0:[]}
            traptable = {0:[]}
            enemytable = {0:[]}
            
            
            levellist = []
            for i in range(100):
                levellist.append(random.randint(0,9))
            
            tapelist = [1,2,3,4,5]
            random.shuffle(tapelist)
            
            tapequeue = []
            tapes_listened = 0
            dead = False
            ammo = random.randint(3,7)
            loadedammo = random.randint(2,6)
            draw_gui=False
            
            load_level(levellist[curlev],1)
    
    if tapes_listened<6:
        screen.blit(bgimage, (0,0))
    else:
        screen.blit(bgimage2, (0,0))
    
    if (len(bullets)>0):
        for b in bullets:
            b.update()
            for e in exterminators:
                if e.rect.colliderect(b):
                    if sign(b.rect.x-e.rect.x)==e.image_xscale:
                        if e.hp>1:
                            e.hp -= 1
                        else:
                            exterminators.remove(e)
                    else:
                        exterminators.remove(e)
                    bullets.remove(b)
            screen.blit(b.image,cam.shift(b))
            
    for b in enemybullets:
        b.update()
        screen.blit(b.image,cam.shift(b))
    
    if not dead:     
        screen.blit(player.image,cam.shift(player))
    if not hand==None:
        hand.update()
        if draw_gui:
            if player.image_xscale==1:
                openimg=hand.openimage
            else:
                openimg=pygame.transform.flip(hand.openimage, 1, 0)
            screen.blit(openimg,cam.shift(hand))
        else:
            screen.blit(hand.image,cam.shift(hand))
    for wall in walls:
        screen.blit(wall.image,cam.shift(wall))
    for t in traps:
        screen.blit(t.image,cam.shift(t))
        if t.rect.colliderect(player) and not dead:
            explosion=PlayerExplode((player.rect.x-32,player.rect.y-32))
            dead = True
    for e in exits:
        screen.blit(e.image,cam.shift(e))
        if (e.rect.colliderect(player)):
            if not hand==None:
                if (player.image_xscale==-1):
                    hand.image = pygame.transform.flip(hand.image, 1, 0)
            for i in exterminators:
                table_add_entry(enemytable,i.name,i.rect.x,i.rect.y,i.image_xscale)
            walls = []
            traps = []
            blockers = []
            exterminators = []
            exits = []
            loot = []
            bullets = []
            enemybullets = []
            non_solids = []
            player = Player((0,-32))
            if not hand==None:
                player.maxspeed = 1
            curlev += e.s
            load_level(levellist[curlev],e.s)
            
    for ns in non_solids:
        screen.blit(ns.image,cam.shift(ns))
    for l in loot:
        screen.blit(l.image,cam.shift(l))
        if l.rect.colliderect(player):
            l.pickup()
    for e in exterminators:
        e.update()
        for b in blockers:
            if b.rect.colliderect(e):
                e.turn_around()
        if e.rect.colliderect(player) and not dead:
            explosion=PlayerExplode((player.rect.x-32,player.rect.y-32))
            dead = True
        screen.blit(e.image,cam.shift(e))
    
    if draw_gui:
        for i in range(ammo):
            screen.blit(hud_ammo_image,(110+32*i,6))
        screen.blit(cylinderimage[loadedammo],(6,6))
    
    if not explosion==None:
        screen.blit(explosion.image,cam.shift(explosion))
        explosion.update()
    if (dead):
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        background.set_alpha(160)
        screen.blit(background, (0, 0))
        screen.blit(restartimage,(86,380))
        
    pygame.display.flip()

