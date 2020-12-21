# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:40:30 2020

@author: missp
"""
st=[]
import json
 

 

with open('label_data03.json') as f:
  data = json.load(f)
 
key_list_all=[]
i=1
while i<=28:
 print(i,i+3)
 if i<7: 
    key_list_all.append(sum([data[key] for key in data  if key>="03-0"+str(i)+"-00" and key<"03-0"+str(i+3)+"-00"],[]))
 elif i==7: 
    key_list_all.append(sum([data[key] for key in data  if key>="03-0"+str(i)+"-00" and key<"03-"+str(i+3)+"-00"],[]))
 elif i>7 and i<28:
    key_list_all.append(sum([data[key] for key in data  if key>="03-"+str(i)+"-00" and key<"03-"+str(i+3)+"-00"],[]))
 else:
    key_list_all.append(sum([data[key] for key in data  if key>="03-"+str(i)+"-00"  ],[]))
 

 i+=3

for i in range(len(key_list_all)):
  statistics=[0,0]
  for d in key_list_all[i]:
      statistics[d[1]]+=1
  print(statistics)
  st.append(statistics[:])
  with open('label_data03_'+str(i)+'_processed.json', 'w') as output_file:
    json.dump(key_list_all[i], output_file, indent=4, sort_keys=True)
with open('label_data03_st.json', 'w') as output_file:
  json.dump(st, output_file, indent=4, sort_keys=True)
for s in st:
    print(s[0],s[1])