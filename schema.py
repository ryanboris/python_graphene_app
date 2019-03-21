import graphene
import json
import uuid
from datetime import datetime as dt


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=dt.now())
    is_admin = graphene.Boolean()


class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())

    def resolve_users(self, info, limit):
        return [
            User(id="1", username="John",
                 created_at=dt.now(), is_admin=True),
            User(id="2", username="Jen", created_at=dt.now(),
                 is_admin=False),
            User(id="3", username="Jane",
                 created_at=dt.now(), is_admin=False),
        ][:limit]


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username, is_admin=False)
        return CreateUser(user=user)


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        post = Post(title=title, content=content)
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
result = schema.execute(
    '''

    query getUsersQuery ($limit: Int!) {
        users(limit: $limit) {
                id
                username
                createdAt
        }
    }
    ''',
    variable_values={'limit': 3}
)

print(json.dumps(dict(result.data.items()), indent=2))
