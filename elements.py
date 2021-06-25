screen_helper = """
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
