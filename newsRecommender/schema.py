import graphene 
import graphql_jwt 
import articles.schema as article_schema 
import users.schema as users_schema 
import collector.schema as collector_schema
import recommendations.Schema as recs_schema 

class Query(
    article_schema.Query, 
    users_schema.Query,
    collector_schema.Query,
    recs_schema.Query,
    graphene.ObjectType):
    pass 

class Mutation(
    users_schema.Mutation,
    collector_schema.Mutation,
    article_schema.Mutation,
    graphene.ObjectType):
     
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()



schema = graphene.Schema(query=Query, mutation= Mutation)
