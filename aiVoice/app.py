from flask import Flask,request
import spacy
import pickle
import re
import xgboost
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello</p>"

with open('nlu_model_2', 'rb') as f:
        model = pickle.load(f)

nlp = spacy.load("en_core_web_sm")

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

# fetch time from text
def add_12_hours(time_string):
    time_format = "%H:%M"  
    time_obj = datetime.strptime(time_string, time_format)

    new_time_obj = time_obj + timedelta(hours=12)
    new_time_string = new_time_obj.strftime(time_format)

    return new_time_string

def getTime(text):
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

# fetch volume data from text
def getVolume(text):
    
    volumeRE = re.compile(r'[bB][yY]\s*\d{1,}|[tT][oO]\s*\d{1,}|\d{1,}')
    list = []
    try:
        volume = volumeRE.search(text).group()
        doc = nlp(volume)    
        for token in doc:
            list.append(token.text)
    except:
        list.append("by")
        list.append("10")
    if len(list) == 1:
        temp = ["to"]
        temp.append(list[0])
        list = temp
    return list

# fetch emailID from text
def getEmail(text):
    emailRE = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    try:
        email = emailRE.search(text).group()
        print(email)
        return str(email)
    except:
        return "No email found"

# get tile data from text
def getTile(text):
    t = ""
    for i in text:
        if(i=='-'):
            continue
        t += i
    text = t
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

def getApp(text):
    t = ""
    for i in text:
        if(i=='-'):
            continue
        t += i
    text = t
    apps = {
        'whatsapp':['whatsapp','whats app','whats','whats-app','whats app'],
        'facebook':['facebook','face book','face-book','face book'],
        'instagram':['instagram','insta gram','insta','insta-gram','insta gram'],
        'twitter':['twitter','twit ter','twit-ter','twit ter'],
        'snapchat':['snapchat','snap chat','snap-chat','snap chat'],
        'linkedin':['linkedin','linked in','linked-in','linked in'],
        'youtube':['youtube','you','you tube','you-tube','you tube'],
        'spotify':['spotify','spoti fy','spoti-fy','spoti fy'],
        'netflix':['netflix','net flix','net-flix','net flix'],
        'amazon':['amazon','ama zon','ama-zon','ama zon'],
        'flipkart':['flipkart','flip kart','flip-kart','flip kart'],
        'paytm':['paytm','pay tm','pay-tm','pay tm'],
        'zomato':['zomato','zomato','zomato','zomato'],
        'swiggy':['swiggy','swig gy','swig-gy','swig gy'],
        'ola':['ola','ola','ola','ola'],
        'uber':['uber','uber','uber','uber'],
        'google':['google','google','google','google'],
        'chrome':['chrome','chrome','chrome','chrome'],
        'firefox':['firefox','firefox','firefox','firefox'],
        'safari':['safari','safari','safari','safari'],
        'opera':['opera','opera','opera','opera'],
        'microsoft':['microsoft','microsoft','microsoft','microsoft'],
        'word':['word','word','word','word'],
        'settings':['settings','settings','settings','settings'],
        'calculator':['calculator','calculator','calculator','calculator'],
        'camera':['camera','camera','camera','camera'],
        'gallery':['gallery','gallery','gallery','gallery','photos','photos','photos','photos'],
        'clock':['clock','clock','clock','clock'],
        'calendar':['calendar'],
        'contacts':['contacts'],
        'messages':['messages',],
        'phone':['phone','phone','phone','phone'],
        'gmail':['gmail','gmail','gmail','gmail'],
        'maps':['maps','maps','maps','maps'],
        'drive':['drive','drive','drive','drive'],
        'files':['files','files','files','files'],
        'music':['music','music','music','music'],
        'playstore':['playstore','playstore','playstore','playstore'],
        'playmusic':['playmusic','playmusic','playmusic','playmusic'],
        'playmovies':['playmovies','playmovies','playmovies','playmovies'],
        'playgames':['playgames','playgames','playgames','playgames'],
        'playbooks':['playbooks','playbooks','playbooks','playbooks'],
        'playnews':['playnews','playnews','playnews','playnews'],

    }
    doc = nlp(text)
    print("hello")
    for token in doc:
        
        print(token.text)
        for key in apps:
            
            if token.text in apps[key]:
                return key
    return "No app found"

def response(intent,intentVal,extraVal,res):
    return {'intent':intent,'intentVal':intentVal,'extraVal':extraVal,'response':res}

@app.route('/getIntent',methods=['POST'])
def getIntent():
    text = request.form.get('text')
    text = text.lower()
    prediction = model.predict([text])[0]
    intent = labels[prediction]
    print(intent)
    if(intent=='alarm_set'):
        time = getTime(text)
        return response(intent,time,None,"Alarm is set for "+time),201
    elif(intent=='alarm_remove'):
        time = getTime(text)
        return response(intent,time,None,"Alarm is removed for "+time),201
    elif(intent=='audio_volume_down'):
        volume = getVolume(text)
        return response(intent,volume[1],volume[0],"Volume is decreased "+ volume[0] + " " +volume[1]),201
    elif(intent=='audio_volume_up'):
        volume = getVolume(text)
        return response(intent,volume[1],volume[0],"Volume is increased "+ volume[0] + " " +volume[1]),201
    elif(intent=='audio_volume_mute'):
        doc = nlp(text)
        for token in doc:
            if token.text=="set":
                vol = getVolume(text)
                return response("audio_volume_up",vol[1],vol[0],"Volume is set "+ vol[0] + " " +vol[1]),201
        return response(intent,"0","to","Volume is muted"),201
    elif(intent=="datetime_query"):
        return response(intent,None,None,"Current time is "),201
    elif(intent=="email_querycontact"):
        phNo = getPhoneNumber(text)
        return response(intent,phNo,None,"Phone number is "+phNo),201
    elif(intent=="email_sendemail"):
        emial = getEmail(text)
        return response(intent,emial,None,"send email to "+emial),201
    elif(intent=="tile_on"):    
        tile = getTile(text)
        return response(intent,tile,"on","Turned on "+tile),201
    elif(intent=="tile_off"):
        tile = getTile(text)
        return response(intent,tile,"off","Turned off "+tile),201
    elif(intent=="open_app"):
        app = getApp(text)
        return response(intent,app,None,"Opened "+app),201
    else:
        return response(intent,None,None,"Sorry I didn't get that"),201
        
# print(getIntent("set alarm for 5:30 pm"))