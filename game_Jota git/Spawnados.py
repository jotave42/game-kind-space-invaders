from PPlay.sprite import *
from PPlay.gameimage import *
class Balas():
    dano=0
    def __init__(self, caminho, pos_x, pos_y, forca,inimigo):
        self.textura=caminho
        self.tiro=Sprite(self.textura)
        self.pos_inc_y=pos_y-(self.tiro.height)
        if(inimigo==True):
             self.pos_inc_y=pos_y+(self.tiro.height)
        self.pos_inc_x=pos_x-(self.tiro.width/2)
        self.tiro.set_position(self.pos_inc_x,self.pos_inc_y)
        self.tiro.draw()
        self.dano= forca
        self.inimigo=inimigo
    def Mover(self,Vel):
        self.velociodade =Vel
        if(self.inimigo==True):
            self.velociodade=self.velociodade*-1
        self.pos_inc_y-=self.velociodade
        self.tiro.set_position(self.pos_inc_x,self.pos_inc_y)
class Fundos():
    def __init__(self, caminho):
        self.textura=caminho
        self.fundo=GameImage(self.textura)
        self.pos_inc_x=0
        self.pos_inc_y=-512
        self.fundo.set_position(self.pos_inc_x,self.pos_inc_x)
    def Comeco(self):
        self.pos_inc_y=0
        self.fundo.set_position(0,self.pos_inc_y)
    def Mover(self,vel):
            self.velociodade = vel
            self.pos_inc_y+=self.velociodade
            self.fundo.set_position(self.pos_inc_x,self.pos_inc_y)
class Inimigo():
    vida=0
    pos_x_inimigo=0
    pos_y_inimigo=0
    pos_x_nave=0
    pos_y_nave=0
    desce=False
    def __init__(self,inimigo_textura, inimigo_vida, pos_inc_x, pos_inc_y):
        self.textura=inimigo_textura
        self.vida=inimigo_vida
        self.inimigo=Sprite(self.textura)
        self.pos_y=pos_inc_y
        self.pos_x=pos_inc_x
        self.inimigo.set_position(self.pos_x,self.pos_y)
        self.inimigo.draw()
    def Receber_Dano(self, dano):
        self.dano_recebido=dano
        self.vida=self.vida-self.dano_recebido
    def Mover(self,vel):
            self.velociodade = vel
            if(self.desce==False):
                self.pos_x+=self.velociodade
                self.inimigo.set_position(self.pos_x,self.pos_y)
            else:
                self.pos_y+=self.velociodade
                self.pos_x=(((self.pos_y_nave-self.pos_y_inimigo)*self.pos_x_nave)+((self.pos_x_inimigo-self.pos_x_nave)*self.pos_y_nave)-((self.pos_x_inimigo-self.pos_x_nave)*self.pos_y))/(self.pos_y_nave-self.pos_y_inimigo)
                self.inimigo.set_position(self.pos_x,self.pos_y)

    def Inicia_Kamikaze(self,nave_x,nave_y):
        self.pos_x_nave=nave_x
        self.pos_y_nave=nave_y
        self.pos_x_inimigo=self.pos_x
        self.pos_y_inimigo=self.pos_y
        self.desce=True








