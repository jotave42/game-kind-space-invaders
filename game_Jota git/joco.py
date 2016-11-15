'''The MIT License (MIT)

Copyright (c) 2016 João Victor Da Costa Melo

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from PPlay.window import *
from PPlay.keyboard import *
from PPlay.gameimage import *
from PPlay.sprite   import *
from PPlay.collision import *
from PPlay.sound import *
from Spawnados import *
import time
import random



ALT_FUNDO=512
LARG_FUNDO=512

pos_img_x=0
pos_img_y=0

musica = Sound("musica.ogg")
som_tiro = Sound("tiro.ogg")
som_gameover= Sound("gameover.ogg")

Vel=150
vel_tiro=1.5
vel_fundo=0.7
vel_inimigo=0.5
vel_kamikaze=1.7
delta_T=0

i_atual=0
i_mudado=0
razao=-1

tempo_animacao=600

tempo_inicial_total=0
tempo_final_total=0

minutos=0
segundos=0

tempo_atual_tiro_inimigo=0
tempo_antigo_tiro_inimigo=0

tempo_atual_tiro=0
tempo_antigo_tiro=0

tempo_atual_kamikaze=0
tempo_antigo_kamikaze=0

intervalo_kamikaze=5
intervalo_tiro_inimigos=400
intervalo_tiro=300

tiros = []
tiros_inimigos= []
fundos = []
mat_inimigos = []
kamikazes=[]
mortos=[]
razeos=[]



janela = Window(ALT_FUNDO,LARG_FUNDO)
janela.set_title("Joco")
janela.set_background_color((0,0,0))

teclado = Keyboard()

fundo_temp = Fundos("starfiel.gif")
fundo_temp.Comeco()
fundo_temp.fundo.draw()
fundos.append(fundo_temp)

nave = Sprite("nave.png")
ALT_NAVE = nave.height
LARG_NAVE= nave.width
pos_img_x=(ALT_FUNDO/2)-LARG_NAVE/2
pos_img_y=(LARG_FUNDO/2)-ALT_NAVE/2
nave.set_position(pos_img_x,pos_img_y)
nave.draw()

vida_nave=100
pontos=0
gameover=False
inimigo_base = Sprite("inimigo.png")
#FUNÇÕES

def cria_inimigos(n_linhas,n_colunas,mat_inimigos,razeos):
    pos_inimigo_x=0
    pos_inimigo_y=50
    espaco=20
    for i in range(0,n_linhas):
        linha=[]
        for j in range(0, n_colunas):
            if(j!=0):
                pos_inimigo_x+=inimigo_base.width+espaco
            else:
                if(i%2==0)or(i==0):
                    pos_inimigo_x=0
                else:
                    pos_inimigo_x=inimigo_base.width
            inimigo = Inimigo("inimigo.png",100,pos_inimigo_x,pos_inimigo_y)
            linha.append(inimigo)
        pos_inimigo_y+=inimigo_base.height+espaco
        mat_inimigos.append(linha)
        if(i%2==0):
            razeos.append(1)
        else:
            razeos.append(-1)
def sortear_atirador(mat_inimigos,tiros_inimigos):
    linhas_totais=len(mat_inimigos)-1
    if(linhas_totais>=0):
        linha_sorteada=random.randint(0,linhas_totais)
        coluna=mat_inimigos[linha_sorteada]
        colunas_totais=len(coluna)-1
        if(colunas_totais>=0):
            coluna_sorteada=random.randint(0,colunas_totais)
            sorteado=coluna[coluna_sorteada]
            pos_x_tiro= sorteado.inimigo.x
            pos_y_tiro= sorteado.inimigo.y
            tiro_temp_inimigo=Balas("tiro4.png",pos_x_tiro+sorteado.inimigo.width/2,pos_y_tiro,10,True)
            tiros_inimigos.append(tiro_temp_inimigo)




def sortear_kamikaze(mat_inimigos,kamikazes):
    linhas=len(mat_inimigos)-1
    if(linhas>=0):
        linha_sorteada=random.randint(0,linhas)
        coluna=mat_inimigos[linha_sorteada]
        colunas=len(coluna)-1
        if(colunas>=0):
            coluna_sorteada=random.randint(0,colunas)
            linha_selecionada=mat_inimigos[linha_sorteada]
            linha_selecionada[coluna_sorteada].Inicia_Kamikaze(nave.x+(LARG_NAVE/2),nave.y+(ALT_NAVE/2))
            #linha_selecionada[coluna_sorteada].Inicia_Kamikaze(nave.x,nave.y)
            kamikazes.append(mat_inimigos[linha_sorteada][coluna_sorteada])
            mat_inimigos[linha_sorteada].remove(mat_inimigos[linha_sorteada][coluna_sorteada])

def incremeta_temp_antigo(tempo_antigo_tiro,tempo_atual_tiro):
    tempo_antigo_tiro= int(round(time.time()*1000))
    tempo_atual_tiro = int(round(time.time()*1000))
    return tempo_antigo_tiro,tempo_atual_tiro

def entrada(x,y,razao,vida_nave,pontuacao,temp_animacao,tiros,tempo_antigo_tiro,tempo_atual_tiro,razeos):#funções sempre antes
    Antigo_X=x
    Antigo_Y=y
    delta_T= janela.delta_time() #frames por secundo iguala processamento
    vel_temp=delta_T*Vel
    if(teclado.key_pressed("ESC")):
        janela.close()
    if(teclado.key_pressed("LEFT")):
        x-= vel_temp
    if(teclado.key_pressed("RIGHT")):
        x+= vel_temp
    if(teclado.key_pressed("UP")):
        y-= vel_temp
    if(teclado.key_pressed("DOWN")):
        y+= vel_temp
    if((x<=0)or(x>LARG_FUNDO-(LARG_NAVE))):
        x=Antigo_X
    if((y<=0)or(y>=ALT_FUNDO-ALT_NAVE)):
        y=Antigo_Y
    if(teclado.key_pressed("SPACE")):
        if(((tempo_atual_tiro==0)and(tempo_antigo_tiro==0))or(abs(tempo_atual_tiro-tempo_antigo_tiro)>=intervalo_tiro)):
            tempo_antigo_tiro,tempo_atual_tiro=incremeta_temp_antigo(tempo_antigo_tiro,tempo_atual_tiro)
            tiro_temp= Balas("tiro3.png",x+LARG_NAVE/2,y,50,False)
            tiros.append(tiro_temp)
    if(len(tiros)>0):
        for i in tiros:
            i.Mover(vel_temp*vel_tiro)
            if(len(mat_inimigos)>0):
                for k in mat_inimigos:
                    for j in k:
                        if(Collision.perfect_collision(j.inimigo,i.tiro)==True):
                            j.Receber_Dano(i.dano)
                            pontuacao+=5
                            tiros.remove(i)
                            if(j.vida<=0):
                                posx=j.inimigo.x
                                posy=j.inimigo.y
                                j.inimigo=Sprite("explocao.png",16)
                                j.inimigo.set_position(posx,posy)
                                j.inimigo.set_sequence(0,16,False)
                                j.inimigo.set_total_duration(temp_animacao)
                                mortos.append(j)
                                k.remove(j)
            if(len(kamikazes)>0):
                for j in kamikazes:
                     if(Collision.perfect_collision(j.inimigo,i.tiro)==True):
                            j.Receber_Dano(i.dano)
                            tiros.remove(i)
                            pontuacao+=15
                            if(j.vida<=0):
                                posx=j.inimigo.x
                                posy=j.inimigo.y
                                j.inimigo=Sprite("explocao.png",16)
                                j.inimigo.set_position(posx,posy)
                                j.inimigo.set_sequence(0,16,False)
                                j.inimigo.set_total_duration(temp_animacao)
                                mortos.append(j)
                                kamikazes.remove(j)
            if(i.pos_inc_y<0):
                tiros.remove(i)

    if(len(fundos)>0):
        for i in fundos:
            i.Mover(vel_temp*vel_fundo)
            if(i.pos_inc_y>512):
                fundos.remove(i)
    if(len(mat_inimigos)>0):
        index=0
        for i in mat_inimigos:
            tam=len(i)
            if(tam!=0):
                if(((i[0].pos_x<0)or(i[tam-1].pos_x>LARG_FUNDO-inimigo_base.width))and(len(mat_inimigos)>0)):
                    razeos[index]=razeos[index]*-1
                    #razao=razao*-1
                    if(i[0].pos_x<0):
                        i[0].pos_x=0
                    if(i[tam-1].pos_x>LARG_FUNDO-inimigo_base.width):
                        i[tam-1].pos_x=LARG_FUNDO-inimigo_base.width
                for j in i:
                        j.Mover((delta_T*100)* razeos[index]*vel_inimigo)
                         #j.Mover((delta_T*100)* razao*vel_inimigo)
            index+=1

    if(len(kamikazes)>0):
        for i in kamikazes:
            i.Mover((delta_T*100)*vel_kamikaze)
            if(Collision.perfect_collision(i.inimigo,nave)==True):
                vida_nave=0
                pontuacao=100#pois intendo que ele desviou
                kamikazes.remove(i)
            if(i.inimigo.y>512):
                pontuacao+=2#pois intendo que ele desviou
                kamikazes.remove(i)

    if(len(tiros_inimigos)>0):
        for i in tiros_inimigos:
            i.Mover(vel_temp*vel_tiro)
            if(Collision.perfect_collision(i.tiro,nave)==True):
                vida_nave-=i.dano
                pontuacao-=3
                tiros_inimigos.remove(i)
            elif(i.tiro.y>512):
                tiros_inimigos.remove(i)

    return x,y,razao,vida_nave,pontuacao,tiros,tempo_antigo_tiro,tempo_atual_tiro,razeos

def Desenha(pontos,minutos,segundos):
    janela.set_background_color((0,0,0))
    if(len(fundos)>0):
        for i in fundos:
            i.fundo.draw()
    if(vida_nave>0):
        nave.draw()
    elif(gameover):
        nave.update()
        nave.draw()
    if(len(tiros)>0):
        for i in tiros:
            i.tiro.draw()
    if(len(mat_inimigos)>0):
        index=0
        for i in mat_inimigos:
            if(len(i)>0):
                for j in i:
                    j.inimigo.draw()
            else:
                mat_inimigos.remove(i)
                razeos.pop(index)
            index+=1
    if(len(kamikazes)>0):
        for i in kamikazes:
            i.inimigo.draw()
    if(len(tiros_inimigos)>0):
        for i in tiros_inimigos:
          i.tiro.draw()
    if(len(mortos)):
        for i in mortos:
            if(i.inimigo.playing):
                i.inimigo.update()
                i.inimigo.draw()
            else:
                mortos.remove(i)
    janela.draw_text("Pontos: "+str(pontos),0,0,25,(255,255,255),"Arial",True)
    janela.draw_text("Tempo: "+str(minutos)+":"+str(segundos),350,0,25,(255,255,255),"Arial",True)
    if(gameover):
        janela.draw_text("GAME-OVER",(LARG_FUNDO/7)+5,(ALT_FUNDO/3)+5,75,(255,255,0),"Arial",True)
        janela.draw_text("GAME-OVER",LARG_FUNDO/7,ALT_FUNDO/3,75,(255,0,0),"Arial",True)

def Reiniciar(tiros,tiros_inimigos,kamikazes,mat_inimigos,pontos,segundos_totais,vida_nave,tempo_final_total,tempo_inicial_total,gameover,nave):
    if(len(tiros)>0):
        for i in tiros:
            tiros.remove(i)
    if(len(tiros_inimigos)>0):
        for i in tiros_inimigos:
            tiros_inimigos.remove(i)
    if(len(kamikazes)>0):
        for i in kamikazes:
            kamikazes.remove(i)
    while(len(mat_inimigos)>0):
        for i in mat_inimigos:
            for j in i:
                i.remove(j)
            if(len(i)<=0):
                mat_inimigos.remove(i)

    pontos=0
    segundos_totais=0
    vida_nave=100
    tempo_final_total=0
    tempo_inicial_total=0
    gameover=False
    nave=Sprite("nave.png")
    nave.set_position(((ALT_FUNDO/2)-LARG_NAVE/2),((LARG_FUNDO/2)-ALT_NAVE/2))
    return pontos,segundos_totais,vida_nave,tempo_final_total,tempo_inicial_total,gameover,nave


while(True):
    if(vida_nave>0):
        if(not musica.is_playing()):
            musica.set_volume(100)
            musica.play()
        if(len(mat_inimigos)==0):
            cria_inimigos(2,8,mat_inimigos,razeos)
        if(len(fundos)==1):
            fundo_temp = Fundos("starfiel.gif")
            fundos.append(fundo_temp)

        if((tempo_inicial_total==0)and(tempo_final_total==0)):
            tempo_inicial_total=int(time.time())
            tempo_final_total=int(time.time())
        else:
            tempo_final_total=int(time.time())

        if((tempo_atual_kamikaze==0)and(tempo_antigo_kamikaze==0)):
            tempo_antigo_kamikaze=int(time.time())
            tempo_atual_kamikaze=int(time.time())
        if(abs(tempo_atual_kamikaze-tempo_antigo_kamikaze)>intervalo_kamikaze):
            tempo_antigo_kamikaze=tempo_atual_kamikaze
            sortear_kamikaze(mat_inimigos,kamikazes)
        else:
            tempo_atual_kamikaze=int(time.time())

        if((tempo_atual_tiro_inimigo==0)and(tempo_antigo_tiro_inimigo==0)):
            tempo_antigo_tiro_inimigo=int(round(time.time()*1000))
            tempo_atual_tiro_inimigo=int(round(time.time()*1000))
        if(abs(tempo_atual_tiro_inimigo-tempo_antigo_tiro_inimigo)>intervalo_tiro_inimigos):
            tempo_antigo_tiro_inimigo=tempo_atual_tiro_inimigo
            sortear_atirador(mat_inimigos,tiros_inimigos)
        else:
            tempo_atual_tiro_inimigo=int(round(time.time()*1000))

        if(abs(tempo_atual_tiro-tempo_antigo_tiro)<intervalo_tiro):
            tempo_atual_tiro = int(round(time.time()*1000))

        pos_img_x,pos_img_y,razao,vida_nave,pontos,tiros,tempo_antigo_tiro,tempo_atual_tiro,razeos = entrada(pos_img_x,pos_img_y,razao,vida_nave,pontos,tempo_animacao,tiros,tempo_antigo_tiro,tempo_atual_tiro,razeos)
        nave.set_position(pos_img_x,pos_img_y)

        segundos_totais=tempo_final_total-tempo_inicial_total
        minutos=segundos_totais//60
        segundos=segundos_totais%60
    else:
        if(gameover==False):
            nave=Sprite("explocao.png",16)
            nave.set_position(pos_img_x,pos_img_y)
            nave.set_sequence(0,16,False)
            nave.set_total_duration(tempo_animacao)
            pontos+=segundos_totais
            if(musica.is_playing()):
                    musica.stop()
            if(not som_gameover.is_playing()):
                som_gameover.set_volume(100)
                som_gameover.play()
            gameover=True
        if(teclado.key_pressed("ESC")):
            janela.close()
        if(teclado.key_pressed("ENTER")):
            pontos,segundos_totais,vida_nave,tempo_final_total,tempo_inicial_total,gameover,nave=Reiniciar(tiros,tiros_inimigos,kamikazes,mat_inimigos,pontos,segundos_totais,vida_nave,tempo_final_total,tempo_inicial_total,gameover,nave)

    Desenha(pontos,minutos,segundos)
    janela.update()

