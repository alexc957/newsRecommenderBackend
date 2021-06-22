from re import search
import pandas as pd 
from glob import glob
import json 
import spacy 
import es_core_news_md
import os 
from pathlib import Path
spacy_model = es_core_news_md.load()

data_path = "D:/Projects/graphql/Spanish news dataset sample/news*"  # path to the news store in json files 

filenames = glob(data_path)
print(len(filenames))
def process_text(text):
    """"
    metodo para eliminar stop words y puntuaciones 
    """
    doc = spacy_model(text.lower())
    result = []
    for token in doc:
        if token.text in spacy_model.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return " ".join(result)



def search_news(search="trump", num_items=300, category="politica"):
    """
    generar una lista con las noticas que contengan la palabra clave {search}

    """
    data_df = [] # uuid,title, text, text vector 
    for i,filename in enumerate(filenames):
        with open(filename, encoding='utf8') as file:
            data = json.load(file)
            if(search in data.get("text").lower()):
               # processed_text = process_text(data.get('text'))
                data_df.append(
                    {
                        "uuid":data.get("uuid"),
                        "title": data.get("title"),
                        "text": data.get("text"),
                        "text_vector": ";".join(spacy_model(data.get('text')).vector.astype(str)),
                        "category" : category
                        
                    }
                ) 
        if len(data_df)==num_items:
            break
    print('done')
    return data_df 

# obtener y generar un datagrame de noticas de Donald Trump 
data_df = search_news(search="trump", category="politica")
trump_df = pd.DataFrame(data_df)

# obtener y generar un datagrame de noticas de deportes

deportes_data = search_news(search="deporte", category="deportes")
deportes_df = pd.DataFrame(deportes_data)

# de futbol 
futbol_data = search_news(search="futbol", category = "deportes")
futbol_df = pd.DataFrame(futbol_data)



# de putin/rusia 
putin_data = search_news(search="putin", category="politica")
putin_df = pd.DataFrame(putin_data)


correa_data = pd.DataFrame( search_news(search="correa", category='politica'))
data =   pd.DataFrame(search_news(search="politica", category='politica'))
data1 = pd.DataFrame(search_news(search="clinton",category="politica"))
data2 = pd.DataFrame(search_news(search="obama", category="politica"))

data3 = pd.DataFrame( search_news(search='baloncesto',category='deportes') )
data4 = pd.DataFrame( search_news(search='farc',category='politica'))
data5 = pd.DataFrame( search_news(search='uribe',category='politica') )
data6 = pd.DataFrame( search_news(search='messi',category='deportes') )
data7 = pd.DataFrame( search_news(search='ronaldo',category='deportes') )
# concatenar los resultados 
news_df = pd.concat([trump_df, deportes_df,futbol_df, putin_df, correa_data,data,data1,data2, data3,data4, data5,data6,data7],ignore_index=True)
print(news_df.shape)
# eliminar duplicados 
news_df = news_df.drop_duplicates(subset=['uuid','title'], keep='first')
# guardar los resultados 
news_df.to_csv("NoticiasConVectoresV4.csv")