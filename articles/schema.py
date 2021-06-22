import math
import graphene
from graphene_django import DjangoObjectType
from .models import Article, SimilarArticle
from django.db.models import Q
from django.db.models import Count


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
    recent_articles = graphene.List(ArticleType)
    most_voted = graphene.List(ArticleType)
    total_pages = graphene.Int()

    def resolve_total_pages(self, info, **kwargs):
        all_articles =Article.objects.all()
        total_pages = math.ceil(len(all_articles)/10)
        return total_pages

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
        votes = Article.objects.annotate(num_votes=Count('vote'));
        return votes.order_by('-num_votes')[:10]
        




class AddArticle(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    summary = graphene.String()
    lang = graphene.String()
    category = graphene.String()
    date_uploaded = graphene.Date()
    text_vector = graphene.String()

    class Arguments:
        title = graphene.String()
        summary = graphene.String()
        lang = graphene.String(required=False)
        category = graphene.String(required=False)
        text_vector = graphene.String(required=False)

    def mutate(self, info, title, summary, lang=None, category=None, text_vector=None):
        # if not text_vector:
        #text_vector = ';'.join(nlp(summary).vector.astype(str))

        article = Article(
            title=title,
            summary=summary,
            lang=lang,
            category=category,
            text_vector=text_vector
        )

        article.save()

        return AddArticle(
            id=article.id,
            title=article.title,
            summary=article.summary,
            lang=article.lang,
            category=article.category,
            date_uploaded=article.date_uploaded,
            text_vector=article.text_vector


        )




class Mutation(graphene.ObjectType):
    add_article = AddArticle.Field()