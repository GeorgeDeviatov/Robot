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
                print(agent,numstol,numstr)
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
    filename = input()#sys.argv[1]
    f = open(filename)
    m,n = parse_line(f)
    
    screen = pg.display.set_mode((800,600))
    
    flat = list()
    
    for i in range(m):
        flat.append(list(parse_line(f)))
    
    agents = []
    
    counag = int(f.readline()[:-1])
    for l in range(counag):
        x,y = parse_line(f)
        agents.append([x,y,False])
    
    view_flat = vx,vy = int(screen.get_width()*(2/3)) , int(screen.get_height()*(2/3))
    #Всякая Информация вне экрана
    
    #Текст
    col = 'red'
    tx = 'its off now'
    font = pg.font.SysFont('corbel',50)
    text= font.render(tx,True,THECOLORS[col])
    screen.blit(text,(vx+10,10))
    #Текст
    
    #Кнопка
    butcoor = [(vx+vx*0.2,vy*0.2),(vx+vx*0.2,vy*0.4),(vx+vx*0.4,vy*0.4),
                                                     (vx+vx*0.4,vy*0.2)]
    pg.draw.polygon(screen, THECOLORS['white'], butcoor)
    #Кнопка
    #Всякая Информация вне экрана
    
    cur = 0
    
    while True:
        #Рамка
        pg.draw.polygon(screen,THECOLORS["green"],[(0,0),(vx,0),(vx,vy),(0,vy)],2)
        
        #Отрисовка поля и агента
        draw(flat,screen.get_width()*(2/3)/n,screen.get_height()*(2/3)/m,agents)
        
        #Отрисовка текста
        text= font.render(str(tx),True,THECOLORS[col])
        screen.blit(text,(vx+vx*(1/10),10))
        
        #Если выключно то поменять цвет тескта и сам текст и наоборот
        if agents[cur][2]:
            colb = 'red'
            col = 'green'
            tx = 'its on now'
        else:
            colb = 'green'
            col = 'red'
            tx = 'its off now'
        pg.draw.polygon(screen, THECOLORS[colb], butcoor)
        
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                print(event.pos,butcoor)
                #Если игрок нажал на кнопку то выкл. или вкл.
                if event.pos[0] > butcoor[0][0] and event.pos[0] < butcoor[3][0]:
                    if event.pos[1] > butcoor[0][1] and event.pos[1] < butcoor[1][1]:
                        agents[cur][2] = not(agents[cur][2])
            if event.type == pg.KEYDOWN:
                try:
                    ent = int(pg.key.name(event.key))
                    if ent<=len(agents)-1:
                        cur = ent
                except:
                    _____ = 0
                if event.key == pg.K_SPACE:
                    if agents[cur][2] and flat[agents[cur][0]-1][agents[cur][1]-1] == 1:
                        flat[agents[cur][0]-1][agents[cur][1]-1] = 0
                if event.key == pg.K_g:
                    if agents[cur][2] and flat[agents[cur][0]-1][agents[cur][1]-1] == 0:
                        flat[agents[cur][0]-1][agents[cur][1]-1] = 1
                if event.key == pg.K_o:
                    agents[cur][2] = True
                if event.key == pg.K_f:
                    agents[cur][2] = False
                if agents[cur][2]:
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