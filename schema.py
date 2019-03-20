import graphene
import json
import uuid
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    is_admin = graphene.Boolean()


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username, is_admin=False)
        return CreateUser(user=user)


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())

    def resolve_users(self, info, limit):
        return [
            User(id="1", username="John",
                 created_at=datetime.now(), is_admin=True),
            User(id="2", username="Jen", created_at=datetime.now(),
                 is_admin=False),
            User(id="3", username="Jane",
                 created_at=datetime.now(), is_admin=False),
        ][:limit]


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
result = schema.execute(
    '''
    mutation {
        createUser(username: "Jeff") {
            user {
                id 
                username
                createdAt
            }
        }
    }
    '''
)

print(json.dumps(dict(result.data.items()), indent=2))
