
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import os 
import csv
from datetime import datetime
col_names =  ["RTT"]
df  = pd.DataFrame(columns = col_names)


# In[2]:


import subprocess
import re
def ping_sever(host):
    v = "| while read pong; do echo '$(date): $pong'; done"
    ping = subprocess.Popen(
        ["ping", "-c", "5", host, ],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE )

    out, error = ping.communicate()
    output = out.decode('utf-8')
    return output.splitlines()
line = ping_sever("www.google.com")


# In[3]:


rtt_arr = []
p_loss = []
p_transmitted =[]
p_received =[]


# In[4]:


for idx in range(len(line)-1):
    m = re.search(r'(?<=time=).*?(?=ms)', line[idx])
    if m:
        rtt_arr.append(m.group())
        l = re.search(r'(?<=received,).*?(?=packet)', line[idx+3])
        p = re.search(r'(?<=,).*?(?=packets)', line[idx+3])
        r = re.search(r'(?<=transmitted,).*?(?=received,)' , line[idx+3])
        if l:
            for i in range(int(p.group().strip(" "))):
                        p_transmitted.append(p.group().strip(" "))
                        p_loss.append(l.group().strip(" "))
                        p_received.append(r.group()[1])


# In[5]:


df["RTT"] = rtt_arr
df["Packet Loss"] = p_loss 
df["Packet transmitted "] = p_transmitted 
df["Packet received"] = p_received
df.head(3)


# In[6]:


#Ceate a csv file for future uses out of the fetched data 
headers=["RTT", "PacketLoss", "PacketTransmitted", "PacketReceived"]
def create_csv_file(data=None):
    if data is None:
        data = headers
    data = headers
    if not os.path.exists("output.csv"):
        with open('output.csv', 'w', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(data)
create_csv_file()


# In[7]:


with open('output.csv', 'a') as f:
    dd = df
    dd.to_csv(f, header=False, index=False)

