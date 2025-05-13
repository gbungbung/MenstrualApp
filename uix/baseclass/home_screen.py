from kivymd.app import MDApp
app = MDApp.get_running_app()

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.pickers import MDDatePicker
from datetime import date, datetime, timedelta
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.spinner import Spinner
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton

from uix.baseclass.dirs import Amala, AppData

class InitScreen(Screen):
    txt =  StringProperty()
    def __init__(self, **kw):
        super(InitScreen, self).__init__(**kw)
        self.txt = "Welcome to the menstrualHealth, track, and learn progress your circles"
        try:
            name= Amala.u_d_load()['p_dt']['f_name']
            self.txt = f"Hello! {name}, welcome to the menstrualHealth, track, and learn progress your circles"
        except: self.txt = self.txt

    def on_enter(self, *args):
        # This makes the home.kv to be loadded maltiple times
        # only if This class is placed in home.kv
        self.event = Clock.schedule_interval(self.change_screen, 5)

    def change_screen(self, dt):
        try:
            # If there is menstrual dates saved then proceed to home
            Amala.u_d_load()['menstrual_history']
            self.parent.set_current("init_2screen")
            #self.parent.set_current("allscreen")
        except: self.parent.set_current("init_2screen")
        self.event.cancel()

class Init_2Screen(Screen):
    def __init__(self, **kw):
        super(Init_2Screen, self).__init__(**kw)
    
    def save_preg_state(self, state):
        Amala.save_preg_state(state)
        Init_3Screen.preg_state = state
        self.parent.set_current('init_3screen')

class Init_3Screen(Screen):
    preg_state = StringProperty()
    def __init__(self, **kw):
        super(Init_3Screen, self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        widg= self.ids.due_date_widgt
        widg.clear_widgets()
        if self.preg_state == 'No': widg.height = '0dp'
        elif self.preg_state == 'Yes':
            label = MDLabel(size_hint_y=None,
                        height=40,
                        text='[size=12][i]And/Or[/i][/size] \nDue date',
                        halign='center',
                        markup=True)
            text_field = MDTextField(
                        id='due_date',
                        hint_text='Due date',
                        multiline=False,
                        font_size='12sp',
                        mode='rectangle',
                        radius=[5,5,5,5],
                        helper_text_mode='persistent',

                        hint_text_color_focus=(0,0,0,1),
                        line_color_focus=(0,0,0,1),
                        text_color_focus=(0,0,0,1),
                        pos_hint={"center_y": .5, "center_x":.5})
            self.widgets = {'due_date': text_field}
            widg.height = '100dp'
            widg.add_widget(label)
            widg.add_widget(text_field)

    def save_date(self):
        self.lmp = ''
        self.delivery_date = ''
        ldt = self.ids.last_m_date
        last_date = ldt.text
        try:
            ddt = self.widgets['due_date']
            ddt.helper_text_color_normal = (1,0,0,1)
            ddt.helper_text_color_focus = (1,0,0,1)
            due_date = ddt.text
        except: pass
        ldt.helper_text_color_normal = (1,0,0,1)
        ldt.helper_text_color_focus = (1,0,0,1)
        
        if self.preg_state == 'No':
            # Set LMP to next page to gather range then save 4 consecutive LMP
            try:
                lmp_1 = datetime.strptime(last_date, "%Y-%m-%d")
                dt = (datetime.strptime(str(date.today()), "%Y-%m-%d") - lmp_1).days
                if dt < 0:
                    ldt.helper_text = 'Date surpass today'
                else:
                    ldt.helper_text_color_normal = 'gray'
                    ldt.helper_text_color_focus = 'green'
                    ldt.helper_text = 'Good!'
                    # Logic to move to range page
                    Init_4Screen.last_date = last_date
                    print(last_date)
                    #self.parent.set_current('init_4screen')
                    print(last_date)
            except:
                ldt.helper_text = 'Wrong format'
        elif self.preg_state == 'Yes':
            if last_date == '' and due_date == '':
                    ldt.helper_text = 'Fill one of the field'
                    ddt.helper_text = 'Fill one of the field'
            elif last_date == '' and due_date != '':
                try:
                    due_d = datetime.strptime(due_date, "%Y-%m-%d")
                    dt = (datetime.strptime(str(date.today()), "%Y-%m-%d") - due_d).days
                    if dt > 0:
                        ddt.helper_text = 'Date past yesterday'
                    else:
                        ddt.helper_text_color_normal = 'gray'
                        ddt.helper_text_color_focus = 'green'
                        ddt.helper_text = 'Good!'

                        ldt.helper_text_color_normal = 'gray'
                        ldt.helper_text_color_focus = 'gray'
                        ldt.helper_text = ''

                        # Logic to deliver lmp and due date
                        lmp = (due_d - timedelta(280)).strftime('%Y-%m-%d')
                        Init_4Screen.last_date = lmp
                        Init_4Screen.due_date = due_d.strftime('%Y-%m-%d')
                        self.parent.set_current('init_4screen')
                except:
                    ddt.helper_text = 'Wrong format'
            elif last_date != '' and due_date == '':
                # check for last date validity
                try:
                    lmp_ = datetime.strptime(last_date, "%Y-%m-%d")
                    dt = (datetime.strptime(str(date.today()), "%Y-%m-%d") - lmp_).days
                    if dt < 0:
                        ldt.helper_text = 'Date surpass today'
                    else:
                        ldt.helper_text_color_normal = 'gray'
                        ldt.helper_text_color_focus = 'green'
                        ldt.helper_text = 'Good!'

                        ddt.helper_text_color_normal = 'gray'
                        ddt.helper_text_color_focus = 'gray'
                        ddt.helper_text = ''
                        # logic to save lmp
                        due_d_ = (lmp_ + timedelta(280)).strftime('%Y-%m-%d')
                        Init_4Screen.last_date = (lmp_).strftime('%Y-%m-%d')
                        Init_4Screen.due_date = due_d_
                        self.parent.set_current('init_4screen')
                except:
                    ldt.helper_text = 'Wrong format'
            
            elif last_date != '' and due_date != '':
                # Check for due date validity
                try:
                    d = datetime.strptime(due_date, "%Y-%m-%d")
                    dt = (datetime.strptime(str(date.today()), "%Y-%m-%d") - d).days
                    if dt > 0:
                        ddt.helper_text = 'Date past yesterday'
                    else:
                        ddt.helper_text_color_normal = 'gray'
                        ddt.helper_text_color_focus = 'green'
                        ddt.helper_text = 'Good!'
                        # logic to save due date
                        Init_4Screen.due_date = (d).strftime('%Y-%m-%d')
                except:
                    ddt.helper_text = 'Wrong format'
                # check for last date validity
                try:
                    lmp_ = datetime.strptime(last_date, "%Y-%m-%d")
                    dt = (datetime.strptime(str(date.today()), "%Y-%m-%d") - lmp_).days
                    if dt < 0:
                        ldt.helper_text = 'Date surpass today'
                    else:
                        ldt.helper_text_color_normal = 'gray'
                        ldt.helper_text_color_focus = 'green'
                        ldt.helper_text = 'Good!'

                        # logic to save lmp
                        Init_4Screen.last_date = (lmp_).strftime('%Y-%m-%d')
                except:
                    ldt.helper_text = 'Wrong format'

                if ldt.helper_text == 'Good!' and ddt.helper_text == 'Good!':
                    self.parent.set_current('init_4screen')

class Init_4Screen(Screen):
    last_date = StringProperty()
    due_date = StringProperty()
    def __init__(self, **kw):
        super(Init_4Screen, self).__init__(**kw)
    
    def on_enter(self, *args):
        print(self.last_date)
        print(self.due_date)

    def save_dates(self):
        range = 28
        lmp_1 = datetime.strptime(self.last_date, "%Y-%m-%d")
        date2= (lmp_1 + timedelta(days=int(range))).strftime("%Y-%m-%d")
        date3= (lmp_1 + timedelta(days=int(range + range))).strftime("%Y-%m-%d")
        date4= (lmp_1 + timedelta(days=int(range + range + range))).strftime("%Y-%m-%d")
        Amala.save_mesntrual_data(date1=self.last_date, date2=date2, date3=date3, date4=date4)

class AllScreen(Screen):
    def __init__(self, **kw):
        super(AllScreen, self).__init__(**kw)

    def change_screen(self, txt):
        if  txt == 'account':
            self.ids.scrns_.current='setup_'
        elif  txt == 'menstrual_0':
            self.ids.scrns_.current = 'menstrual_0'
        elif  txt == 'home':
            self.ids.scrns_.current='home_'
        elif  txt == 'notification_':
            self.ids.scrns_.current='notification_'
  
class Home(Screen):
    tip1= StringProperty()
    tip2= StringProperty()
    on_count_day = StringProperty()
    exact_days = StringProperty()

    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        
    def on_pre_enter(self, **kwargs):
        self.date_calc()
        self.day_change('Today')
    
    def date_calc(self):
        tdy= date.today()
        try:
            self.dys = Amala.auto_add_menstry_day()

            if self.dys == '1': mark_up= 'st'
            elif self.dys == '2': mark_up= 'nd'
            elif self.dys == '3': mark_up= 'rd'
            else: mark_up= 'th'

            self.on_count_day = '{}\n\n{}[sup]{}{}'.format(tdy, self.dys, mark_up, '[/sup][sub][/sub] day on the circle')
            self.exact_days = '{}[sup]{}{}'.format(self.dys, mark_up,  '[/sup] [sub] [/sub]')
        except:
            self.dys = '0'
            mark_up= 'th'
            self.on_count_day = 'Add some data to finish setup'
            self.exact_days = '{}[sup]{}{}'.format(self.dys, 
                                mark_up,  '[/sup] [sub] [/sub]')

    def day_change(self, txt):
        if self.dys == '0':
            self.tip = 'First time here? fill  in some data to continue'
        else:
            #if txt == 'Yesterday':
            #    self.tip = f'{Amala.processing_ans(day=str(int(self.dys)-1))}'
            if txt == 'Today':
                self.tip1 = Amala.processing_ans(day=self.dys)[1]
                self.tip2 = Amala.processing_ans(day=self.dys)[0]
            elif txt == 'Tomorrow':
                self.tip1 = Amala.processing_ans(day=str(int(self.dys)+1))[1]
                self.tip2 = Amala.processing_ans(day=str(int(self.dys)+1))[0]

class MenstrualDtScreen0(Screen):
    def __init__(self, **kwargs):
        super(MenstrualDtScreen0, self).__init__(**kwargs)
        self.dialog = None
        self.range_ = 28
        self.d1 = ''
        self.dt2 = ''
        self.dt3 = ''
        self.dt4 = ''

    def on_enter(self, *args):
        try:
            lst = list(Amala.u_d_load()['menstrual_history'])[-1]
            self.dt1 = Amala.u_d_load()['menstrual_history'][lst]
            self.ids.date_.text = self.dt1
            self.ids.save_update_btn.text = 'update'
        except: pass
        
    def on_save(self, instance, value, date_range):
        if self.txt_fld_id == 'date_':
            self.ids.date_.text = str(value)

    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self, vl):
        date_dialog = MDDatePicker()
        self.txt_fld_id = vl
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def check_date_(self):
        date_ = self.ids.date_.text
        self.ids.date_.helper_text_color_normal = (1,0,0,1)
        self.ids.date_.helper_text_color_focus = (1,0,0,1)
        if date_ == '': self.ids.date_.helper_text = 'Field is required*'
        else:
            try:
                datetime.strptime(date_, "%Y-%m-%d")
                self.ids.date_.helper_text_color_normal = 'gray'
                self.ids.date_.helper_text_color_focus = 'green'
                self.ids.date_.helper_text = 'Good!'
            except: self.ids.date_.helper_text = 'Format should be yyyy-mm-dd*'

    def save__(self):
        self.dialog = None
        if self.ids.date_.helper_text == 'Good!':
            date_ = self.ids.date_.text
            ag = datetime.strptime(date_, "%Y-%m-%d")
            dt = (datetime.strptime(str(date.today()), "%Y-%m-%d") - ag).days
            if dt >= 0:
                try:
                    lst = list(Amala.u_d_load()['menstrual_history'])[-2]
                    dt2 = Amala.u_d_load()['menstrual_history'][lst]
                    if (datetime.strptime(date_, "%Y-%m-%d") - datetime.strptime(dt2, "%Y-%m-%d")).days <= 0:
                        self.ids.date_.helper_text = 'Date entered surpass previous month date'
                    elif 0 <= (datetime.strptime(date_, "%Y-%m-%d") - datetime.strptime(dt2, "%Y-%m-%d")).days <= 15:
                        self.ids.date_.helper_text = 'Date added mean you bleeded in less than 21 days, True?'
                    else: self.pop_pop()
                except: self.pop_pop()
            else:
                self.ids.date_.helper_text_color_normal = (1,0,0,1)
                self.ids.date_.helper_text_color_focus = (1,0,0,1)
                self.ids.date_.helper_text = 'The date entered past today'

    def prob_dialog(self, *args):
        if self.btn == 'update': buttons=[
                    MDFillRoundFlatButton(text="No", on_release= self.close_dialog, md_bg_color= app.main_color),
                    MDFillRoundFlatButton(text="Yes", on_release= self.change_screen, md_bg_color= app.main_color),
                    ]
        else: buttons=[
                    MDFillRoundFlatButton(text="No", on_release= self.close_dialog, md_bg_color= app.main_color),
                    MDFillRoundFlatButton(text="Yes", on_release= self.save_dt, md_bg_color= app.main_color),
                    ]
        self.dialog = MDDialog(text=self.txt, buttons = buttons,)
        self.dialog.open()

    def ask_dialog(self, btn):
        tx = "You always follow 28 days pattern?"
        buttons=[
                MDFillRoundFlatButton(text="No", on_release= self.change_screen, md_bg_color= app.main_color),
                MDFillRoundFlatButton(text="Yes", on_release= self.save_dt, md_bg_color= app.main_color),
                ]
        if btn == 'update':
            tx = 'You want to modify other previous dates?'
            buttons=[
                    MDFillRoundFlatButton(text="No", on_release= self.save_dt, md_bg_color= app.main_color),
                    MDFillRoundFlatButton(text="Yes", on_release= self.change_screen, md_bg_color= app.main_color),
                    ]
            
        if self.ids.date_.text == '': self.ids.date_.helper_text = 'Field can not be empty'
        elif self.ids.date_.helper_text != '': pass
        else:
            self.dialog = MDDialog(text=tx, buttons = buttons,)
            self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def save_dt(self, instance):
        self.dialog.dismiss()
        self.dt1= self.ids.date_.text
        range_ = 28
        if self.ids.save_update_btn.text == 'update':
            Amala.update_last_menstrual_data(self.dt1)
        else:
            if self.dt2 == '':
                dt = datetime.strptime(self.dt1, "%Y-%m-%d") - timedelta(days=range_)
                self.dt2= f'{dt.strftime("%Y-%m-%d")}'
            if self.dt3 == '':
                nw_dt3 = datetime.strptime(self.dt2, "%Y-%m-%d") - timedelta(days=range_)
                self.dt3= f'{nw_dt3.strftime("%Y-%m-%d")}'
            if self.dt4 == '':
                nw_dt4 = datetime.strptime(self.dt3, "%Y-%m-%d") - timedelta(days=range_)
                self.dt4=f'{nw_dt4.strftime("%Y-%m-%d")}'
            Amala.save_mesntrual_data(date1=self.dt4, date2=self.dt3, 
                                    date3=self.dt2, date4=self.dt1)
        self.parent.parent.parent.ids.scrns_.current = 'home_'

    def change_screen(self, instance):
        self.dialog.dismiss()
        MenstrualDtScreen.mod_date  = self.ids.date_.text
        self.parent.parent.parent.ids.scrns_.current = 'menstrual_'

    def on_number_selected(self, spinner, text):
        self.range_ = text

    def pop_pop(self):
        if not self.dialog:
            spinn = SpinnerNumber(
                    text = f'{self.range_}',
                    values =  [str(i) for i in range(1, 91)],
                    size_hint = (None, None),
                    background_color = (0.7, 0.7, 0.7, 0),
                    pos_hint = {'center_x': .5}
            )
            spinn.bind(text= self.on_number_selected)
            self.dialog  = MDDialog(
                                    type = 'custom',
                                    content_cls = Builder.load_string(''' 
MDBoxLayout:
    orientation: 'vertical'
    size_hint_y: None
    height: '40dp'
    Widget:
        size_hint_y: None
        height: '10dp'
                                        '''
                                    ),
                                    buttons = [MDFlatButton(text= 'Save', on_release=self.save_dt)]
                                    )
            self.dialog.content_cls.add_widget(spinn)
            self.dialog.open()

class MenstrualDtScreen(Screen):
    mod_date = StringProperty()
    def __init__(self, **kwargs):
        super(MenstrualDtScreen, self).__init__(**kwargs)
        
    def on_enter(self, **kwargs):
        last_p_dates= {}
        try:
            last_dates = Amala.u_d_load()['menstrual_history']
            la = list(last_dates)
            for d in la[-4:]:
                last_p_dates['date_1'] = last_dates[la[-1]]
                last_p_dates['date_2'] = last_dates[la[-2]]
                last_p_dates['date_3'] = last_dates[la[-3]]
                last_p_dates['date_4'] = last_dates[la[-4]]
            self.ids.save_update_btn.text = 'update'
        except:
            last_p_dates= {"date_1": '', "date_2": '', "date_3": '', "date_4": ''}
            self.ids.save_update_btn.text = 'save'
         
        self.ids.date_1.text = self.mod_date
        self.ids.date_2.text = last_p_dates['date_2']
        self.ids.date_3.text = last_p_dates['date_3']
        self.ids.date_4.text = last_p_dates['date_4']
        
    def on_save(self, instance, value, date_range):
        if self.txt_fld_id == 'date_1':
            self.ids.date_1.text = str(value)
        elif self.txt_fld_id == 'date_2':
            self.ids.date_2.text = str(value)
        elif self.txt_fld_id == 'date_3':
            self.ids.date_3.text = str(value)
        elif self.txt_fld_id == 'date_4':
            self.ids.date_4.text = str(value)
        else: pass

    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self, vl):
        date_dialog = MDDatePicker()
        self.txt_fld_id = vl
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def check_date_errors(self):
        date_1 = self.ids.date_1.text
        date_2 = self.ids.date_2.text
        date_3 = self.ids.date_3.text
        date_4 = self.ids.date_4.text
        self.ids.date_1.helper_text_color_normal = (1,0,0,1)
        self.ids.date_1.helper_text_color_focus = (1,0,0,1)
        self.ids.date_2.helper_text_color_normal = (1,0,0,1)
        self.ids.date_2.helper_text_color_focus = (1,0,0,1)
        self.ids.date_3.helper_text_color_normal = (1,0,0,1)
        self.ids.date_3.helper_text_color_focus = (1,0,0,1)
        self.ids.date_4.helper_text_color_normal = (1,0,0,1)
        self.ids.date_4.helper_text_color_focus = (1,0,0,1)
        if date_1 == '':
            self.ids.date_1.helper_text = 'This field is important'
        else:
            try:
                datetime.strptime(date_1, "%Y-%m-%d")
                self.ids.date_1.helper_text = ''
            except: self.ids.date_1.helper_text = 'Format should be YYYY-MM-DD'
        if date_2 == '':
            self.ids.date_2.helper_text_color_normal = 'gray'
            self.ids.date_2.helper_text_color_focus = 'gray'
            self.ids.date_2.helper_text = 'This field is optional'
        else:
            try:
                datetime.strptime(date_2, "%Y-%m-%d")
                self.ids.date_2.helper_text = ''
            except: self.ids.date_2.helper_text = 'Format should be YYYY-MM-DD'
        if date_3 == '':
            self.ids.date_3.helper_text_color_normal = 'gray'
            self.ids.date_3.helper_text_color_focus = 'gray'
            self.ids.date_3.helper_text = 'This field is optional'
        else:
            try:
                datetime.strptime(date_3, "%Y-%m-%d")
                self.ids.date_3.helper_text = ''
            except: self.ids.date_3.helper_text = 'Format should be YYYY-MM-DD'
        if date_4 == '':
            self.ids.date_4.helper_text_color_normal = 'gray'
            self.ids.date_4.helper_text_color_focus = 'gray'
            self.ids.date_4.helper_text = 'This field is optional'
        else:
            try:
                datetime.strptime(date_4, "%Y-%m-%d")
                self.ids.date_4.helper_text = ''
            except: self.ids.date_4.helper_text = 'Format should be YYYY-MM-DD'
        
    def save_dt(self):
        dt1= self.ids.date_1.text
        dt2 = self.ids.date_2.text
        dt3 = self.ids.date_3.text
        dt4 = self.ids.date_4.text
        if dt2 == '':
            d = datetime.strptime(dt1, "%Y-%m-%d")
            dt = d - timedelta(days=int(28))
            dt2= dt.strftime("%Y-%m-%d")
        if dt3 == '':
            nw_dt3 = datetime.strptime(dt2, "%Y-%m-%d") - timedelta(days=int(28))
            dt3= nw_dt3.strftime("%Y-%m-%d")
        if dt4 == '':
            nw_dt4 = datetime.strptime(dt3, "%Y-%m-%d") - timedelta(days=int(28))
            dt4= nw_dt4.strftime("%Y-%m-%d")
        
        Amala.save_mesntrual_data(date1=dt4, date2=dt3, date3=dt2, date4=dt1)

    def update_dt(self):
        Amala.update_menstrual_data(date1=self.ids.date_4.text, 
                                    date2=self.ids.date_3.text, 
                                    date3=self.ids.date_2.text, 
                                    date4=self.ids.date_1.text)

    def calc_dates(self):
        date_1 = self.ids.date_1.text
        date_2 = self.ids.date_2.text
        date_3 = self.ids.date_3.text
        date_4 = self.ids.date_4.text
        range = 28
        tdy = date.today()
        if date_1 == '':
            try:
                date_1 = (datetime.strptime(date_2, "%Y-%m-%d") + timedelta(days=range)).strftime("%Y-%m-%d")
                if date_3 == '':
                    date_3 = (datetime.strptime(date_2, "%Y-%m-%d") - timedelta(days=range)).strftime("%Y-%m-%d")
                    if date_4 == '':
                        date_4 = (datetime.strptime(date_3, "%Y-%m-%d") - timedelta(days=range)).strftime("%Y-%m-%d")
                else:
                    if date_4 == '':
                        date_4 = (datetime.strptime(date_3, "%Y-%m-%d") - timedelta(days=range)).strftime("%Y-%m-%d")
            except:
                try:
                    date_2 = (datetime.strptime(date_3, "%Y-%m-%d") + timedelta(days=range)).strftime("%Y-%m-%d")
                    date_1 = (datetime.strptime(date_2, "%Y-%m-%d") + timedelta(days=range)).strftime("%Y-%m-%d")
                    if date_4 == '':
                        date_4 = (datetime.strptime(date_3, "%Y-%m-%d") - timedelta(days=range)).strftime("%Y-%m-%d")
                except:
                    if date_4 != '':
                        date_3 = (datetime.strptime(date_4, "%Y-%m-%d") + timedelta(days=range)).strftime("%Y-%m-%d")
                        date_2 = (datetime.strptime(date_3, "%Y-%m-%d") + timedelta(days=range)).strftime("%Y-%m-%d")
                        date_1 = (datetime.strptime(date_2, "%Y-%m-%d") + timedelta(days=range)).strftime("%Y-%m-%d")
                        if datetime.strptime(datetime.strptime(date_1, "%Y-%m-%d"), "%Y-%m-%d") > datetime.strptime(tdy.strftime("%Y-%m-%d"), "%Y-%m-%d"):
                            return f'The date entered must be invalid, your last months date seem to be in future, adjust your dates'
                    else: return f'No date filled in any field'
        else:
            if date_2 == '':
                date_2 = (datetime.strptime(date_1, "%Y-%m-%d") - timedelta(days=range)).strftime("%Y-%m-%d")
            if date_3 == '':
                date_3 = (datetime.strptime(date_2, "%Y-%m-%d") - timedelta(days=range)).strftime("%Y-%m-%d")
            if date_4 == '':
                date_4 = (datetime.strptime(date_3, "%Y-%m-%d") - timedelta(days=range)).strftime("%Y-%m-%d")
            if datetime.strptime(date_1, "%Y-%m-%d") > datetime.strptime(tdy.strftime("%Y-%m-%d"), "%Y-%m-%d"):
                return f'The date entered must be invalid, your last months date seem to be in future, adjust your dates'
        
        self.ids.date_1.text = date_1
        self.ids.date_2.text = date_2
        self.ids.date_3.text = date_3
        self.ids.date_4.text = date_4
 
    def change_screen(self):
        date_1 = self.ids.date_1.text
        date_2 = self.ids.date_2.text
        date_3 = self.ids.date_3.text
        date_4 = self.ids.date_4.text
        try:
            datetime.strptime(date_4, "%Y-%m-%d")
            self.ids.date_4.hint_text = 'Last 4 month menstrual date'
        except:
            if self.ids.date_4.text == '':
                self.ids.date_4.hint_text = 'Last 4 month menstrual date'
            else: self.ids.date_4.hint_text = 'Format should be YYYY-MM-DD'
        try: 
            datetime.strptime(date_3, "%Y-%m-%d")
            self.ids.date_3.hint_text = 'Last 3 month menstrual date'
        except:
            if self.ids.date_3.text == '':
                self.ids.date_3.hint_text = 'Last 3 month menstrual date'
            else: self.ids.date_3.hint_text = 'Format should be YYYY-MM-DD'
        try:
            datetime.strptime(date_2, "%Y-%m-%d")
            self.ids.date_2.hint_text = 'Last 2 month menstrual date'
        except:
            if self.ids.date_2.text == '':
                self.ids.date_2.hint_text = 'Last 2 month menstrual date'
            else:  self.ids.date_2.hint_text = 'Format should be YYYY-MM-DD'
        try: 
            datetime.strptime(date_1, "%Y-%m-%d")
            self.ids.date_1.hint_text = 'Last month menstrual date'
            try:
                if self.ids.save_update_btn.text == 'update':
                    self.update_dt()
                    self.parent.parent.parent.ids.scrns_.current = 'home_'
                else:
                    self.save_dt()
                    self.parent.parent.parent.ids.scrns_.current = 'home_'
            except: pass
        except: 
            if self.ids.date_1.text == '': self.ids.date_1.hint_text = 'Previous menstrual date is necessary'
            else: self.ids.date_1.hint_text = 'Format should be YYYY-MM-DD'

class Setups(Screen):
    avatar= StringProperty()
    user_= StringProperty ()
    age= StringProperty ()
    m_issue= StringProperty ()
    last_period = StringProperty('')
    next_period = StringProperty('')
    
    def __init__(self, **kw):
        super(Setups, self).__init__(**kw)
        self.menu = None
        self.items = ["Light theme", "Dark theme"]
        self.load_data()

    def on_enter(self, **kw):
        self.load_data()

    def load_data(self):
        try:
            ## Extract data from the app data source
            e = Amala.u_d_load()
            f_name= e['p_dt']['f_name']
            l_name= e['p_dt']['s_name']
            self.user_ = '{} {}'.format(f_name, l_name)

            self.age= e['p_dt']['d_birth'] 

            ag = datetime.today() - datetime.strptime(self.age, "%Y-%m-%d")
            if self.age == '': self.age = 'not specified'
            else: self.age = str(int(ag.days/365))
            
            self.m_issue = e['med_issue']
            if self.m_issue == '': self.m_issue = 'no medical issue'
            
            self.avatar = '' #e['avatar']
            if self.avatar == '': self.avatar = "./uix/assets/img/user.png"
        except:
            self.user_ = "no name"
            self.avatar = "./uix/assets/img/user.png"
        try:
            dts = list(Amala.u_d_load()['menstrual_history'])[-1]
            self.last_period = Amala.u_d_load()['menstrual_history'][dts]
    
            d3 = datetime.strptime(self.last_period, "%Y-%m-%d")
            tdy = datetime.strptime(str(date.today()), "%Y-%m-%d")
            range = Amala.range()
            next_ = d3 + timedelta(days=int(range))
            self.next_period=f'{next_.strftime("%Y-%m-%d")}'
        except:
            self.last_period = ''
            self.next_period = ''
            
    def show_(self, tx):
        if tx == 'about': ExtraScreen.header = 'About us'
        elif tx == 'terms': ExtraScreen.header = 'Terms of use'
        else: ExtraScreen.header = 'Privacy policy'
        self.parent.parent.parent.ids.scrns_.current='extra_data_'

    def modify_last_menstrual(self):
        self.parent.parent.parent.ids.scrns_.current='menstrual_0'

    def next_period_dialog(self):
        tx = f"We predict your next date based on range of your last menstrual cycles which is {Amala.range()} days"
        buttons=[MDFillRoundFlatButton(text="Ok", on_release= self.close_dialog, md_bg_color= app.main_color),]
        self.dialog = MDDialog(text=tx, buttons = buttons,)
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def change_screen(self):
        self.parent.parent.parent.ids.scrns_.current='user_data_'

    def theme_change(self):
        menu_items =[{
                        "text": item,
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=item: self.on_select(x)
                    } for item in self.items]
        if not self.menu:
            self.menu = MDDropdownMenu(
                caller = self.ids.theme_,
                items =  menu_items,
                position = "center",
                width = 200,
            )
        else:
            self.menu.items = menu_items
        self.menu.open()

    def on_select(self, text):
        self.ids.theme_.text = f'Themes     [i]({text})[/i]'
        self.menu.dismiss()
        self.ids.theme_.focus = False
        if text == 'Dark theme':
            #save the current state theme into app data
            AppData._theme_add('Dark')
            #Set background color of the custome button after changing theme
            # they behave defferent if not handled manually
            self.ids.last_p.md_bg_color = 0,0,0,.05
            self.ids.next_p.md_bg_color = 0,0,0,.05
            self.ids.theme_.md_bg_color = 0,0,0,.05
            self.ids.priv_p.md_bg_color = 0,0,0,.05
            self.ids.abt_.md_bg_color = 0,0,0,.05
            self.ids.term_.md_bg_color = 0,0,0,.05
            #Change the current state theme
            app.theme_cls.theme_style = 'Dark'
        elif text == 'Light theme':
            AppData._theme_add('Light')
            self.ids.last_p.md_bg_color = (1,1,1,1)
            self.ids.next_p.md_bg_color = (1,1,1,1)
            self.ids.theme_.md_bg_color = (1,1,1,1)
            self.ids.priv_p.md_bg_color = (1,1,1,1)
            self.ids.abt_.md_bg_color = (1,1,1,1)
            self.ids.term_.md_bg_color = (1,1,1,1)
            app.theme_cls.theme_style = 'Light'

class UserDataScreen(Screen):
    def __init__(self, **kwargs):
        super(UserDataScreen, self).__init__(**kwargs)
        self.menu = None
        self.items = ["A", "A+", "B", "B+", "AB", "AB+", "O", "O+"]
        
    def on_enter(self, **kwargs):
        try:
            ## Extract data from the app data source
            e = Amala.u_d_load()

            f_name= e['p_dt']['f_name']
            l_name= e['p_dt']['s_name']
            self.ids.f_name.text = f_name
            self.ids.l_name.text = l_name
            self.ids.d_birth.text = e['p_dt']['d_birth']
            self.ids.m_issue.text = e['med_issue']
            self.ids.loc.text = e['p_dt']['b_loc']
            self.ids.weight_.text = e['p_dt']['weight_']
            self.ids.height_.text = e['p_dt']['height_']
            self.ids.b_group.text = e['p_dt']['b_group']
        except: pass
    
    def on_save(self, instance, value, date_range):
        self.ids.d_birth.text = str(value)
        
    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    
    def save_dt(self):
        d_birth= self.ids.d_birth.text
        f_name= self.ids.f_name.text 
        l_name = self.ids.l_name.text
        m_issue= self.ids.m_issue.text
        b_group= self.ids.b_group.text
        height_= self.ids.height_.text
        weight_= self.ids.weight_.text
        location= self.ids.loc.text

        gender= 'Female'
        avatar = ''
        try:
            self.check_errors()
            if self.error is False:
                Amala.s_u_data(avatar=avatar, first_name=f_name, second_name=l_name, 
                            gender=gender, d_birth=d_birth, blood_group=b_group, 
                            location=location, weight_=weight_, height_=height_, medical1=m_issue)
                
                self.parent.parent.parent.ids.scrns_.current='setup_'
        except: pass

    def drop_blood_menu(self):
        menu_items =[{
                        "text": item,
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=item: self.on_select(x)
                    } for item in self.items]
        if not self.menu:
            self.menu = MDDropdownMenu(
                caller = self.ids.b_group,
                items =  menu_items,
                position = "bottom",
                width = 200,
            )
        else:
            self.menu.items = menu_items
        self.menu.open()

    def on_select(self, text):
        self.ids.b_group.text = text
        self.menu.dismiss()
        self.ids.b_group.focus = False

    def check_errors(self):
        d_birth= self.ids.d_birth.text
        weight_= self.ids.weight_.text
        self.ids.d_birth.helper_text_color_normal = (1,0,0,1)
        self.ids.d_birth.helper_text_color_focus = (1,0,0,1)
        self.ids.weight_.helper_text_color_normal = (1,0,0,1)
        self.ids.weight_.helper_text_color_focus = (1,0,0,1)
        if d_birth == '':
            self.ids.d_birth.helper_text = 'Date of birth required*'
            self.error = True
        else:
            try:
                datetime.strptime(d_birth, "%Y-%m-%d")
                self.ids.d_birth.helper_text_color_normal = 'gray'
                self.ids.d_birth.helper_text_color_focus = 'gray'
                self.ids.d_birth.helper_text = ''
                self.error = False
            except:
                self.ids.d_birth.helper_text = 'Format should be yyyy-mm-dd'
                self.error = True
        if weight_ == '':
            self.ids.weight_.helper_text = 'Weight is required*'
            self.error = True
        else: 
            self.ids.weight_.helper_text_color_normal = 'gray'
            self.ids.weight_.helper_text_color_focus = 'gray'
            self.ids.weight_.helper_text = ''

class ExtraScreen(Screen):
    header = StringProperty()
    content = StringProperty()
    head = StringProperty()

    def __init__(self, **kwargs):
        super(ExtraScreen, self).__init__(**kwargs)
        
    def on_pre_enter(self, *args):
        if self.header == 'Privacy policy':
            self.head =self.header
            try:
                with open('./docs/privacy.txt', 'r') as f:
                    self.content = f.read()
            except: self.content = '[b]Ooops![/b] \n Some error occured, Privacy details should be shown here'
        elif self.header == 'About us':
            self.head =self.header
            try:
                with open('./docs/about.txt', 'r') as f: self.content = f.read()
            except: self.content = '[b]Ooops![/b] \n Some error occured, Help details should be shown here'
        elif self.header == 'Terms of use':
            self.head =self.header
            try:
                with open('./docs/terms.txt', 'r') as f: self.content = f.read()
            except: self.content = '[b]Ooops![/b] \n Some error occured, terms details should be shown here'

class NotificationScreen(Screen):
    def __init__(self, **kw):
        super(NotificationScreen, self).__init__(**kw)
class GroupButton():
    pass

class FlButton(ButtonBehavior, MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Tab(MDFloatLayout, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SpinnerNumber(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = (200, 40)
        self.background_color = (0.7, 0.7, 0.7, 0)
        self.color = (0,0,0,1)
        self.font_size = '28sp'