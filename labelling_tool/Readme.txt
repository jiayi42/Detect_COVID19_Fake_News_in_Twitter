download raw offline data 
(done by Twitter dataflow by Kafka performed in Docker deployed in Kubernetes in Real time embedded system course https://github.com/asuprem/edna/tree/master/setup/Part%205%20-%20An%20EDNA%20Job%20on%20Kubernetes)

Set the path to the directory with gz file in ChainedProcess.py
run ChainedProcess.py

Please go to your google account and apply for the fact check api key 
place the key in payload in the code to link the api

In mac, use the following command to start labelling your data and make sure your computer not to be dormant or without Internet connection

also please set the month you want to label

OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES python RTfactcheck_api.py

please be patient to wait for the labeling process

you get your labeled data json file for the month you want to label

segment it into different period by running process.py

put the each period files into your google drive and start train your data. Enjoy it!