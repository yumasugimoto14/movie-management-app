
import database


# データベースの初期化
database.initialize_database()


# テスト用の映画を登録
movie_id = database.add_movie(
    "テスト映画",
    "テスト監督",
    "ドラマ",
    2020
)

print(f"登録した映画のID：{movie_id}")


# 登録した映画情報を更新
result = database.update_movie(
    movie_id,
    "更新後の映画",
    "更新後の監督",
    "SF",
    2024
)

if result:
    print("映画情報を更新しました。")
else:
    print("映画情報を更新できませんでした。")


# 更新後の映画情報を確認
movies = database.get_all_movies()

for movie in movies:
    if movie["id"] == movie_id:
        print("\n更新後の映画情報")
        print(f"タイトル：{movie['title']}")
        print(f"監督：{movie['director']}")
        print(f"ジャンル：{movie['genre']}")
        print(f"公開年：{movie['year']}")


# 映画情報を削除
result = database.delete_movie(movie_id)

if result:
    print("\n映画情報を削除しました。")
else:
    print("\n映画情報を削除できませんでした。")


# 削除後の映画情報を確認
movies = database.get_all_movies()

print("\n削除後の映画一覧")

for movie in movies:
    print(f"{movie['id']}：{movie['title']}")
