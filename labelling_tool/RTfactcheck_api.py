# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 14:46:58 2020

@author: missp
"""
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import json
import requests
import ujson
import multiprocessing 
import eventlet
from pebble import ProcessPool

def fundation(query): 
    payload = {
    'key':  ,# please apply and use your own api key in google fact check api
    'query':query
    }
    url ='https://factchecktools.googleapis.com/v1alpha1/claims:search'
    response = requests.get(url,params=payload)
    if response.status_code == 200:
        result = json.loads(response.text)
 
        try:
            #topRating = result["claims"][0]
            # arbitrarily select top 1
            #claimReview = topRating["claimReview"][0]["textualRating"]
            #claimVal = "According to " + str(topRating["claimReview"][0]['publisher']['name'])+ " that claim is " + str(claimReview)
            checker_raw=[claims["claimReview"][0]["textualRating"].lower() for claims in result["claims"] if "Misleading" not in claims["claimReview"][0]["textualRating"]]
            prune=sum([ -1.0 if ('false' in check or 'fake' in check) else 0.5 if ('half true' in check) else 1 if ('true' in check) else 0 for check in checker_raw])/float(len(checker_raw)+1)
                    
            #print(checker_raw,prune)
            #print('============')
            return  prune        
        except:
            #print("No claim review field found.")
            return 0
    else:
        print('bad request')
        return 0
    
def FactCheck(query):
    if len(query.split())<=4:return 0
 
    querys=sent_tokenize(query)
    if len(querys)==1:
        return fundation(query)
    if len(querys)>1:
        a= fundation(query)
        if a!=0: 
            return a
        
        if len(querys)<=10:
            return sum([ fundation(que) for que in querys])
        else:
            return sum([ fundation(que) for que in querys[:10]])
    return 0
 
from multiprocessing import Pool   
def labelFactCheck(text_list):
    text_score =[]
    pp=len(text_list)
    i=0
    while i<pp-4:
        if i%40==0:
            print(str(i/float(pp)*100)+'%')
        #p = Pool(processes=4)

        #data = p.map(FactCheck, text_list[i:i+4])

        #p.close()

        with ProcessPool(max_workers=4) as pool:

            future = pool.map(FactCheck, text_list[i:i+4], timeout=20)

            data = list(future.result())
        ppd=data.copy()
        text_score += [(text,sc) for text,sc in zip(text_list[i:i+4],ppd)]
        i+=4
    if pp-i>0:
      with ProcessPool(max_workers=pp-i) as pool:

          future = pool.map(FactCheck, text_list[i:], timeout=20)

          data = list(future.result())
      ppd=data.copy()
      text_score += [(text,sc) for text,sc in zip(text_list[i:i],ppd)]
    text_score = [ (text_sc[0],0) if text_sc[1]>0 else (text_sc[0],1) if text_sc[1]<0 else (text_sc[0],-1) for text_sc in text_score]
    return text_score
 

TopicWord='''
ballot funding drug mail voter ad police voting fund budget tax nursing vote chloroquine hydroxychloroquine poll footage inmate payment dollar relief man prison support crime financial officer debt option faith muslim spending violence title million application package revenue payroll private proposal cut letter lawmaker stimulus enforcement safety increase polling legislation insurance unemployment white age county benefit employee healthy job student coverage outside colored payment essential hotel protection loan restaurant income adult layer color church cost food legal store kid mandate percent young covering wearer particle self short eviction gathering learning requirement center instruction attention room release leave cloth employer brain chinese lab travel cremation man clip alive lockdown ventilator funeral fatality mortality product supply bag woman quarantine british animal estimate message cause certificate equipment threat average capacity common droplet screenshot special influenza viral fear infected count outlet severe air bed factor site sign reporter billionaire daily body victim plastic fever'''
TopicWordlist= list(set(TopicWord.split()))
def filtercollector(texts):
   filterlist=[]
   for text in texts:
        no_k=True
        for keywords in TopicWordlist:
            if keywords in text:
               filterlist.append(text)
               no_k=False
               break
        if no_k: 
            if random.randint(1, 100)>=95:
               filterlist.append(text) 
   return filterlist 

with open('data03.json') as f:
  data = json.load(f)
label_data={}
import time,random
i=0
kak=0
try:
  for key  in data:
    st=time.time()
    #if  key<="03-11-19" or key>"03-16-00":continue
    text_list=data[key]["full_text"]
    print("start",'section time=',key)
    if len(text_list)>250:
        ol=len(text_list)
        text_list =filtercollector(text_list)
        
        #random.shuffle(text_list)
        if len(text_list)>500:
          random.shuffle(text_list)
          bound=max(len(text_list)//10,250)
          print("further key pruning",ol,'to',len(text_list),'to', bound)
          text_list = text_list[:bound]
        else:
          print("key  pruning",ol,'to',len(text_list))
        print("process",len(text_list))
    else:
        print("process",len(text_list))
    try:
        aa=labelFactCheck(text_list)
        kk=[]
        for a in aa:
            if a[1]!=-1:
                kk.append(a)
        label_data[key]=kk
        print('lable time=',round(time.time()-st,2),"process",len(text_list),"get",len(kk))
        print('')
    except Exception as e:
        print( "<p>Error: %s</p>" % str(e) )
        print('weird executions time=',round(time.time()-st,2))
        print('')
    if kak%6==0:

      with open('label_data03.json', 'w') as output_file:

        ujson.dump(label_data, output_file, indent=4, sort_keys=True)

    kak+=1

    

 

  with open('label_data0301.json', 'w') as output_file:

    ujson.dump(label_data, output_file, indent=4, sort_keys=True)
except:
  with open('label_data0301.json', 'w') as output_file:
    ujson.dump(label_data, output_file, indent=4, sort_keys=True)
'''


text_list= [
            "my boyfriend surprised me with a trip to atlanta to go see the cdc headquarters because i start my infectious disease epi masters program this year and it s my dream to be an id doctor for the cdc",
            "sather ladies and gentlemen, nih cdc just concocted a new health scare named after a mexican beer.",
            "cdc expects more cases of coronavirus in us after first incident in washington state",
            "first u. s. case of deadly coronavirus confirmed atlanta airport to begin screening passengers coronavirus atlanta hartsfieldjackson airport china",
            "but didnt they ban travel from some countries in africa few years ago due to ebola or something? did the cdc not recommend that?",
            "add to that the fact that the cdc is a private, for profit corporation not a government agency and owns over patents on vaccines and related products and procedures they make a ton of money on vaccines",
            "i ve just read on the cdc website that the coronavirus is ruled out as sars or mers. and the alert level is level. which means, don t cancel plans, but be proactive and cautious. as vegans, not eating fish or meat where the virus was first detected i think we will be ok",
            "coronavirus gets its name from crown like spikes on its surface cdc. corona is latin for crown. including the newly identified form of the virus, there are a total of seven coronaviruses that can infect humans. other well known coronaviruses include sars and mers.",
            "coronaviruses cause illness ranging from the common cold to more severe diseases such as pneumonia to middle east respiratory syndrome, known as mers, and severe acute respiratory syndrome, or sars.",
            "people have recently asked me where i get news on outbreaks like ncov. besides government sources, i always see what have written. they re the best in the business and both are canadians living abroad. teamcanada",
            "the current influenza outbreak numbers.",
            "cdc confirms first us case of coronavirus that has killed in china",
            "do disinfectants kill the coronavirus? yes, they can. the cdc suggests that anyone exposed to an infected patient clean all high touch surfaces, such as counters, tabletops, doorknobs, bathroom fixtures, toilets, phones, keyboards, tablets and bedside tables.",
            "the ultimate intention is that anyone in receipt of a centrelink payment will be involuntarily forced onto the card. and big banks are taking over the administration of it too. the cdc program violates human rights treaty obligations",
            "cleaning agents can include a household disinfectant with a label that says epa approved, according to the cdc. a homemade version can be made, using one tablespoon of bleach to one quart of water.",
            "cdc english statement taiwan timely identifies first imported case of sever special infectious pneumonia from wuhan, china through onboard quarantine central epidemic command center raises travel notice level for wuhan to level warning",
            "jogging tayu cdc",
            "well supposedly the cdc said the man is in good condition and came in himself after recognizing the symptoms. the good news is right now it seems that antibiotics help with the treatment of the virus, so deaths likely to happen where there is less attention to patients.",
            "signs and symptoms lassa fever cdc",
            "this is a matter of risk perception cdc estimates that so far this season there have been at least million flu illnesses,, hospitalizations and, deaths from flu.",
            "chinese coronavirus outbreak has reached u. s. shores, cdc says los angeles times",
            "first us case of wuhan coronavirus confirmed by cdc",
            "first patient with wuhan coronavirus is identified in the u. s.",
            "cdc adds health entry screenings at atlanta airport due to coronavirus",
            "study cdc s vaccine schedule may be harmful to children via",
            "first us case of wuhan coronavirus confirmed by cdc",
            "thank you. i am using who and cdc for official data.",
            "azhar dear adeel good morning. since i opened my cdc account the mkt is on decline and bears are active. any idea how long this trend will continue..? however i m enjoying my trading.",
            "the centers for disease control,, is monitoring the outbreak of a new coronavirus, ncov, in wuhan, china. cases are confirmed in thailand, japan and southkorea. the u. s. announced the first infection in a traveler returning from wuhan.",
            "momma ezer chick that s why i specifically looked up the cdc and nhs stats. i knew he d dismiss ppfa and guttmacher out of hand. but he seems to not understand how links to websites work...",
            "cdc first case of wuhan coronavirus confirmed in u. s. health",
            "u. s. airports to screen for chinese coronavirus",
            "sather cdc owns the patent for their lab created strain.",
            "cdc emergency meeting tomorrow",
            "u. s. confirms first case of deadly coronavirus, cdc to add entry health screening at atl",
            "newly developed tests achieve concordance on superbug strains from the cdc",
            "china was in the news, big time, today. this isn t a good thing in any arena.",
            "don t you mean h n and h n? i suggest, rather than relying upon any tw ttery med cal adv ce, folks just visit the cdc and read...",
            "vicki meek walker mamadeb truther tatvamasi ralph, you re still on that. you re stuck. it doesn t matter. and the fact that it was published by the cdc, makes your statement dubious at best the point was the content. it s clear, however that you can t grasp this, so, please, repeat your refrain, ad infinitum.",
            "yes. guidelines the fda and cdc offer info for medical pros to use good stewardahip to follow clinical guidelines when prescribing antibiotics",
            "first us case of wuhan coronavirus confirmed by cdc",
            "an estimated. m flu illness,, hospitalization, death in a flu season, widespreading in us states. us govt senators stay focused on americans, do something good for them. china wuhancoronavirus",
            "nonsense chief admits vaccines cause autism. says question not answered lied about main witness testimony or it would be common knowledge vaccines cause autism",
            "petition the cdc banned transgender, fetus, and other words in a new repressive crackdown. demand the health agency reverse course now",
            "seattle, tacoma is not, one of the airports that cdc has listed as screen ng sites for corona virus.",
            "cdc adds health entry screenings at atlanta airport due to coronavirus via wate news",
            "what, the cdc does not have a vaccine to inject people with yet? they will soon.",
            "coronavirus health officials announce first known us case",
            "cdc confirms first u. s. case of deadly china virus via",
            "oh great... cdc",
            "well, here we go. new protocols at work. masks... rural hospitals have no testing for this, only the cdc. my er is going to be flooded with scared people wanting to be tested and there is no test i can run. cdc on speed dial, huzzah night shift protect yourself, folks",
            "there are many myths about how to wash your hands properly so we talked to doctors to find out how long to wash them the best soap to use if hand sanitizer does the trick and more. cdc",
            "look at the table of injuries set up by hhs cdc for vaccine injuries. vaccine inserts vaccine injury cases where doctors and scientists agree on vaccine induced death. do a few hours of research on the hanna polling case. look at the lack of safety studies",
            "u can read what the cdc had to say about it",
            "so the cdc says there were only diagnosed cases of sars in the u. s. during that outbreak. wonder where the next case of this is going to be.",
            "the confirmed the first case of novel coronavirus ncov in the united states in the state of washington.",
            "cdc confirms first us case of coronavirus that has killed in china",
            "is testing available only at cdc or available to all hospitals?",
            "first us case of wuhan coronavirus confirmed by cdc",
            "vicki meek walker mamadeb truther tatvamasi they think the cdc is like the illuminati",
            "latest reported numbers for china coronavirus wuhancoronavirus ncov ncov",
            "wear face mask especially when you travelling wuhanvirus influenza wuhancoronavirus wuhanpneumonia",
            "first case of mystery coronavirus found in washington state cdc via",
            "hong kong, located right next to mainland but surprisingly having case of wuhancoronavirus and not imposing any effective preventive measures while the number of cases in china increases by hundred every few hours and other farther countries have confirmed cases as well",
            "the actual numbers could be x or x or even x worse. wuhanvirus wuhancoronavirus freehk policeterrorism policestate",
            "the standard was developed by osha? bottom line, healthcare workers are infected and the bbp standard isn t going to stop this virus. osha is going to depend on the cdc and who to provide guidance on protective measures.",
            "myanmar yangon has a direct flight to wuhan and it flies once a week by china eastern airlines. riskassessment wuhancoronavirus wuhanpneumonia",
            "uh oh, captainbananas mental debilitation has spread to others. someone call the cdc."
        ]
aa=labelFactCheck(text_list)
kk=[]
for a in aa:
    if a[1]!=-1:
        kk.append(a)
for k in kk:
    print(k)
    if k[1]==0:
        print('true')
    if k[1]==1:
        print('false')
    print('===')
'''
