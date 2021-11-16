import pygame as pg
import sys
from pygame.color import THECOLORS

def parse_line(f):
    k = f.readline()
    if k[len(k)-1] == '\n':
        return map(int,k[:-1].split())
    return map(int,k.split())

def draw(flat,sizex,sizey,agents):#Отрисовка поля
    numstr = 0
    numstol = 0
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
                    if agent[2]:
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
    f = open('flat.txt')
    m,n = parse_line(f)
    
    screen = pg.display.set_mode((800,600))
    
    flat = list()
    
    for i in range(m):
        flat.append(list(parse_line(f)))
    
    agents = []
    
    counag = int(f.readline()[:-1])
    cur = 0
    for l in range(counag):
        x,y = parse_line(f)
        agents.append([x,y,False])
    
    view_flat = vx,vy = int(screen.get_width()*(2/3)) , int(screen.get_height()*(2/3))
    #Всякая Информация вне экрана
    
    #Текст вкл./выкл.
    col = 'red'
    tx = 'its off now'
    font = pg.font.SysFont('corbel',50)
    text= font.render(tx,True,THECOLORS[col])
    screen.blit(text,(vx+10,10))
    #Текст кол-во агентов-роботов
    txc = len(agents)
    font2 = pg.font.SysFont('corbel',50)
    text2 = font.render(tx,True,THECOLORS['yellow'])
    screen.blit(text,(10,vy+10))
    #Текст текущий агент-робот
    fontcur = pg.font.SysFont('corbel',50)
    textcur = fontcur.render(str(cur),True,THECOLORS['purple'])
    screen.blit(textcur,(vx+50,vy+50))
    
    #Кнопка вкл./выкл.
    butcoor = [(vx+vx*0.2,vy*0.2),(vx+vx*0.2,vy*0.4),(vx+vx*0.4,vy*0.4),
                                                     (vx+vx*0.4,vy*0.2)]
    pg.draw.polygon(screen, THECOLORS['white'], butcoor)
    
    
    #Кнопка добавления агентов
    adbutcoor = [(10,vy+120),(10,vy+180),(70,vy+180),(70,vy+120)]
    pg.draw.polygon(screen,THECOLORS['orange'],adbutcoor)
    #Всякая Информация вне экрана
    
    
    while True:
        #Рамка
        pg.draw.polygon(screen,THECOLORS["green"],[(0,0),(vx,0),(vx,vy),(0,vy)],2)
        
        #Отрисовка поля и агента
        draw(flat,screen.get_width()*(2/3)/n,screen.get_height()*(2/3)/m,agents)
        
        #Отрисовка текста
        if len(agents)==0:
            tx = 'No agents'
            col = 'darkred'
        text= font.render(str(tx),True,THECOLORS[col])
        screen.blit(text,(vx+vx*(1/10),10))
            
        
        #Отрисовка кол-ва агентво-роботов-пылесосов
        txc = len(agents)
        text2= font2.render(str(txc),True,THECOLORS['yellow'])
        screen.blit(text2,(10,vy+10))
        
        #Отрисовка номера текущего робота
        textcur = fontcur.render(str(cur),True,THECOLORS['purple'])
        screen.blit(textcur,(vx+50,vy+50))
        
        #Если выключно то поменять цвет тескта и сам текст и наоборот
        if len(agents)>0 and agents[cur][2]:
            colb = 'red'
            col = 'green'
            tx = 'its on now'
        else:
            colb = 'green'
            col = 'red'
            tx = 'its off now'
        
        #Кнопки
        if len(agents)>0:
            pg.draw.polygon(screen, THECOLORS[colb], butcoor)
        
        
        pg.draw.polygon(screen,THECOLORS['orange'],adbutcoor)
        
        
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                #print(event.pos,butcoor)
                #Если игрок нажал на кнопку то выкл. или вкл.
                if event.pos[0] > butcoor[0][0] and event.pos[0] < butcoor[3][0]:
                    if event.pos[1] > butcoor[0][1] and event.pos[1] < butcoor[1][1] and len(agents)>0:
                        agents[cur][2] = not(agents[cur][2])
                 
                if event.pos[0] > adbutcoor[0][0] and event.pos[0] < adbutcoor[3][0]:
                    if event.pos[1] > adbutcoor[0][1] and event.pos[1] < adbutcoor[1][1] and len(agents)>0:
                        agents.append([1,1,False])
                        
                
            if event.type == pg.KEYDOWN:
                try:
                    ent = int(pg.key.name(event.key))
                    if ent<=len(agents)-1:
                        cur = ent
                except:
                    _____ = 0
                if event.key == pg.K_SPACE and len(agents)>0:
                    if agents[cur][2] and flat[agents[cur][0]-1][agents[cur][1]-1] == 1:
                        flat[agents[cur][0]-1][agents[cur][1]-1] = 0
                if event.key == pg.K_g and len(agents)>0:
                    if agents[cur][2] and flat[agents[cur][0]-1][agents[cur][1]-1] == 0:
                        flat[agents[cur][0]-1][agents[cur][1]-1] = 1
                if event.key == pg.K_o and len(agents)>0:
                    agents[cur][2] = True
                if event.key == pg.K_f and len(agents)>0:
                    agents[cur][2] = False
                if event.key == pg.K_k and len(agents) > 0:
                    agents.pop(cur)
                    cur = 0
                if len(agents)>0 and agents[cur][2]:
                    if event.key == pg.K_LEFT:
                        if agents[cur][1]>1:
                            agents[cur][1]-=1
                    if event.key == pg.K_RIGHT:
                        if agents[cur][1]<n:
                            agents[cur][1]+=1
                    if event.key == pg.K_UP:
                        
                        if agents[cur][0]>1:
                            agents[cur][0]-=1
                    if event.key == pg.K_DOWN:
                        
                        if agents[cur][0]<m:
                            agents[cur][0]+=1
        screen.fill((0,0,0))