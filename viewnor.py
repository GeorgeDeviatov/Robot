import pygame as pg
import sys
from pygame.color import THECOLORS
import random

class Environment:
    def __init__(self,m,n,objects=[]):
        self.m=m
        self.n=n
        self.env=[]
        self.objects = objects
        for i in range(m):
            new = []
            for t in range(n):
                new.append(random.randint(0,1))
            self.env.append(new)
    
    def add_robot(self,robot,x=1,y=1):
        self.objects.append(robot)
        self.objects.append([x,y])
    
    
    def up(self,player):
        if self.objects[player.cur*2+1][0]>=2:
            self.objects[player.cur*2+1][0]-=1
    
    def down(self,player):
        if self.objects[player.cur*2+1][0]<self.m:
            self.objects[player.cur*2+1][0]+=1
    
    def left(self,player):
        if self.objects[player.cur*2+1][1]>=2:
            self.objects[player.cur*2+1][1]-=1
    
    def right(self,player):
        if self.objects[player.cur*2+1][1]<self.n:
            self.objects[player.cur*2+1][1]+=1
    
    def clear(self,player):
        if self.env[self.objects[player.cur*2+1][0]-1][self.objects[player.cur*2+1][1]-1] == 0:
            self.env[self.objects[player.cur*2+1][0]-1][self.objects[player.cur*2+1][1]-1] = 1
    
    def check(self,player,event):
        player.check(event,self)

class Player:
    def __init__(self,cur=0):
        self.cur = cur
    def check(self,eevent,env):
        if event.key == pg.K_LEFT:
            env.left(self)
        if event.key == pg.K_RIGHT:
            env.right(self)
        if event.key == pg.K_UP:     
            env.up(self)
        if event.key == pg.K_DOWN:
            env.down(self)
        if event.key == pg.K_SPACE:
            env.clear(self)

class Robot:
    def __init__(self,ison=False):
        self.ison = ison

def parse_line(f):
    k = f.readline()
    if k[len(k)-1] == '\n':
        return map(int,k[:-1].split())
    return map(int,k.split())

def draw(flat,sizex,sizey,agents,env,player):#Отрисовка поля
    numstr = 0
    numstol = 0
    print(agents)
    for n in flat:
        numstr += 1
        numstol = 0
        for i in n:
            numstol +=1
            col = THECOLORS["blue"]
            if i==0:
                col = THECOLORS["red"]
            pg.draw.polygon(screen,col,[(sizex*(numstol-1),sizey*(numstr-1)),
                                        (sizex*(numstol-1),sizey*numstr),(sizex*numstol,sizey*numstr)
                                        ,(sizex*numstol,sizey*(numstr-1))])
            #Игрок
            for agent in agents:
                #print(agent,numstol,numstr)
                if numstol==agent[1] and numstr==agent[0]:
                    if env.objects[player.cur].ison:
                        colo = 'green'
                    else:
                        colo = 'red'
                    cent = (sizex*(numstol-1)+(sizex/2),sizey*(numstr-1)+(sizey/2))
                    pg.draw.circle(screen,THECOLORS["yellow"],cent,min(sizex/2,sizey/2))
                    pg.draw.circle(screen,THECOLORS[colo],cent,min(sizex/10,sizey/10))
                


if __name__ == "__main__":
    #Загрузка информации из файла
    pg.init()
    #filename = input()#sys.argv[1]
    
    screen = pg.display.set_mode((800,600))
    '''
    flat = list()
    
    for i in range(m):
        flat.append(list(parse_line(f)))
    '''
    
    rob = Robot(False)
    env = Environment(4,5,[rob,[2,2]])
    countofrob = len(env.objects)//2
    ag = [env.objects[i] for i in range(1,len(env.objects),2)]
    player = Player(0)
    
    view_flat = vx,vy = int(screen.get_width()*(2/3)) , int(screen.get_height()*(2/3))
    #Всякая Информация вне экрана
    
    #Текст вкл./выкл.
    col = 'red'
    tx = 'its off now'
    font = pg.font.SysFont('corbel',50)
    text= font.render(tx,True,THECOLORS[col])
    screen.blit(text,(vx+10,10))
    #Текст кол-во агентов-роботов
    txc = countofrob
    font2 = pg.font.SysFont('corbel',50)
    text2 = font.render(tx,True,THECOLORS['yellow'])
    screen.blit(text,(10,vy+10))
    #Текст текущий агент-робот
    fontcur = pg.font.SysFont('corbel',50)
    textcur = fontcur.render(str(player.cur),True,THECOLORS['purple'])
    screen.blit(textcur,(vx+50,vy+50))
    
    #Отрисвка введёного числа во время ввода номера робота
    num = ""
    fontsee = pg.font.SysFont('corbel',50)
    textsee = fontsee.render(num,True,THECOLORS['white'])
    screen.blit(textsee,(200,vy+150))
    
    #Кнопка вкл./выкл.
    butcoor = [(vx+vx*0.2,vy*0.2),(vx+vx*0.2,vy*0.4),(vx+vx*0.4,vy*0.4),
                                                     (vx+vx*0.4,vy*0.2)]
    pg.draw.polygon(screen, THECOLORS['white'], butcoor)
    
    
    #Кнопка добавления агентов
    adbutcoor = [(10,vy+120),(10,vy+180),(70,vy+180),(70,vy+120)]
    pg.draw.polygon(screen,THECOLORS['orange'],adbutcoor)
    
    #Кнопка выбора текущего агента-робота-пылесоса
    colforchoose = 'darkblue'
    counbutcoor = [(110,vy+120),(110,vy+180),(170,vy+180),(170,vy+120)]
    pg.draw.polygon(screen,colforchoose,counbutcoor)
    
    
    
    
    nowof = True
    was = nowof
    
    #Всякая Информация вне экрана
    
    
    while True:
        #print(env.objects)
        ag = [env.objects[i] for i in range(1,len(env.objects),2)]
        #Рамка
        pg.draw.polygon(screen,THECOLORS["green"],[(0,0),(vx,0),(vx,vy),(0,vy)],2)
        
        #Отрисовка поля и агента
        draw(env.env,screen.get_width()*(2/3)/env.n,screen.get_height()*(2/3)/env.m,ag,env,player)
        
        #Отрисовка текста
        if countofrob==0:
            tx = 'No agents'
            col = 'darkred'
        text= font.render(str(tx),True,THECOLORS[col])
        screen.blit(text,(vx+vx*(1/10),10))
            
        
        #Отрисовка кол-ва агентво-роботов-пылесосов
        txc = countofrob
        text2= font2.render(str(txc),True,THECOLORS['yellow'])
        screen.blit(text2,(10,vy+10))
        
        #Отрисовка номера текущего робота
        textcur = fontcur.render(str(player.cur),True,THECOLORS['purple'])
        screen.blit(textcur,(vx+50,vy+50))
        
        #Отрисвка введёного числа во время ввода номера робота
        if not(nowof) and was:
            textsee = fontsee.render(str(num),True,THECOLORS['white'])
            screen.blit(textsee,(200,vy+150))
        
        
        #Если выключно то поменять цвет тескта и сам текст и наоборот
        if countofrob>0 and env.objects[0].ison:
            colb = 'red'
            col = 'green'
            tx = 'its on now'
        else:
            colb = 'green'
            col = 'red'
            tx = 'its off now'
        
        #Кнопки
        if countofrob>0:
            pg.draw.polygon(screen, THECOLORS[colb], butcoor)
        
        
        pg.draw.polygon(screen,THECOLORS['orange'],adbutcoor)
        
        
        #Кнопка выбора текущего агента-робота-пылесоса
        if nowof:
            colforchoose = 'darkblue'
        else:
            colforchoose = 'blue'
        counbutcoor = [(110,vy+120),(110,vy+180),(170,vy+180),(170,vy+120)]
        pg.draw.polygon(screen,colforchoose,counbutcoor)
        
        
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:#Куча кнопок
                #print(event.pos,butcoor)
                #Если игрок нажал на кнопку то выкл. или вкл.
                if event.pos[0] > butcoor[0][0] and event.pos[0] < butcoor[3][0]:
                    if event.pos[1] > butcoor[0][1] and event.pos[1] < butcoor[1][1] and countofrob>0:
                        env.objects[player.cur].ison = not(env.objects[player.cur].ison)
                 
                if event.pos[0] > adbutcoor[0][0] and event.pos[0] < adbutcoor[3][0]:
                    if event.pos[1] > adbutcoor[0][1] and event.pos[1] < adbutcoor[1][1]:
                        
                        newr = Robot(False)
                        env.add_robot(newr,1,1)
                        
                if event.pos[0] > counbutcoor[0][0] and event.pos[0] < counbutcoor[3][0]:
                    if event.pos[1] > counbutcoor[0][1] and event.pos[1] < counbutcoor[1][1] and countofrob>0:
                        
                        
                        was = nowof
                        nowof = not(nowof)
                        if nowof and not(was):
                            try:
                                num = int(num)
                                if num<countofrob:
                                    player.cur = num
                                num = ''
                            except:
                                print("NO")
                                num = ''
                        
                
            if event.type == pg.KEYDOWN:
                env.check(player,event)

                if not(nowof):
                    num+=(pg.key.name(event.key))
                    try:
                        num = int(num)
                        if not(num<countofrob): 
                            nowof = not(nowof)
                            num = ''
                        else:
                            num=str(num)
                    except:
                        nowof = not(nowof)
                        num = ''
                    '''
            
                if event.key == pg.K_o and len(agents)>0:
                    agents[cur][2] = True
                if event.key == pg.K_f and len(agents)>0:
                    agents[cur][2] = False
                if event.key == pg.K_k and len(agents) > 0:
                    agents.pop(cur)
                    cur = 0
                if event.key == pg.K_w:
                    cur+=1
                    if cur>=len(agents):
                        cur = 0
                if event.key == pg.K_s:
                    cur-=1
                    if cur<0:
                        cur = len(agents)
                        cur-=1
                '''

        screen.fill((0,0,0))