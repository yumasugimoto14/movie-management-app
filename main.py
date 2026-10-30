import json
import os

#データ保存用ファイル
FILE_NAME = "movies.json"


def load_movies():
    #JSONファイルから映画データを読み込む。
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("映画データの形式が正しくありません。")
            return None
        
        for movie in data:
            if not isinstance(movie, dict):
                print("映画データの形式が正しくありません。")
                return None
            required_keys = {"id", "title", "director", "year", "rating"}
            if not required_keys.issubset(movie.keys()):
                print("必要な項目が不足している映画データがあります。")
                return None
        
        return data

    except (json.JSONDecodeError, OSError):
        print("映画データを読み込めませんでした。")
        return None


def save_movies():
    #映画データをJSONファイルに保存する
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(movies, file, ensure_ascii=False, indent=4)
            return True
    except OSError:
        print("映画データの保存に失敗しました。")
        return False


def add_movie_record(title, director, genre, year, rating):
    #Web画面から受け取った映画情報を登録する

    #タイトルの確認
    if not isinstance(title, str) or not title.strip():
        return False

    #公開年の確認
    if not isinstance(year, int) or year <= 0:
        return False

    #評価の確認
    if not isinstance(rating, int) or not 1 <= rating <= 5:
        return False

    #次のIDを決定する
    if not movies:
        movie_id = 1
    else:
        movie_id = max(movie["id"] for movie in movies) + 1

    #映画データを作成する
    movie = {
        "id": movie_id,
        "title": title.strip(),
        "director": director.strip(),
        "genre": genre.strip(),
        "year": year,
        "rating": rating
    }

    #　映画データを追加する
    movies.append(movie)

    #　JSONファイルに保存する
    if save_movies():
        return True

    #　保存に失敗した場合は追加したデータを取り消す
    movies.remove(movie)

    return False


def get_next_id():
    #次に使用する映画IDを取得する
    if not movies:
        return 1
    return max(movie["id"] for movie in movies) + 1


def input_non_empty(prompt):
    #空欄でない文字列を入力させる。キャンセル時はNoneを返す。
    value = input(prompt).strip()
    if not value:
        print("空欄にはできません。")
        return None
    return value


def input_year(prompt="公開年："):
    #正の整数の公開年を入力してもらう。
    try:
        year = int(input(prompt))
    except ValueError:
        print("公開年には整数を入力してください。")
        return None

    if year <= 0:
        print("公開年には1以上を入力してください。")
        return None

    return year


def input_rating(prompt="評価（１～５）："):
    #１～５の整数の評価を入力してもらう。
    try:
        rating = int(input(prompt))
    except ValueError:
        print("評価には整数を入力してください。")
        return None

    if not 1 <= rating <= 5:
        print("評価は１～５で入力してください。")
        return None

    return rating 


def print_movie(movie):
    #映画１件のデータを表示する。
    print(f"ID：{movie['id']}")
    print(f"タイトル：{movie['title']}")
    print(f"監督：{movie['director']}")
    print(f"公開年：{movie['year']}")
    print(f"ジャンル：{movie['genre']}")
    print(f"評価：{'*' * movie['rating']}")
    print("-" * 24)


def show_movies(movie_list=None):
    #映画一覧を表示する。
    if movie_list is None:
        movie_list = movies

    print("\n---映画一覧---")
    if not movie_list:
        print("該当する映画はありません。")
        return

    for movie in movie_list:
        print_movie(movie)


def add_movie():
    #映画を登録する。
    print("\n---映画登録---")

    title = input_non_empty("タイトル：")
    if title is None:
        return

    director = input_non_empty("監督：")
    if director is None:
        return 

    genre = input_non_empty("ジャンル：")
    if genre is None:
        return

    year = input_year()
    if year is None:
        return

    rating = input_rating()
    if rating is None:
        return

    movie = {
        "id" : get_next_id(),
        "title" : title,
        "director" : director,
        "genre" : genre,
        "year" : year,
        "rating" : rating,
        }

    movies.append(movie)

    if save_movies():
        print(f"「{title}」を登録しました。")
    else:
        movies.remove(movie)
        print("登録を取り消しました。データは保存されていません。")


def search_movie():
    #タイトルの一部で映画を検索する。
    print("\n---映画検索---")

    keyword = input_non_empty("検索するタイトル：")
    if keyword is None:
        return

    found_movies = [
        movie for movie in movies
        if keyword.casefold() in movie["title"].casefold()
    ]

    show_movies(found_movies)


def find_movie_by_id(movie_id):
    #IDに一致する映画を探す。見つからなければNoneを返す。
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return None


def input_movie_id(prompt):
    #整数の映画IDを入力してもらう。
    try:
        return int(input(prompt))
    except ValueError:
        print("IDには整数を入力してください。")
        return None


def edit_movie():
    #指定した映画の情報を編集する。
    print("\n---映画情報の編集---")
    movie_id = input_movie_id("編集する映画のID：")
    if movie_id is None:
        return

    movie = find_movie_by_id(movie_id)
    if movie is None:
        print("指定されたIDの映画がありません。")
        return

    print("現在の情報：")
    print_movie(movie)
    print("変更しない項目はそのままEnterを押してください。")

    new_title = input(f"タイトル（{movie['title']}）：").strip()
    new_director = input(f"監督（{movie['director']}）：").strip()
    new_year_text = input(f"公開年（{movie['year']}）：").strip()
    new_genre = input(f"ジャンル（{movie['genre']}）：").strip()
    new_rating_text = input(f"評価（{movie['rating']}）：").strip()

    update_movie = movie.copy()

    if new_title:
        update_movie["title"] = new_title
    if new_director:
        update_movie["director"] = new_director
    if new_genre:
        update_movie["genre"] = new_genre

    if new_year_text:
        try:
            new_year = int(new_year_text)
            if new_year <= 0:
                print("公開年は1以上を入力してください。")
                return
            update_movie["year"] = new_year
        except ValueError:
            print("公開年は整数を入力してください。")
            return

    if new_rating_text:
        try:
            new_rating = int(new_rating_text)
            if not 1 <= new_rating <= 5:
                print("評価には１～５を入力してください。")
                return
            update_movie["rating"] = new_rating
        except ValueError:
            print("評価には整数を入力してください。")
            return
            
    index = movies.index(movie)
    movies[index] = update_movie

    if save_movies():
        print("映画情報を更新しました。")
    else:
        movies[index] = movie
        print("保存できなかったため、変更を取り消しました。")


def delete_movie():
    #指定した映画を削除する。
    print("\n---映画削除---")
    movie_id = input_movie_id("削除する映画のID：")
    if movie_id is None:
        return

    movie = find_movie_by_id(movie_id)
    if movie is None:
        print("指定されたIDの映画はありません。")
        return

    confirm = input(f"「{movie['title']}」を削除しますか？（y/n）：").strip().lower()
    if confirm != "y":
        print("削除を取り消しました。")
        return

    index = movies.index(movie)
    movies.pop(index)

    if save_movies():
        print(f"「{movie['title']}」を削除しました。")
    else:
        movies.insert(index, movie)
        print("保存できなかったため、削除を取り消しました。")

    
def filter_by_genre():
    #ジャンルを指定して映画を絞り込む。
    print("\n---ジャンルによる絞り込み---")
    genre = input_non_empty("ジャンル：")
    if genre is None:
        return
    
    filtered_movies = [
        movie for movie in movies
        if movie["genre"].casefold() == genre.casefold()
    ]

    show_movies(filtered_movies)


def sort_movies():
    #公開年または評価で映画を並び替える。
    print("---映画の並べ替え---")
    print("１．古い順")
    print("２．新しい順")
    print("３．評価が高い順")
    choice = input("１～３の番号を入力してください。：")

    if choice == "1":
        sorted_movies = sorted(movies, key=lambda movie: movie["year"])
    elif choice == "2":
        sorted_movies = sorted(movies, key=lambda movie: movie["year"], reverse=True)
    elif choice == "3":
        sorted_movies = sorted(movies, key=lambda movie: movie["rating"], reverse=True)
    else:
        print("１～３の番号を入力してください。")
        return

    show_movies(sorted_movies)


def main():
    #アプリのメイン処理。
    while True:
        print("\n=====映画管理アプリ=====")
        print("１.登録")
        print("２.一覧")
        print("３.検索")
        print("４.編集")
        print("５.削除")
        print("６.ジャンル絞り込み")
        print("７.並べ替え")
        print("８.終了")

        choice = input("１～８の番号を入力してください。：").strip()

        if choice == "1":
            add_movie()
        elif choice == "2":
            show_movies()
        elif choice == "3":
            search_movie()
        elif choice == "4":
            edit_movie()
        elif choice == "5":
            delete_movie()
        elif choice == "6":
            filter_by_genre()
        elif choice == "7":
            sort_movies()
        elif choice == "8":
            print("アプリを終了します。")
            break
        else:
            print("１～８の番号を入力してください。")

#ファイルの読み込みに失敗した場合は、データを上書きしないように起動を中止する。
movies = load_movies()

if __name__ == "__main__":
    if movies is not None:
        main()
    else:
        print("データを保護するため、アプリを終了します。")

