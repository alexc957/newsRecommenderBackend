import graphene 
from graphene_django import DjangoObjectType
from .models import Vote
from articles.models import Article
from users.schema import UserType 
from articles.schema import ArticleType
from django.db.models import Q
from articles.models import Article


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote



class Query(graphene.ObjectType):
    votes = graphene.List(VoteType)
    vote = graphene.Field(VoteType,article_id = graphene.Int(required=True))
    

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

    def resolve_vote(self,info, article_id, **kwargs):
        print("article id",article_id)
        article = Article.objects.filter(id = article_id).first()
        user = info.context.user
        if user.is_anonymous or not user:
            return None
        if not article:
            raise Exception("Bad article id provided")
        return Vote.objects.filter(article = article,user=user).first()






class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    article = graphene.Field(ArticleType)
    liked = graphene.Boolean()
    

    class Arguments:
        article_id = graphene.Int()

    
    def mutate(self, info, article_id):
        user = info.context.user
        #print("username? ",user)
        print("context",info.context)
        if not user.is_authenticated:
            raise Exception('you must be logged to vote!')
        print("user", user.username)        
        article = Article.objects.filter(id = article_id).first()
        if not article:
            raise Exception('Invalid article')
        print("article", article.title)    
        vote = Vote.objects.filter(user=user,article=article).first()
        #print('voted liked',vote.liked)
        if vote:
            vote.liked = not vote.liked 
            vote.save()
            return vote    
        return Vote.objects.create(
            user = user,
            article = article
        )
       


class Mutation(graphene.ObjectType):
    create_vote = CreateVote.Field()