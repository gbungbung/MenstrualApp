import pathlib as Path
from kivy.utils import platform
import os
import json
from datetime import date, timedelta, datetime
import requests

if platform == 'android': ## get Android path 
    from android.storage import primary_external_storage_path, app_storage_path, secondary_external_storage_path
    from android.permissions import request_permissions, Permission
    from android import api_version
    permits = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]

    if api_version > 29: home= app_storage_path() # Data folders in android external storage/Scoped storage
    else: home= f'{primary_external_storage_path()}' # Data folders in android external storage

elif platform == 'win': home = Path.Path.home() ## Get Windows home folder

data_folder = '{}{}'.format(home, '/MenstrualHealth/dts')
app_folder = '{}{}'.format(home, '/MenstrualHealth/.datas')

### app version, languages selected, theme, last access, 
app_data = f"./uix/assets/a_d.json"

### Contains name, age, medical issue, other_personal issue
user_data = f"{data_folder}/u_d.json"

### Medical statements
menstr_d = f'./uix/assets/menstrualdata.json'

class Directories:
    '''A class to handle targeted OS(s) directories and files
       that is Android/IOS/Windows'''

    def make_dirs():
        '''Make initial directory'''
        try:
            if platform == 'android':
                request_permissions(permits)
        except: print('Failed to request permission')
        try:
            os.makedirs(app_folder) #Using os, since pathlib cant make nested dirs
            print('succes folder made')
        except FileExistsError:
            print('File exist')
        except Error as e:
            print(e)   
        try:
            os.makedirs(data_folder)
        except FileExistsError:
            print('File exist')
        except Error as e:
            print(e)   

class AppData:
    '''A class to load and process app data ie versions,
       missing files as such, Also handles user details'''
    def l_app_data():
        try:
            with open(app_data, 'r', encoding ='utf8') as n: data= json.load(n)
            return data
        except: return False

    def sett_dataL():
        try:
            with open(se_data, 'r', encoding ='utf8') as n: data= json.load(n)
            return data['settings']
        except: return False
        
    def theme_dataL():
        try:
            with open(se_data, 'r', encoding ='utf8') as n: data= json.load(n)
            return data['settings']['theme']
        except: return False

    def lang_dataL():
        try:
            with open(se_data, 'r', encoding ='utf8') as n: data= json.load(n)
            return data['settings']['lang']
        except: return False

    def database_L():
        try:
            with open(database, 'r') as n: data= json.load(n)
            return data
        except: return False

    def s_dataL():
        try:
            with open(se_data, 'r') as n: data= json.load(n)
            return data
        except: pass

    def stg_mother_lang_add(lang):
        data= {'settings':{'lang': lang}}
        dt= Udata.s_dataL()
        if dt is None:
            try:
                with open(se_data, 'w', encoding ='utf8') as f: json.dump(data, f, indent=4)
            except FileNotFoundError:
                os.makedirs(data_folder)
                with open(se_data, 'w', encoding ='utf8') as f: json.dump(data, f, indent=4)
        else:
            try:
                dt['settings']['lang'] = lang
                with open(se_data, 'w', encoding ='utf8') as f: json.dump(dt, f, indent=4)
            except:
                dt['settings']={'lang':lang}
                with open(se_data, 'w', encoding ='utf8') as f: json.dump(dt, f, indent=4)

    def stg_lang_foregn_add(lang):
        data= {'settings':{'flang1': lang}}
        dt= Udata.s_dataL()
        if dt is None:
            try:
                with open(se_data, 'w', encoding ='utf8') as f: json.dump(data, f, indent=4)
            except FileNotFoundError:
                os.makedirs(data_folder)
                with open(se_data, 'w', encoding ='utf8') as f: json.dump(data, f, indent=4)
        else:
            try:
                dt['settings']['flang1'] = lang
                with open(se_data, 'w', encoding ='utf8') as f: json.dump(dt, f, indent=4)
            except:
                dt['settings']={'flang1':lang}
                with open(se_data, 'w', encoding ='utf8') as f: json.dump(dt, f, indent=4)

    def _theme_add(theme):
        data= {'theme': theme}
        dt= AppData.l_app_data()
        if dt is None:
            try:
                with open(app_data, 'w', encoding ='utf8') as f: json.dump(data, f, indent=4)
            except FileNotFoundError:
                os.makedirs(data_folder)
                with open(app_data, 'w', encoding ='utf8') as f: json.dump(data, f, indent=4)
        else:
            try:
                dt['theme'] = theme
                with open(app_data, 'w', encoding ='utf8') as f: json.dump(dt, f, indent=4)
            except:
                dt = {'theme':theme}
                with open(app_data, 'w', encoding ='utf8') as f: json.dump(dt, f, indent=4)
                
class Amala():
    '''A class to handles user data and specific medical statements'''
    def l_menstr_data(d):
        try:
            data= requests.get('http://www.h.com')
            return data
        except:
            with open(menstr_d, 'r') as n: data= json.load(n)
            return data[d]

    def processing_ans(day):
        '''check if period set(this should be as input by user)
           check if age is on range i.e menopause or not.
        '''
        #TODO: Check for period onset on user details .json
        period_set = True
        if period_set is not True:
            u_d = Amala.u_d_load()
            if day >=33:
                ag = datetime.strptime(u_d["p_dt"]['d_birth'], "%Y-%m-%d")
                age = (datetime.strptime(str(date.today()), "%Y-%m-%d") - ag).days / 365
                if int(age) <= 45:
                    med_issue = u_d['med_issue']
                    if med_issue == '':
                        return f'''Dear {u_d['p_dt']['f_name']}, you might have early pregnant'''
                    else:
                        ## TODO: Check if the medical condition relates to onset of menstrual flow
                        return f'''Dear {u_d['p_dt']['f_name']}, It is more likely to wait a 
                                    more longer due to your medical issue'''
                else: return f'''Dear {u_d['p_dt']['f_name']}, with your age you are likely 
                                been entered a menopause stage or it is near a wait few days to confirm, 
                                its better to consult profetional doctor for conformation'''
        else:
            try:
                exp= Amala.l_menstr_data(day)['Explanation_short']
            except: exp = ''
            return [Amala.l_menstr_data(day)["Tip"], exp]

    def u_d_load():
        try:
            with open(user_data, 'r') as n: data= json.load(n)
            return data
        except: print('User data loading failure')

    def s_u_data(first_name, second_name, gender, d_birth, 
                    blood_group, location, medical1, height_, weight_, avatar):
        datas = {'p_dt': {'f_name':first_name.capitalize(), 
                            's_name': second_name.capitalize(), 
                            'avatar': avatar, 
                            'gender':gender, 'd_birth': d_birth, 
                            'b_group': blood_group, 
                            'height_': height_,
                            'weight_': weight_,
                            'b_loc': location.capitalize()},
                            'med_issue': medical1.capitalize()}

        dts = Amala.u_d_load()
        if dts is None:
            try:
                with open(user_data, 'w', encoding ='utf8') as f:
                    json.dump(datas, f, indent=4)
            except:
                Directories.make_dirs()
                with open(user_data, 'w', encoding ='utf8') as f:
                    json.dump(datas, f, indent=4)
        elif KeyError:
            dts.update(datas)
            with open(user_data, 'w', encoding ='utf8') as f:
                json.dump(dts, f, indent=4)
        else:
            with open(user_data, 'w', encoding ='utf8') as f:
                json.dump(datas, f, indent=4)

    def save_mesntrual_data(date1, date2, date3, date4):
        dts = Amala.u_d_load()
        if dts is None:
            mestr_histry= {'menstrual_history': {'date1':date1, 'date2':date2, 'date3':date3, 'date4':date4}}
            try:
                with open(user_data, 'w', encoding ='utf8') as f: json.dump(mestr_histry, f, indent=4)
            except:
                Directories.make_dirs()
                with open(user_data, 'w', encoding ='utf8') as f: json.dump(mestr_histry, f, indent=4)
        elif KeyError:
            menstr_histry = {'date1':date1, 'date2':date2, 'date3':date3, 'date4':date4}
            dts.update({'menstrual_history': menstr_histry})
            with open(user_data, 'w', encoding ='utf8') as f: json.dump(dts, f, indent=4)
        else: # Comeback for check the code bellow might have no use
            last_key = list(dts['menstrual_history'])[-1]
            remaining_key= int(last_key[4:])
            dt1= '{}{}'.format('date', remaining_key + 1)
            dt2= '{}{}'.format('date', remaining_key + 2)
            dt3= '{}{}'.format('date', remaining_key + 3)
            dt4 = '{}{}'.format('date', remaining_key + 4)

            menstr_histry= dts['menstrual_history']
            menstr_histry.update({dt1:date1, dt2:date2, dt3: date3, dt4: date4})
            new_di = {'menstrual_history': menstr_histry}
            
            with open(user_data, 'w', encoding ='utf8') as f: json.dump(new_di, f, indent=4)

    def save_preg_state(state):
        data= {"preg_state": state}
        dts = Amala.u_d_load()
        if dts is None:
            try:
                with open(user_data, 'w', encoding ='utf8') as f:
                    json.dump(data, f, indent=4)
            except:
                Directories.make_dirs()
                with open(user_data, 'w', encoding ='utf8') as f:
                    json.dump(data, f, indent=4)
        else:
            try:
                dts.update({'preg_state': state})
                with open(user_data, 'w', encoding ='utf8') as f:
                    json.dump(dts, f, indent=4)
            except KeyError:
                dts.update(data)
                with open(user_data, 'w', encoding ='utf8') as f:
                    json.dump(dts, f, indent=4)

    def update_last_menstrual_data(date):
        dts = Amala.u_d_load()
        lst = list(dts['menstrual_history'])[-1] # Gett the last item name
        dts['menstrual_history'].update({lst:date})
        with open(user_data, 'w', encoding ='utf8') as f: json.dump(dts, f, indent=4)

    def update_menstrual_data(date1, date2, date3, date4):
        dts = Amala.u_d_load()

        dt4 = list(dts['menstrual_history'])[-1]
        dt3 = list(dts['menstrual_history'])[-2]
        dt2 = list(dts['menstrual_history'])[-3]
        dt1 = list(dts['menstrual_history'])[-4]
                    
        menstr_histry= dts['menstrual_history']
        menstr_histry.update({dt1:date1, dt2:date2, dt3: date3, dt4: date4})
        dts.update({'menstrual_history': menstr_histry})
        with open(user_data, 'w', encoding ='utf8') as f: json.dump(dts, f, indent=4)

    def auto_add_menstry_day():
        dts = Amala.u_d_load()
        if dts is None:
            return '0'
        else:
            try:
                dt4 = list(dts['menstrual_history'])[-1]
                dt3 = list(dts['menstrual_history'])[-2]
                dt2 = list(dts['menstrual_history'])[-3]
                dt1 = list(dts['menstrual_history'])[-4]
        
                d0 = datetime.strptime(dts['menstrual_history'][dt1], "%Y-%m-%d")
                d1 = datetime.strptime(dts['menstrual_history'][dt2], "%Y-%m-%d")
                d2 = datetime.strptime(dts['menstrual_history'][dt3], "%Y-%m-%d")
                d3 = datetime.strptime(dts['menstrual_history'][dt4],"%Y-%m-%d")   
            
                dr0=d1-d0
                dr1=d2-d1
                dr2=d3-d2
                range =int((dr0.days+dr1.days+dr2.days)/3)  
                tdy = datetime.strptime(str(date.today()), "%Y-%m-%d")
                dys = (tdy - d3).days
                if dys > range:
                    #### Automatically adds next period day basing on range
                    new_date=d3 + timedelta(days=int(range))
            
                    last_key = list(dts['menstrual_history'])[-1]
                    remaining_key= int(last_key[4:])
                    dt1= '{}{}'.format('date', remaining_key + 1)
                
                    menstr_histry= dts['menstrual_history']
                    menstr_histry.update({dt1:new_date.strftime("%Y-%m-%d")})
                    dts.update({'menstrual_history': menstr_histry})
                    with open(user_data, 'w', encoding ='utf8') as f:
                        json.dump(dts, f, indent=4)
                return f'{dys}'
            except KeyError:
                return '0'
            
    def range():
        dts = Amala.u_d_load()
        try:
            dt4 = list(dts['menstrual_history'])[-1]
            dt3 = list(dts['menstrual_history'])[-2]
            dt2 = list(dts['menstrual_history'])[-3]
            dt1 = list(dts['menstrual_history'])[-4]
    
            d0 = datetime.strptime(dts['menstrual_history'][dt1], "%Y-%m-%d")
            d1 = datetime.strptime(dts['menstrual_history'][dt2], "%Y-%m-%d")
            d2 = datetime.strptime(dts['menstrual_history'][dt3], "%Y-%m-%d")
            d3 = datetime.strptime(dts['menstrual_history'][dt4],"%Y-%m-%d")     
        
            dr0=d1-d0
            dr1=d2-d1
            dr2=d3-d2
            range =int((dr0.days+dr1.days+dr2.days)/3)
            return range
        except:
            return 'No data added'