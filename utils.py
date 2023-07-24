import pandas as pd
from pyarabic.araby import strip_tashkeel, tokenize
import string
import arabicstopwords.arabicstopwords as stp

def justify_date(df):
    weekdays=[]
    days=[]
    months=[]
    years=[]
    times=[]
    for item in df['date']:
        date,time=item.split('-')
        weekday,day,month,year=date.split()
        time=time.strip()
        weekdays.append(weekday)  
        days.append(day)
        months.append(month)
        years.append(year)
        times.append(time)
    df["weekday"]=weekdays
    df["day"]=days
    df["month"]=months
    df["year"]=year
    df["time"]=times


    # Convert the 'time' column to datetime format & 
    # Extract the hour from the 'time' column
    df['hour'] =  pd.to_datetime(df['time']).dt.hour





def preprocess_arabic_text(text):
    # Tokenization
    tokens = tokenize(text)

    # Remove punctuation and non-Arabic characters
    arabic_tokens = [token for token in tokens if all(c not in string.punctuation for c in token)]

    # Remove diacritics (Tashkeel)
    stripped_tokens = [strip_tashkeel(token) for token in arabic_tokens]
    arabic_stop_words =set(stp.stopwords_list())

   # Remove Arabic stop words
    cleaned_tokens = [token for token in stripped_tokens if token not in arabic_stop_words]

    return cleaned_tokens




 

   

    