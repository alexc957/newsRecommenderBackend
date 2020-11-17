from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id= graphene.Int(required=True))


    def resolve_user(self,info, id=None, **kwargs):
        return get_user_model().objects.filter(id=id).first()

    def resolve_users(self,info):
        return get_user_model().objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments: 
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model().objects.filter(username=username).first()
        if user:
            raise Exception("Username already exist")

        user2 = get_user_model().objects.filter(email=email).first()
        if user2:
            raise Exception("email already exist")

        user = get_user_model()(
            username = username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()






