import requests
from bs4 import BeautifulSoup

from nltk.corpus import stopwords
from textblob import TextBlob

import pandas as pd
#import matplotlib.pyplot as plt


def getUrlText(url_lst):
    """
    url_lst - List of URLs to be processed
    Will return list of strings(text from the URLs)
    """
    
    #Initialising array for return
    ret_text = []
    
    for url in url_lst:
        
        print(url)
        
        #Get text from Url
        r = requests.get(url)
        html_code = r.text
        
        #Format the text for extraction
        soup = BeautifulSoup(html_code, "lxml")
        
        for script in soup(["script", "style"]):
            script.extract()
        
        ret_text.append(soup.get_text())
    
    assert len(url_lst) == len(ret_text)
    
    return ret_text


def getFrequentWords(text_lst):
    """
    text_lst - List of strings to be processed
    quart - Quartile for words
    Will return list of strings(text from the URLs)
    """
    #Intialsing list for dataframes
    df_con = []
    
    #Extracting words and getting count of the words and adding to a dataframe
    for t in text_lst:
        text = TextBlob(t)
        text = text.words.singularize()
        text = [t.lower() for t in text if t.isalnum()]
         
        stop_words = set(stopwords.words("english"))
        wordsFiltered = {}
        for w in text:
            if w not in stop_words:
                if w in wordsFiltered:
                    wordsFiltered[w] = wordsFiltered[w] +1
                else:
                    wordsFiltered[w] = 1
            
        df = pd.DataFrame(list(wordsFiltered.items()), columns= ['word', 
                          'counts'])
        df_con.append(df)
    
    assert len(df_con) == len(text_lst)
        
    #Combine all the URLs' frequently used words
    df_unfinal = pd.concat(df_con, axis =0)
    assert pd.notnull(df_unfinal).all().all()
    
    if df_unfinal.word.value_counts()[0] != 1:
        print("*****There are common words****")
        df_unfinal['counts'] = df_unfinal.groupby('word')['counts'].transform('sum')
        df_unfinal = df_unfinal.drop_duplicates(subset = 'word')
    
    assert df_unfinal.word.value_counts()[0] == 1

    quant= df_unfinal.quantile(0.8)
    df_final = df_unfinal[df_unfinal['counts']>quant.loc['counts']]
    
    assert df_final.word.dtype == object
    assert df_final.counts.dtype == 'int64'
    
    return df_final


url_lst = ['https://stackoverflow.com/questions/684171/how-to-re-import-an-updated-package-while-in-python-interpreter','https://stackoverflow.com/questions/12477823/calling-a-function-in-a-separate-file-in-python']
text_lst = getUrlText(url_lst)
df = getFrequentWords(text_lst)