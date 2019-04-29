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
FROM
```console
(0.001) SELECT `users`.`id`, `users`.`username` FROM `users` ORDER BY `users`.`id` DESC; args=()
(0.001) SELECT `posts`.`id`, `posts`.`user_id`, `posts`.`content`, FROM `posts` WHERE `posts`.`user_id` = 4 ORDER BY `posts`.`id` DESC; args=(4,)
(0.001) SELECT `posts`.`id`, `posts`.`user_id`, `posts`.`content`, FROM `posts` WHERE `posts`.`user_id` = 3 ORDER BY `posts`.`id` DESC; args=(3,)
(0.001) SELECT `posts`.`id`, `posts`.`user_id`, `posts`.`content`, FROM `posts` WHERE `posts`.`user_id` = 2 ORDER BY `posts`.`id` DESC; args=(2,)
(0.001) SELECT `posts`.`id`, `posts`.`user_id`, `posts`.`content`, FROM `posts` WHERE `posts`.`user_id` = 1 ORDER BY `posts`.`id` DESC; args=(1,)
```
TO
```console
(0.001) SELECT `users`.`id`, `users`.`username` FROM `users` ORDER BY `users`.`id` DESC; args=()
(0.001) SELECT `posts`.`id`, `posts`.`user_id`, `posts`.`content` FROM `posts` WHERE `posts`.`user_id` IN (1, 2, 3, 4) ORDER BY `posts`.`id` DESC; args=(1, 2, 3, 4)
```

##TODO


- [ ] Only Many case

