from recommendations.Recommender import Recommender

def crear_relaciones():
    rec = Recommender(threshold=0.86)
    rec.find_similars_articles_in_all_articles()