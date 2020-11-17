import math
import graphene
from graphene_django import DjangoObjectType
from .models import Article, SimilarArticle
from django.db.models import Q


class ArticleType(DjangoObjectType):
    """
    docstring
    """
    class Meta:
        model = Article



class SimilarArticleType(DjangoObjectType):
    class Meta:
        model =  SimilarArticle


class Query(graphene.ObjectType):
    """
    docstring
    """
    articles = graphene.List(
        ArticleType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int())

    article = graphene.Field(
        ArticleType,
        article_id=graphene.Int(required=True)
    )

    def resolve_total_pages(self, info, **kwargs):
        raise Exception("Not implemented yet")


    def resolve_articles(self,info,search=None,first=None,skip=None,**kwargs):
        qs = Article.objects.all() # qs: query selector 
        if search:
            filter = (
                Q(title__icontains=search) | Q(summary__icontains=search)

            )
            qs = qs.filter(filter)


        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]


        return qs

    def resolve_article(self, info, article_id=None, **kwargs):
        article = Article.objects.get(id=article_id)
        if not article:
            raise Exception('Bad article Id')

        return article


    def resolve_recent_articles(self, info, **kwargs):
        articles = Article.objects.all().order_by('-date_uploaded')
        return articles[:10]


    def resolve_most_voted(self,info, **kwargs):
        raise Exception("not implemented yet")




#class AddArticle(graphene.Mutation):
 #   pass




