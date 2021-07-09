from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import math
import matplotlib.pyplot as plt

from kivy.lang import Builder






class MyApp(App):

    def frin(self):
        self.gg=[]
        self.ARR = ["H","Gпр","М","Тг"," "," "]
        self.AL = AnchorLayout()
        self.BOX = BoxLayout(orientation="vertical", padding = 10)
        for i in self.ARR:
            box1 = BoxLayout(orientation="horizontal")
            self.lbl1 = Label(text=i, halign="right", valign="center", size_hint=[0.3, 0.5])
            self.inp1 = TextInput(size_hint=[1, 0.5], multiline=False)
            box1.add_widget(self.lbl1)
            if i == " ":
                pass
            else:
                box1.add_widget(self.inp1)
                self.gg.append(self.inp1)
            self.BOX.add_widget(box1)



        self.btn = Button(text="РАСЧЁТ", on_press = self.set_srin,background_color = (0.2,1,0,1))
        self.BOX.add_widget(self.btn)




    def srin(self):
        plt.clf()
        Mp = float(self.gg[2].text) #1
        H = float(self.gg[0].text) #300
        sigmaVH = -0.169714286*Mp+1.213523810
        if sigmaVH > 1:
            sigmaVH = 1
        Gpr = float(self.gg[1].text) #26
        Pn = 0.0005517*H**2-11.9457454*H+101281.8063251
        Tn = -0.00000000672*H**2-0.00646850169*H+288.14306710633
        an = 0.00000002227*H**2-0.00382688981*H+340.28507315515
        k = 1.4
        kg = 1.33
        Tg = float(self.gg[3].text)
        sigmaKS = 0.95
        kpdTK = 0.9
        kpdTTK = 0.99
        delta_ohl = 0.05
        m = 0.6
        kpdTV = 0.9
        kpdTTV = 0.99
        Vp = Mp*an
        lyambda = math.sqrt( ( ((k+1)/2)*Mp**2 ) / (1+(((k-1)/2)*Mp**2)) )
        tau = 1-(k-1)/(k+1)*lyambda**2
        pi = math.pow(tau,k/(k-1))
        Pvh = Pn*sigmaVH/pi
        Tvh = Tn/tau
        q = pow((k+1)/2,1/(k-1))*lyambda*pow(tau,1/(k-1))
        piV = 2.65*q+0.125
        kpdV = 0.5*q+0.5
        Pvn = Pvh*piV
        Tvn = Tvh*(1+(pow(piV,0.286)-1)/kpdV)
        piK = 0.00285804*Gpr**2+0.038630653*Gpr+1.581155779
        kpdK = 0.000052083*Gpr**3-0.0028125*Gpr**2+0.057916667*Gpr+0.38
        Pk = Pvn*piK
        Tk = Tvn*(1+(pow(piK,0.286)-1)/kpdK)
        Pg = Pk*sigmaKS
        cpTg = 1.328571429*Tg-390
        cpTk = -0.0035*Tg**2+13.549999981*Tg-11449.99998261
        cpnTg = 5*Tg-2000
        cpnT0 = 455
        kpdG = 0.98
        Hu = 42900
        qT = (cpTg-cpTk)/(Hu*kpdG-cpnTg+cpnT0)
        delta_otb = (1+qT)*delta_ohl/((1+qT)*delta_ohl+1)
        Xtk = 1005*(Tk-Tvn)/(1165*Tg*kpdTK*(1+qT)*(1-delta_otb)*kpdTTK)
        piTK = pow(1-Xtk,-kg/(kg-1))
        Ptk = Pg/piTK
        Ttk = Tg*(1-Xtk*kpdTK)
        Xtv = (1005*(1+m)*(Tvn-Tvh)/(1165*Ttk*kpdTV*(1+qT)*(1-delta_otb)*kpdTTV))
        piTV = pow(1-Xtv,-kg/(kg-1))
        Pt = Ptk/piTV
        Tt = Ttk*(1-Xtv*kpdTV)
        lyambda_c1s = 1
        pi_c1s = math.pow(1-(kg-1)*lyambda_c1s**2,kg/(kg-1))
        P1cs = Pt*pi_c1s
        lyambda_c1 = 0.97
        pi_c1 = math.pow(1-(kg-1)*lyambda_c1**2,kg/(kg-1))
        P1c = P1cs/pi_c1
        Tc = Tt*(1+m*Tvn/Tt)/(1+m)
        Pc = (Pvn+P1c)/2

        self.x=["Н", "B", "BH", "K", "Г", "TK", "T", "C"]
        self.t=[Tn, Tvh, Tvn, Tk, Tg, Ttk, Tt, Tc]
        p=[Pn, Pvh, Pvn, Pk, Pg, Ptk, Pt, Pc]
        plt.plot(self.x,p)
        plt.grid()
        plot = FigureCanvasKivyAgg(plt.gcf())
        self.boX = BoxLayout(orientation="vertical")
        self.boX.add_widget(plot)
        self.back = Button(text="Далее",size_hint=[1, 0.2],  on_press = self.set_thrin,background_color = (0.2,1,0,1))
        self.boX.add_widget(self.back)
        self.AL.add_widget(self.boX)
        return x, t

    def thrin(self):
            self.AL.remove_widget(self.boX)
            plt.clf()
            plt.plot(self.x,self.t)
            plt.grid()
            self.plot2 = FigureCanvasKivyAgg(plt.gcf())
            self.bOX = BoxLayout(orientation="vertical")
            self.bOX.add_widget(self.plot2)
            self.back2 = Button(text="В начало",size_hint=[1, 0.2],  on_press = self.set_back,background_color = (0.2,1,0,1))
            self.bOX.add_widget(self.back2)
            self.AL.add_widget(self.bOX)


    def build(self):
        self.frin()
        self.AL.add_widget(self.BOX)
        return self.AL

    def set_srin(self, instance):
        try:
            for i in range(len(self.gg)):
                float(self.gg[i].text)

            self.AL.remove_widget(self.BOX)
            self.srin()
        except:
            self.btn.text = "ERROR!"

    def set_back(self, instance):
        try:
            self.AL.remove_widget(self.bOX)
            self.AL.remove_widget(self.boX)
            self.btn.text = "РАСЧЁТ"
            self.AL.add_widget(self.BOX)
        except:
            print("error")
            self.btn.text = "ERROR!"

    def set_thrin(self, instance):
        try:
            self.AL.remove_widget(self.boX)
            self.thrin()
        except:
            print("error")
            self.btn.text = "ERROR!"


MyApp().run()
