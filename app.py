from flask import Flask, Response, jsonify, abort
from typing import Tuple
from flask import json

from flask import Flask, jsonify


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

def data_loader() -> Tuple[dict, dict]:
    """
    Функция загружает данные из json файлов и преобразует их в dict.
    Функция не должна нарушать изначальную структуру данных.
    Формат ответа:
#     posts: [
#         {
#             id: <int>,
#             title: <str>,
#             body: <str>, 
#             author:  <str>,
#             created_at: <str>,
#             comments_count: <int>
#         }
#     ],
#     total_results: <int>
    """
    with open('data/posts.json', encoding='UTF-8') as f_posts, open('data/comments.json', encoding="UTF-8") as f_comments:
        posts = json.load(f_posts)
        comments = json.load(f_comments)
    return posts, comments

@app.route('/')
def index():
    posts, comments = data_loader()
    posts_with_comments_count = []
    for post in posts["posts"]:
        comments_count = len([comment for comment in comments["comments"] if comment["post_id"] == post["id"]])
        post_with_comments_count = {
            "id": post["id"],
            "title": post["title"],
            "body": post["body"],
            "author": post["author"],
            "created_at": post["created_at"],
            "comments_count": comments_count
        }
        posts_with_comments_count.append(post_with_comments_count)
        total_results = f'total_results: {len(posts_with_comments_count)}'
    
    return json.jsonify(posts_with_comments_count, total_results)


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """
    На странице /posts/<post_id> вывести json, который должен содержать:
    - пост с указанным в ссылке id
    - список всех комментариев к новости

    Отдавайте ошибку abort(404), если пост не существует.


    Формат ответа:
    id: <int>,
    title: <str>,
    body: <str>, 
    author:  <str>,
    created_at: <str>
    comments: [
        "user": <str>,
        "post_id": <int>,
        "comment": <str>,
        "created_at": <str>
    ]

    Порядок ключей словаря в ответе не важен
    """
    posts, comments = data_loader()
    post = next((post for post in posts["posts"] if post["id"] == post_id), None)
    if post is None:
        abort(404)
    comment = [comment for comment in comments["comments"] if comment['post_id'] == post_id]
    output = {
        "id": post["id"],
        "title": post["title"],
        "body": post["body"],
        "author": post["author"],
        "created_at": post["created_at"],
        "comments": comment
    }
    return jsonify(output)

if __name__ == '__main__':
    app.run()