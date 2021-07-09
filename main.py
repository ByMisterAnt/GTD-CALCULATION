from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from math import sqrt

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.properties import ObjectProperty

screens = """
ScreenManager:
    MainScreen:
    ResultScreen:

<MainScreen>:
    adaptive_height: True
    name: 'main'
    MDCard:
        id: 'card'
        size_hint: None, None
        size: 200, 450
        pos_hint: {'center_x':0.5,'center_y':0.5}
        elevation: 10
        padding: 15
        spacing: 25
        orientation: 'vertical'

        MDLabel:
            text: 'Введите исходные данные'
            halign: 'center'
            font_size: 18
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]

        MDTextFieldRound:
            id: H
            hint_text: 'H'
            size_hint_x: None
            width: 150
            font_size: 16
            pos_hint: {"center_x":0.5}

        MDTextFieldRound:
            id: Gpr
            hint_text: 'Gпр'
            size_hint_x: None
            width: 150
            font_size: 16
            pos_hint: {"center_x":0.5}

        MDTextFieldRound:
            id: Pn
            hint_text: 'Pн'
            size_hint_x: None
            width: 150
            font_size: 16
            pos_hint: {"center_x":0.5}

        MDTextFieldRound:
            id: Tn
            hint_text: 'Тн'
            size_hint_x: None
            width: 150
            font_size: 16
            pos_hint: {"center_x":0.5}

        MDTextFieldRound:
            id: M
            hint_text: 'М'
            size_hint_x: None
            width: 150
            font_size: 16
            pos_hint: {"center_x":0.5}

        MDTextFieldRound:
            id: Tg
            hint_text: 'Тг'
            size_hint_x: None
            width: 150
            font_size: 16
            pos_hint: {"center_x":0.5}

        MDRectangleFlatButton:
            text: 'Расчёт'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            on_press: root.manager.current = 'result'
            on_press: app.update_plot()

<ResultScreen>:
    name: 'result'
    MDCard:
        pos_hint: {'center_x':0.5,'center_y':0.5}
        elevation: 10
        padding: 15
        spacing: 25
        orientation: 'vertical'

        MDBoxLayout:
            id: expense_graph

        MDRectangleFlatButton:
            text: 'Назад'
            pos_hint: {'center_x':0.5,'center_y':0.3}
            on_press: root.manager.current = 'main'
            on_press: app.delplt()
"""


class MainScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(ResultScreen(name='result'))


class GTDcalc(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        screen = Builder.load_string(screens)
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

        Mp = float(MDApp.get_running_app().root.get_screen('main').ids.M.text) #1
        H = float(MDApp.get_running_app().root.get_screen('main').ids.H.text) #300
        sigmaVH = -0.169714286*Mp+1.213523810
        if sigmaVH > 1:
            sigmaVH = 1
        Gpr = float(MDApp.get_running_app().root.get_screen('main').ids.Gpr.text) #26
        Pn = 0.0005517*H**2-11.9457454*H+101281.8063251
        Tn = -0.00000000672*H**2-0.00646850169*H+288.14306710633
        an = 0.00000002227*H**2-0.00382688981*H+340.28507315515
        k = 1.4
        kg = 1.33
        Tg = float(MDApp.get_running_app().root.get_screen('main').ids.Tg.text) #1600
        sigmaKS = 0.95
        kpdTK = 0.9
        kpdTTK = 0.99
        delta_ohl = 0.05
        m = 0.6
        kpdTV = 0.9
        kpdTTV = 0.99
        Vp = Mp*an
        lyambda =  sqrt( ( ((k+1)/2)*Mp**2 ) / (1+(((k-1)/2)*Mp**2)) )
        tau = 1-(k-1)/(k+1)*lyambda**2
        pi =  pow(tau,k/(k-1))
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
        pi_c1s =  pow(1-(kg-1)*lyambda_c1s**2,kg/(kg-1))
        P1cs = Pt*pi_c1s
        lyambda_c1 = 0.97
        pi_c1 =  pow(1-(kg-1)*lyambda_c1**2,kg/(kg-1))
        P1c = P1cs/pi_c1
        Tc = Tt*(1+m*Tvn/Tt)/(1+m)
        Pc = (Pvn+P1c)/2

        x=["Н", "B", "BH", "K", "Г", "TK", "T", "C"]
        t=[Tn, Tvh, Tvn, Tk, Tg, Ttk, Tt, Tc]
        p=[Pn, Pvh, Pvn, Pk, Pg, Ptk, Pt, Pc]

        plt.plot(x,p,x,t)
        plt.grid()
        plotShow.ids.expense_graph.add_widget(FigureCanvasKivyAgg(figure=plt.gcf()))


GTDcalc().run()
