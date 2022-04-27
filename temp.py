from flask import Flask,render_template,request
from pandas.tseries.offsets import DateOffset
import pickle
import pandas as pd
from flask_apscheduler import APScheduler
from datetime import datetime
import numpy as np
import re


app=Flask(__name__)
scheduler = APScheduler()

model=pickle.load(open("Nov2k19.pkl","rb"))

data=pd.read_csv("C:/Users/Rushikesh/Final Year Project/New folder/Nov2k19.csv")
data["date_time"]=pd.to_datetime(data["date_time"])
data.set_index("date_time",inplace=True)
data.drop("Unnamed: 0",axis=1,inplace=True)
start_date=data.index[-1]


def change_date(date):
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})','\\3-\\2-\\1',date)



@app.route("/")

def home():
    return render_template("index.html")


@app.route("/Refresh",methods=["GET","POST"])


def predict():
    global data,start
    
    #print(datetime.today())
    #print(data.index)
    #print(data.shape)
    #print(data.tail(1).index[0])
    future_dates = pd.date_range(data.tail(1).index[0], periods=6, freq='H')
    #future_series = pd.DataFrame([np.nan for i in range(5)], index=future_index,columns=["tempC"])
    future_dataset=pd.DataFrame(index=future_dates[1:],columns=data.columns)
    print(future_dates)
    print(future_dataset)
    data=pd.concat([data,future_dataset])
    #start_date=future_dataset.index[0]
    end_date=future_dataset.index[-1] 
    print(start_date)
    print(end_date)
    data['forecast'] = model.predict(start = start_date, end = end_date, dynamic= True)
    p=model.predict(start=start_date, end=end_date, dynamic= True)
    print(p)
   
    val=-5
    print(round(p[val],2))
    print(round(p[val+1],2))
    print(round(p[val+2],2))
    print(round(p[val+3],2))
    print(round(p[val+4],2))
    print(str(p.index[val])[10:16])
    print(str(p.index[val+1])[10:16])
    print(str(p.index[val+2])[10:16])
    print(str(p.index[val+3])[10:16])
    print(str(p.index[val+4])[10:16])
    print(str(p.index[val])[0:10])
    print(change_date(str(p.index[val])[0:10]))
         
    
        
        
    return render_template('index.html',forcast1=f"{round(p[val],2)}",forcast2=f"{round(p[val+1],2)}",
                               forcast3=f"{round(p[val+2],2)}",forcast4=f"{round(p[val+3],2)}",forcast5=f"{round(p[val+4],2)}",
                               day=f"{change_date(str(p.index[val])[0:10])}",time1=f"{str(p.index[val])[10:16]}",time2=f"{str(p.index[val+1])[10:16]}",
                               time3=f"{str(p.index[val+2])[10:16]}",time4=f"{str(p.index[val+3])[10:16]}",time5=f"{str(p.index[val+4])[10:16]}")

if __name__=="__main__":
    scheduler.add_job(id="Scheduled task", func = predict, trigger = "interval",seconds =10)
    scheduler.start()
    app.run(debug=True)
    
