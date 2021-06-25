from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import math

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from elements import screen_helper

from kivy.properties import ObjectProperty

#################
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
#################


class MainScreen(Screen):
    pass

class ResultScreen(Screen):
    expense_graph = ObjectProperty(None)
    def update_plot():
        plotShow = MDApp.get_running_app().root.get_screen('ResultScreen')
        plotShow.ids.expense_graph.clear_widgets()
        x = [1,2,3,4,5]
        plt.plot(x)
        plt.grid()
        plotShow.ids.expense_graph.add_widget(FigureCanvasKivyAgg(figure=plt.gcf()))

sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(ResultScreen(name='result'))


class GTDcalc(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        screen = Builder.load_string(screen_helper)
        return screen

    def gg(self):
        print("gg")

    def delplt(self):
        plotShow = MDApp.get_running_app().root.get_screen('result')
        plotShow.ids.expense_graph.clear_widgets()


    def update_plot(self):
        plt.clf()
        plotShow = MDApp.get_running_app().root.get_screen('result')
        plotShow.ids.expense_graph.clear_widgets()
        
        Mp = 1
        H = 300
        sigmaVH = -0.169714286*Mp+1.213523810
        if sigmaVH > 1:
            sigmaVH = 1
        Gpr = 26
        Pn = 97770.861
        Tn = 286.21
        an = 320
        k = 1.4
        Tg = 1600
        sigmaKS = 0.95
        kpdTK = 0.9
        kpdTTK = 0.99
        delta_ohl = 0.05
        m = 0.6
        kpdTV = 0.9
        kpdTTV = 0.99


        Vp = Mp*an
        lyambda = math.sqrt( (((k+1)/2)*Mp) / (1+((k-1)/2*Mp**2)))
        tau = 1-(k-1)/(k+1)*lyambda**2
        pi = math.pow(tau,k/(k-1))
        #
        #print(pi, "\t", tau, "\t", lyambda, "\t",sigmaVH)
        #
        #############################################################################
        #Bx

        Pvh = Pn*sigmaVH/pi
        Tvh = Tn/tau

        q = pow((k+1)/2,1/(k-1))*lyambda*pow(tau,1/(k-1))
        piV = 2.65*q+0.125
        kpdV = 0.5*q+0.5
        Pvn = Pvh*piV
        Tvn = Tvh*(1+(pow(piV,0.286)-1)/kpdV)
        #
        #print(Pvh, "\t", Tvh, "\t", q, "\t", piV, "\t", kpdV, "\t", Pvn, Tvn)
        #
        #############################################################################
        #K
        piK = 0.00285804*Gpr**2+0.038630653*Gpr+1.581155779
        kpdK = 0.000052083*Gpr**3-0.0028125*Gpr**2+0.057916667*Gpr+0.38
        Pk = Pvn*piK
        Tk = Tvn*(1+(pow(piK,0.286)-1)/kpdK)
        #
        #print(Pk, "\t", Tk, "\t", piK, "\t", kpdK)
        #
        #############################################################################
        #KC

        Pg = Pk*sigmaKS

        cpTg = 1.328571429*Tg-390
        cpTk = -0.0035*Tg**2+13.549999981*Tg-11449.99998261
        cpnTg = 5*Tg-2000
        cpnT0 = 455
        kpdG = 0.98
        Hu = 42900

        qT = (cpTg-cpTk)/(Hu*kpdG-cpnTg+cpnT0)
        #
        #print(qT)
        #
        #############################################################################
        #TK
        delta_otb = (1+qT)*delta_ohl/((1+qT)*delta_ohl+1)
        Xtk = 1-1005*(Tk-Tvn)/(1165*Tg*kpdTK*(1+qT)*(1-delta_otb)*kpdTTK)
        piTK = pow(Xtk,-1/(0.3))

        Ptk = Pg/piTK
        Ttk = Tg*(1-Xtk*kpdTK)
        #
        #print(Xtk, "\t",piTK, "\t",Ttk,"\t", Ptk, "\t")
        #
        #############################################################################
        #TB

        Xtv = 1-(1005*(2+m)*(Tvn-Tvh)/(1165*Ttk*kpdTV*(1+qT)*(1-delta_otb)*kpdTTV))
        piTV = pow(Xtv,-1/(0.3))
        Pt = Ptk/piTV
        Tt = Ttk*(1-Xtv*kpdTV)
        #
        #print(Xtv, "\t",piTV, "\t",Tt,"\t", Pt, "\t")
        #
        #############################################################################
        #vnytr kontyr
        kg = 1.33
        piLC1s = Pt*math.pow(1-(kg-1)/(kg+1)*1**2,kg/(kg-1))

        x=["Н", "B", "BH", "K", "Г", "TK", "T"]#, "C"]
        t=[Tn, Tvh, Tvn, Tk, Tg, Ttk, Tt]#, Tc]
        p=[Pn, Pvh, Pvn, Pk, Pg, Ptk, Pt]#, Pc]
        #plt.remove()
        plt.plot(x,p,x,t)
        plt.grid()
        plotShow.ids.expense_graph.add_widget(FigureCanvasKivyAgg(figure=plt.gcf()))


GTDcalc().run()
