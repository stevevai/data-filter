# -*- coding: utf-8 -*-
#import re
#filter_ts = re.compile(r'"ts":(\d+\.?\d+)?')
#filter_open = re.compile(r'"open":(\d+\.?\d+)?')
#filter_close = re.compile(r'"close":(\d+\.?\d+)?')
#filter_low = re.compile(r'"low":(\d+\.?\d+)?')
#filter_amount = re.compile(r'"amount":(\d+\.?\d+)?')
import pandas as pd
import json
def data_filter(file_name):
    file = open(file_name)
    file_list = file.read().split("}{")
    file_list = ["{"+x+"}" for i,x in enumerate(file_list) if i!=0 and i!=len(file_list)]
    data = pd.DataFrame()
    for i, f in enumerate(file_list):
        if "data" in f:
            try:
                file_pandas = pd.DataFrame(json.loads(f)["data"],\
                                  index = range(1),\
                                  columns=['open','close','low','amount'])
            except:
                continue
        elif "tick" in f:
            try:
                file_pandas = pd.DataFrame(json.loads(f)["tick"],\
                      index = range(1),\
                      columns=['open','close','low','amount'])
            except:
                continue
        else:
            continue
        file_pandas['ts'] = json.loads(f)["ts"]
        file_pandas = file_pandas.reindex(columns=['ts','open','close','low','amount'])
        data = data.append(file_pandas)
    data.reset_index(inplace=True)    
    del data["index"]
    data.to_csv(file_name.replace(".txt","")+".csv")
data_filter("market_detail.txt")  
data_filter("kline.txt")  
