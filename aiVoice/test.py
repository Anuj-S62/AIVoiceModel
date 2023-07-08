import spacy
import flask
import xgboost
nlp = spacy.load("en_core_web_sm")
import pickle
import re
from datetime import datetime, timedelta



labels = {}
labels[0] =   "alarm_query"
labels[1] =   "alarm_remove"
labels[2] =   "alarm_set"
labels[3] =   "audio_volume_down"
labels[4] =   "audio_volume_mute"
labels[5] =   "audio_volume_other"
labels[6] =   "audio_volume_up"
labels[7] =   "calendar_query"
labels[8] =   "calendar_remove"
labels[9] =   "calendar_set"
labels[10] = 	"cooking_query"
labels[11] = 	"cooking_recipe"
labels[12] = 	"datetime_convert"
labels[13] = 	"datetime_query"
labels[14] = 	"email_addcontact"
labels[15] = 	"email_query"
labels[16] = 	"email_querycontact"
labels[17] = 	"email_sendemail"
labels[18] = 	"general_affirm"
labels[19] = 	"general_commandstop"
labels[20] = 	"general_confirm"
labels[21] = 	"general_dontcare"
labels[22] = 	"general_explain"
labels[23] = 	"general_greet"
labels[24] = 	"general_joke"
labels[25] = 	"general_negate"
labels[26] = 	"general_praise"
labels[27] = 	"general_quirky"
labels[28] = 	"general_repeat"
labels[29] = 	"iot_cleaning"
labels[30] = 	"iot_coffee"
labels[31] = 	"iot_hue_lightchange"
labels[32] = 	"iot_hue_lightdim"
labels[33] = 	"iot_hue_lightoff"
labels[34] = 	"iot_hue_lighton"
labels[35] = 	"iot_hue_lightup"
labels[36] = 	"tile_off"
labels[37] = 	"tile_on"
labels[38] = 	"lists_createoradd"
labels[39] = 	"lists_query"
labels[40] = 	"lists_remove"
labels[41] = 	"music_dislikeness"
labels[42] = 	"music_likeness"
labels[43] = 	"music_query"
labels[44] = 	"music_settings"
labels[45] = 	"news_query"
labels[46] = 	"play_audiobook"
labels[47] = 	"open_app"
labels[48] = 	"play_music"
labels[49] = 	"play_podcasts"
labels[50] = 	"play_radio"
labels[51] = 	"qa_currency"
labels[52] = 	"qa_definition"
labels[53] = 	"qa_factoid"
labels[54] = 	"qa_maths"
labels[55] = 	"qa_stock"
labels[56] = 	"recommendation_events"
labels[57] = 	"recommendation_locations"
labels[58] = 	"recommendation_movies"
labels[59] = 	"social_post"
labels[60] = 	"social_query"
labels[61] = 	"takeaway_order"
labels[62] = 	"takeaway_query"
labels[63] = 	"transport_query"
labels[64] = 	"transport_taxi"
labels[65] = 	"transport_ticket"
labels[66] = 	"transport_traffic"
labels[67] = 	"weather_query"

with open('nlu_model_2', 'rb') as f:
    clf = pickle.load(f)

print(labels[clf.predict(["what's the time"])[0]])
print(labels[clf.predict(["set an alarm for 5 p.m."])[0]])
print(labels[clf.predict(["remove alarm for 5 p.m."])[0]])
print(labels[clf.predict(["what time"])[0]])
print(labels[clf.predict(["call 9568 850 745"])[0]])
print(labels[clf.predict(["write a mail to abs@gmail.com"])[0]])
print(labels[clf.predict(["turn off location"])[0]])


def add_12_hours(time_string):
    time_format = "%H:%M"  
    time_obj = datetime.strptime(time_string, time_format)

    new_time_obj = time_obj + timedelta(hours=12)
    new_time_string = new_time_obj.strftime(time_format)

    return new_time_string

def setAlarm(text):
    timeRE = re.compile(r'\d{1,2}:\d{1,2}\s*[apAP]\.*[mM]\.*')
    try:
        time = timeRE.search(text).group()
        # print(time)
        flag = False
        for i in time:
            # print(i)
            if(i=='p'):
                print("hello")
                flag = True
        s = ""
        for i in time:
            if i==" ":
                break
            s+=i
        if(flag==True):
            time = add_12_hours(s)
        else:
            time = s
        return str(time)
    except:
        return "No time found"

def getVolume(text):
    
    volumeRE = re.compile(r'[bB][yY]\s*\d{1,}|[tT][oO]\s*\d{1,}')
    list = []
    try:
        volume = volumeRE.search(text).group()
        doc = nlp(volume)    
        for token in doc:
            list.append(token.text)
    except:
        list.append("by")
        list.append("10")
    return {list[0]:list[1]}

def getPhoneNumber(text):
    phoneRE = re.compile(r'\d{1,}\s*\d{1,}\s*\d{1,}')
    try:
        phone = phoneRE.search(text).group()
        pNo = ""
        for i in range(len(phone)):
            if phone[i] == ' ':
                continue
            else:
                pNo += phone[i]
        return str(pNo)
    except:
        return "No phone number found"

def getEmail(text):
    emailRE = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    try:
        email = emailRE.search(text).group()
        print(email)
        return str(email)
    except:
        return "No email found"        

def getTile(text):
    tiles = {'data':['mobile data','data','mobile','internet'],
            'wifi':['wifi','wi-fi'],
            'bluetooth':['bluetooth','bluetooh'],
            'hotspot':['hotspot','hot spot','hot-s'],
            'airplane' : ['airplane','airplane mode','aeroplane','aeroplane mode','aero plane','aero plane mode','aero-plane','aero-plane mode','aero'],
            'flashlight':['torch','flashlight','flash','light'],
            'location':['location','location services','location service','location on','location off','location mode','location settings','location setting','location mode','location modes','location']
            }
    doc = nlp(text)
    for token in doc:
        for key in tiles:
            if token.text in tiles[key]:
                return key
    return "No tile found"


# setAlarm('remove alarm for 30 p.m.')
# print(getPhoneNumber('call 9568 850 745'))
# print(getEmail('write a mail to abs@students.iitmandi.ac.in'))
print(getTile('turn off location'))
print(setAlarm("set an alarm for 5:30 a.m."))

print(add_12_hours("5:30"))
