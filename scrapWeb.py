import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import matplotlib.pyplot as plt

def getMostUsedWords(url_lst):
    
    df_final = []
    
    for url in url_lst:
        print(url)
        r = requests.get(url)
        html_code = r.text#converting into text
        
        #creatingBeautifulsoupobject
        soup = BeautifulSoup(html_code, "lxml")
        
        #remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        #get the text from object
        text1 = soup.get_text()
        
        #Tokenizes words from text
        text = word_tokenize(text1)
        text = [t.lower() for t in text if t.isalnum()  ]
        
        #Filtering out the stopwords
        stop_words = set(stopwords.words("english"))
        wordsFiltered = {}
        for w in text:
            if w not in stop_words:
                if w in wordsFiltered:
                    wordsFiltered[w] = wordsFiltered[w] +1
                else:
                    wordsFiltered[w] = 1
        
        df = pd.DataFrame(list(wordsFiltered.items()), columns= ['Word', 'Count'])
        
#        #Plotting histogram
#        _ = df.plot(kind = 'hist')
#        _ = plt.show()
#        
#        _ = df.boxplot(column = 'Count')
#        _ = plt.show()
        
        quant= df.quantile(0.99)
        filter_df = df[df['Count']>quant.loc['Count']]
        
        df_final.append(filter_df)
    
    df_final = pd.concat(df_final)
    
    return df_final

