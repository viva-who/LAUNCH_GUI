from CCoordinates import CXY,tCXY
from CDesignator import CDesignator
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from TkToolTip import ToolTip

# Класс отрисовки электронного модуля
class CModDraw():
    def __init__(self,ModName,c,):
        self.__ModName=ModName
        self.__c=c
        #
        self.__root = Tk()
        self.__root.title(self.__ModName)
        self.__root.geometry(self.__c.size(1.1))
        #
        self.__canvas = Canvas(bg="#53C351", width=c.width, height=c.height)
        self.__canvas.pack(anchor=CENTER, expand=1)
        #
        self.__root.bind('<Motion>', self.move)
        self.__xy_null=CXY()
        self.__mxy=CXY()
        ToolTip(self.__canvas, msg=self.getmsg)



    def set0plt(self,XY_null):
        self.__xy_null=self.__c.tr(XY_null) 
        

    def getmsg(self):
        return str(self.__mxy)
            

    def move(self,event):
            xy=CXY(event.x,event.y).norm(self.__xy_null)
            self.__mxy.set_x(xy.x/self.__c.scale)
            self.__mxy.set_y(-xy.y/self.__c.scale)


    def RootLoop(self):
        self.__root.mainloop()


    # Отрисовка фигуры с переводом координат
    def DrawFig(self,rzm,xy,Angle,el_fill,el_outline,fig='R'):
         # Рисуем компонент
        vl=self.__c.trvl(xy,rzm,Angle)
        np=self.__c.trnp(xy,rzm,Angle)
        match fig:
            case 'R':
                self.__canvas.create_rectangle(vl.x,vl.y,np.x,np.y, fill=el_fill, outline=el_outline)
            case 'O':
                self.__canvas.create_oval(vl.x,vl.y,np.x,np.y, fill=el_fill, outline=el_outline)
            
    # Печать текста на плате с переводом координат
    def DrawText(self,xy,ang,txt,txt_fill):
        angle_turn=self.__c.tr_angle(ang)
        dt=self.__c.tr(xy)
        textID = self.__canvas.create_text(dt.x,dt.y, angle=angle_turn, fill=txt_fill)
        self.__canvas.itemconfig(textID, text = txt)

    # Отрисовка электронного копонента
    def DzDraw(self,dz,rzm,nozzle=""):
        el_fill="#80CBC4"
        el_outline="#004D40"
        match dz.Des[0]:
            case 'R':
                el_fill="#485E5D"
                el_outline="#13453E"
            case 'C':
                el_fill="#757535"
                el_outline="#1B6872"
            case 'L':
                el_fill="#247CF7"
                el_outline="#0A373D"
            case 'D':
                el_fill="#214643"
                el_outline="#13636E"
            case 'V':
                match dz.Des[1]:
                    case 'T':
                        el_fill="#373798"
                        el_outline="#396336"
                        #print(rzm,dz.Angle)
                    case 'D':
                        el_fill="#6E2E1E"
                        el_outline="#3A7981"
        # Рисуем компонент
        self.DrawFig(rzm,dz.XY,dz.Angle,el_fill,el_outline)
        # Рисуем ключ
        self.DrawFig(CXY(.2,.2),dz.XY1p,dz.Angle,"#F17F7F","#02231D")
        # Рисуем отпечаток головки по координате установки
        d0=0.
        d1=0.
        match nozzle:
            case 'N502':
                d0=0.4     
                d1=0.7
            case 'N503':
                d0=0.6     
                d1=1.0
            case 'N504':
                d0=1.     
                d1=1.5
            case 'N505':
                d0=1.7     
                d1=3.5
            case 'N506':
                d0=3.2     
                d1=5.0
        self.DrawFig(CXY(d0/2.,d0/2.),dz.XY,dz.Angle,"","#000000",'O')        
        self.DrawFig(CXY(d0/2.+.1,d0/2.+.1),dz.XY,dz.Angle,"","#000000",'O')        
        self.DrawFig(CXY(d1/2.,d1/2.),dz.XY,dz.Angle,"","#000000",'O')        
        self.DrawFig(CXY(d1/2.-.1,d1/2.-.1),dz.XY,dz.Angle,"","#000000",'O')        
        # Печатаем дезигнатор   
        self.DrawText(dz.XY,dz.Angle,dz.Des,"#FDFDFD")  
               
    # Отрисовка репперного занака
    def RepDraw(self,dz_rep,rdz):
        # Рисуем внешний круг
        self.DrawFig(CXY(rdz,rdz),dz_rep.XY,dz_rep.Angle,"#69CFB0","#031210",'O')
        # Рисуем внутренний круг
        self.DrawFig(CXY(.5,.5),dz_rep.XY,dz_rep.Angle,"#C0E16E","#031210",'O')
        # Подписываем дезигнатор
        self.DrawText(dz_rep.XY,dz_rep.Angle,dz_rep.Des[3],"#0B0606")         
        
    # Отрисовка меток 2-х рабочих репперов ближнего и дальнего
    def RepFL(self,rzfr,rep0,rep1): 
        # Выводим репер с нулевыми координатами  
        self.DrawFig(rzfr,rep0.XY,rep0.Angle,"","#E1FC37",'O')
        # Выводим самый дальний репер
        self.DrawFig(rzfr,rep1.XY,rep1.Angle,"","#291FE7",'O')
         

    