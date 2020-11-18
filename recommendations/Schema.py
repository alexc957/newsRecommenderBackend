import graphene
from graphene_django import DjangoObjectType
from .models import Recommendation
from django.contrib.auth import get_user_model
from users.schema import UserType
from articles.schema import ArticleType
from articles.models import Article, SimilarArticle
from .Recommender import Recommender
from articles.schema import SimilarArticleType
import time
import random 
import datetime 


recomender = Recommender(threshold=0.998)

class RecommendationType(DjangoObjectType):
    """
    docstring
    """
    class Meta:
        model = Recommendation


class Query(graphene.ObjectType):
    recommendations = graphene.List(
        RecommendationType
    )

    similar_articles = graphene.List(
        SimilarArticleType,
        article_id = graphene.Int(required=True)
    )

    def resolve_similar_articles(self,info, article_id=None, **kwargs):
        article = Article.objects.filter(id=article_id).first()
        if not article:
            raise Exception("Bad ID provided")
        related_articles = SimilarArticle.objects.filter(principal_article=article).order_by('-score')

        return similar_articles[:10]

    def resolve_recommendations(self, info, **kwargs):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("You must be logged to receive recommendations")

        recomender.generate_recommendations(user)
        recs = Recommendation.objects.filter(user=user).order_by('-score')
        return score
