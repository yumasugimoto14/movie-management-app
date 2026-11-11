import sqlite3
from pathlib import Path


#　データベースファイルの保存場所
DB_PATH = Path(__file__).resolve().parent / "movies.db"


def get_connection():
    #　データベースに接続する
    conn = sqlite3.connect(DB_PATH)
    #　カラム名を使ってデータを取得できるようにする
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    #　データベースとテーブルを初期化する
    conn = get_connection()

    try:
        cursor = conn.cursor()

        #　moviesテーブルを作成
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                director TEXT NOT NULL,
                genre TEXT,
                year INTEGER,
                rating INTEGER NOT NULL DEFAULT 3
                    CHECK (rating BETWEEN 1 AND 5)
            )
        """)

        #　既存のテーブルにratingカラムがあるか確認する
        cursor.execute("PRAGMA table_info(movies)")
        columns = [column["name"] for column in cursor.fetchall()]

        #　ratingカラムが存在しない場合は追加する
        if "rating" not in columns:
            cursor.execute("""
                ALTER TABLE movies
                ADD COLUMN rating INTEGER NOT NULL DEFAULT 3
                CHECK (rating BETWEEN 1 AND 5)
            """)

        #　変更を確定
        conn.commit()

    finally:
        #　データベースとの接続を終了
        conn.close()


def add_movie(title, director, genre, year, rating):
    #　映画情報をデータベースに登録する
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO movies (title, director, genre, year, rating)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, director, genre, year, rating)
        )

        #　登録したデータのIDを取得
        movie_id = cursor.lastrowid

        #　登録内容を確定
        conn.commit()

        return movie_id

    finally:
        conn.close()


def get_all_movies():
    #　データベースから全ての映画情報を取得する
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM movies ORDER BY id ASC"
        )

        movies = cursor.fetchall()

        return movies

    finally:
        conn.close()


def sort_movies(movies, sort_by):
    #　並び替え条件を定義する
    sort_options = {
        "id": lambda movie: movie["id"],
        "year_asc": lambda movie: (
            movie["year"] is None,
            movie["year"] if movie["year"] is not None else 0,
            movie["id"]
        ),
        "year_desc": lambda movie: (
            movie["year"] is None,
            -movie["year"] if movie["year"] is not None else 0,
            movie["id"]
        ),
        "rating_desc": lambda movie: (
            -movie["rating"],
            movie["id"]
        )
    }

    sort_key = sort_options.get(sort_by, sort_options["id"])

    return sorted(movies, key=sort_key)


def search_movies(keyword):
    #　映画タイトル・監督名・ジャンルから検索する
    conn = get_connection()

    try:
        cursor = conn.cursor()

        keyword = keyword.strip()
        
        #　検索キーワードを部分一致検索用にする
        search_keyword = f"%{keyword}%"

        cursor.execute(
            """
            SELECT * FROM movies
            WHERE title LIKE ?
                OR director LIKE ?
                OR genre LIKE ?
            ORDER BY id ASC
            """,
            (search_keyword, search_keyword, search_keyword)
        )

        #　検索結果を取得
        movies = cursor.fetchall()

        return movies
    
    finally:
        conn.close()


def update_movie(movie_id, title, director, genre, year, rating):
    #　映画情報を更新する
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE movies
            SET title = ?,
                director = ?,
                genre = ?,
                year = ?,
                rating = ?
            WHERE id = ?
            """,
            (title, director, genre, year, rating, movie_id)
        )

        #　変更されたレコード数を取得
        updated_count = cursor.rowcount

        #　変更内容を確定
        conn.commit()

        return updated_count > 0

    finally:
        conn.close()


def delete_movie(movie_id):
    #　映画情報を削除する
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM movies WHERE id = ?",
            (movie_id,)
        )

        #　削除されたレコード数を取得
        deleted_count = cursor.rowcount

        #　削除内容を確定
        conn.commit()

        return deleted_count > 0

    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()
    print("データベースを初期化しました。")