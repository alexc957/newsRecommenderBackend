import pandas as pd 
from glob import glob
import json 
import spacy 
import es_core_news_md
import os 
from pathlib import Path
spacy_model = es_core_news_md.load()

data_path = "D:/Projects/djngo-graphql/Spanish news dataset sample/news*"  # path to the news store in json files 

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
                processed_text = process_text(data.get('text'))
                data_df.append(
                    {
                        "uuid":data.get("uuid"),
                        "title": data.get("title"),
                        "text": data.get("text"),
                        "text_vector": ";".join(spacy_model(processed_text).vector.astype(str)),
                        "category" : category
                        
                    }
                ) 
        if len(data_df)==num_items:
            break
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
# concatenar los resultados 
news_df = pd.concat([trump_df, deportes_df,futbol_df, putin_df])

# eliminar duplicados 
news_df = news_df.drop_duplicates(subset=['uuid','title'], keep='first')
# guardar los resultados 
news_df.to_csv("NoticiasConVectores.csv")