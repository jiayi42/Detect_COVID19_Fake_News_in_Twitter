import glob, gzip, ujson
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import re
from nltk.tokenize import WordPunctTokenizer
tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))
import os
from collections import defaultdict
files = glob.glob('/Users/mason/Desktop/2020-03/*.gz')# download the offline data and set the path to the directory with gz files
each_hour_data=defaultdict(dict)
#print(files)
def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    
    letters_only = re.sub("[^a-zA-Z.?,]", " ", clean)
    lower_case = letters_only.lower()
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip().replace(" .",'.').replace(" ?",'?').replace(" ,",','),text



import time



for f in files:
    print(f,'start')
    key=f.split('-2020-')[1].replace('.json.gz','')
    print(key)
    each_hour_data[key]['full_text']=[]
    start=time.time()
    with gzip.open(f, "r") as compressed_gzip_reader:
         for line in compressed_gzip_reader:
                json_line = ujson.loads(line)
                clean_tweet,original_tweet=tweet_cleaner(json_line['full_text'])
                if not clean_tweet.startswith('rt') and not clean_tweet.startswith('RT'):
                  #print(clean_tweet)
                  #print(original_tweet)
                  #print('========') 
                  if re.search("[^a-zA-Z]", clean_tweet) and 3<=len(clean_tweet.split())<=100: 
                    each_hour_data[key]['full_text'].append(clean_tweet)
         #for ele in each_hour_data[key]['full_text']: 
         #  print(ele)
         #  print('=====')
    print(len(each_hour_data[key]['full_text']))
    #break
    print(f,'clean ok','spend',round(time.time()-start,2),'secs\n')
#print([ len(each_hour_data[d]['full_text']) for d in each_hour_data.keys()])
    
with open('data.json', 'w') as output_file:
            ujson.dump(each_hour_data, output_file, indent=4, sort_keys=True)

