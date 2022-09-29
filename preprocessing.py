import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
import datetime as dt
from sklearn.model_selection import train_test_split
import numpy as np
# data is that 23 feature one



def season_datetime_fix(data):
    """function creates datetime features. faeatures- a date dummy as if date is starting from begginning of years  
    match week, match day of saeason, 
    """
    data[['week','dayofseason','date_dummy']]= "" 
    data.datetime=pd.to_datetime(data.datetime).dt.date
    for season in data.season.unique():
        season_data=data[data['season']==season]
        start=season_data.iloc[0].datetime
        year=start.year
        delta=start-dt.date(year,1,1)
        season_data['date_dummy']=season_data.datetime-delta
        season_data.week=season_data.date_dummy.apply(lambda x:x.isocalendar()[1])
        season_data.dayofseason=season_data.date_dummy.apply(lambda x: x.timetuple().tm_yday)
        data[data.season==season]=season_data
    data['day']=data['datetime'].apply(lambda x:x.isoweekday())
    return data


def process_reg(data_path):
    "features added aand rmoved and asplit the data  perticuarly for a regression setup"

    data=pd.read_csv(data_path,encoding='windows-1254')
    data.columns=[i.lower() for i in data.columns]
    data.drop(data.loc[data['season'].str.contains('1993|1994|1995|1996|1997|1998|1999',regex=True)].index,inplace=True)
    data=season_datetime_fix(data)
    data['week']=data.week.astype(int)
    data['dayofseason']=data.dayofseason.astype(int)
    data['fthg']=data['fthg'].astype(float)
    data['ftag']=data['ftag'].astype(float)
    data.sort_values('date_dummy',inplace=True) 
    return data


