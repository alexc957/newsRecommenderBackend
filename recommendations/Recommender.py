from django.contrib.auth import get_user_model
from sklearn.metrics.pairwise import cosine_similarity
from collector.models import Vote
from articles.models import Article, SimilarArticle
from .models import Recommendation
import time 

import random

class Recommender:

    def __init__(self, threshold=0.99):
        self.threshold = threshold
        

    def cosine_similarity_score(self,x,y):
        y = np.array(y.split(';')).astype(float)
        x = np.array(x.split(';')).astype(float)
        # print(y.shape)
        # print(x.shape)
        try:

            similarity_score = cosine_similarity([x], [y])
        except ValueError:
            return 0

        if similarity_score.size > 0:
            return similarity_score[0, 0]
        return 0


    def find_similars_articles_in_all_articles(self):
        all_articles = Article.objects.all()
        t0 = time.time()
        length = len(all_articles)
        for idx in range(0, length):
            print(f"processing {idx+1} of {length} ")
            for article_a in all_articles:
                if all_articles[idx] != article_a.id:
                    sim_score = self.cosine_similarity_score(
                        all_articles[idx].text_vector, article_a.text_vector)
                    similar_article = SimilarArticle.objects.filter(
                        principal_article=all_articles[idx], related_article=article_a).first()

                    if sim_score > self.threshold and not similar_article:
                        #print("creating similar article")
                        SimilarArticle.objects.create(
                            principal_article=all_articles[idx],
                            related_article=article_a,
                            score=similar_article,
                        )
        print("done")
        print(f'total time: {(time.time() - t0)/60} minutes')


    def generate_recommendations(self, user):
        """
            Genera recomendaciones en base al votos/perfil de usuario 
        """
        votes_made_by_user = Vote.objects.filter(user=user, liked=True)

        articles_liked_by_user = [vote.article for vote in votes_made_by_user]
        for article_liked in articles_liked_by_user:
            for similar_article in article_liked.similar_articles.all()[:5]:
                recommendation = Recommendation.objects.filter(
                    article=similar_article.related_article, user=user).first()
                if not recommendation:
                    Recommendation.objects.create(
                        score=similar_article.score,
                        user=user,
                        article=similar_article.related_article

                    )
        print("done")    