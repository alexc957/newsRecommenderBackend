import es_core_news_md
from articles.models import Article
import pandas as pd 
spacy_model = es_core_news_md.load()
# este script guarda los articulos en la base 
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

def save_elcomercio_news():
    #model = spacy.load('es_core_news_md')

    elcomercio_df = pd.read_excel('scripts/corpus_elcomercio.xlsx') 
    for index, row in elcomercio_df.iterrows():
        #processed_text = process_text(row['Texto'])
        Article.objects.create(
            title = row['Noticia'],
            summary = row['Texto'],
            category = "COVID19",
            date_uploaded = row['Fecha'].date(),
            text_vector = ';'.join(spacy_model(row['Texto']).vector.astype(str))
        )
    print('Done')


def save_news_to_db():
    # guarda los articulos generados en calculate_text_vectors.py en la base 
    df = pd.read_csv('scripts/NoticiasConVectores.csv')
    print(df.shape)
    for index,row in df.iterrows():
        Article.objects.create(
            title = row['title'],
            summary = row['text'],
            category = row["category"],
            text_vector = row['text_vector'],
        )

    print("done")


#%% 

# %%
