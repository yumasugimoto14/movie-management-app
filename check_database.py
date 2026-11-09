
import database


# データベースの初期化
database.initialize_database()


# 映画情報を登録
movie_id = database.add_movie(
    "インセプション",
    "クリストファー・ノーラン",
    "SF",
    2010
)

print(f"映画を登録しました。ID：{movie_id}")


# 映画情報を取得
movies = database.get_all_movies()

print("\n映画一覧")

for movie in movies:
    print(f"ID：{movie['id']}")
    print(f"タイトル：{movie['title']}")
    print(f"監督：{movie['director']}")
    print(f"ジャンル：{movie['genre']}")
    print(f"公開年：{movie['year']}")
    print("--------------------")
