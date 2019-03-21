import graphene
import json
import uuid
from datetime import datetime


class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return f'https://cloudinary.com/{self.username}/{self.id}'


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())

    def resolve_users(self, info, limit=None):
        return [
            User(id="1", username="Fred", created_at=datetime.now()),
            User(id="2", username="Doug", created_at=datetime.now())
        ][:limit]


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        if info.context.get('is_anonymous'):
            raise Exception('Not authenticated!')
        post = Post(title=title, content=content)
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
    {
      users {
        id
        createdAt
        username
        avatarUrl
      }
    }
    ''',
    # context={'is_anonymous': True}
    # variable_values={'limit': 1}
)

dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))
