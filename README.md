# drf-dynamic-relations
🥤Dynamically set eager load in Django REST Framework.

Dynamic field in serializer with query string. If the field contains a relation, it automatically use `prefetch_related` for eager load to improve performance

```python
class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ('id', 'content')


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username',)
        includible_fields = ('posts',)

class UserViewSet(DynamicRelationMixin, viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
```

`GET /users`
```json
[
  {
    "id": 1,
    "username": "flatcoke"
  },
  ...
]

```
`GET /users?omit=username`
```json
[
  {
    "id": 1
  },
  ...
]

```

`GET /users?include=posts`
```json
[
  {
    "id": 1,
    "username": "flatcoke",
    "posts": [
        {"id": 1, "content": "This is a content"},
        ...
    ]
  },
  ...
]

```

`GET /users?fields=id,posts`
```json
[
  {
    "id": 1,
    "posts": [
        {"id": 1, "content": "This is a content"},
        ...
    ]
  },
  ...
]

```
