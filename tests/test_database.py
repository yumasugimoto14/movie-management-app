import unittest
import sqlite3
import tempfile

from pathlib import Path
from unittest.mock import patch

import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        """テスト用のデータベースを準備する"""

        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_movies.db"

        self.patcher = patch.object(database, "DB_PATH", self.db_path)
        self.patcher.start()

        database.initialize_database()

    def tearDown(self):
        """テスト用のデータベースを片付ける"""

        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_add_movie(self):
        """映画を登録できる"""

        movie_id = database.add_movie(
            "テスト映画",
            "テスト監督",
            "アクション",
            2024,
            5
        )

        movies = database.get_all_movies()

        self.assertEqual(movie_id, 1)
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["title"], "テスト映画")
        self.assertEqual(movies[0]["rating"], 5)


    def create_test_movies(self):
        #　検索・並び替えのテスト用の映画を登録する

        database.add_movie(
            "インセプション",
            "クリストファー・ノーラン",
            "SF",
            2010,
            5
        )

        database.add_movie(
            "君の名は。",
            "新海誠",
            "アニメ",
            2016,
            4
        )

        database.add_movie(
            "天気の子",
            "新海誠",
            "アニメ",
            2019,
            3
        )


    def test_update_movie(self):
        """映画を更新できる"""

        movie_id = database.add_movie(
            "変更前の映画",
            "テスト監督",
            "アクション",
            2020,
            3
        )

        result = database.update_movie(
            movie_id,
            "変更後の映画",
            "新しい監督",
            "ドラマ",
            2024,
            4
        )

        movies = database.get_all_movies()

        self.assertTrue(result)
        self.assertEqual(movies[0]["title"], "変更後の映画")
        self.assertEqual(movies[0]["director"], "新しい監督")
        self.assertEqual(movies[0]["rating"], 4)

    def test_update_nonexistent_movie(self):
        """存在しない映画を更新しようとするとFalseになる"""

        result = database.update_movie(
            999,
            "テスト映画",
            "テスト監督",
            "アクション",
            2024,
            3
        )

        self.assertFalse(result)

    def test_delete_movie(self):
        """映画を削除できる"""

        movie_id = database.add_movie(
            "削除する映画",
            "テスト監督",
            "アクション",
            2020,
            3
        )

        result = database.delete_movie(movie_id)

        movies = database.get_all_movies()

        self.assertTrue(result)
        self.assertEqual(len(movies), 0)

    def test_delete_nonexistent_movie(self):
        """存在しない映画を削除しようとするとFalseになる"""

        result = database.delete_movie(999)

        self.assertFalse(result)

    def test_invalid_rating(self):
        """評価が1〜5以外の場合はエラーになる"""

        with self.assertRaises(sqlite3.IntegrityError):
            database.add_movie(
                "テスト映画",
                "テスト監督",
                "アクション",
                2024,
                6
            )

    def test_existing_database_migration(self):
        """評価カラムがない既存DBにratingを追加できる"""

        old_db_path = self.db_path.parent / "old_movies.db"

        conn = sqlite3.connect(old_db_path)

        conn.execute("""
            CREATE TABLE movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                director TEXT NOT NULL,
                genre TEXT,
                year INTEGER
            )
        """)

        conn.execute("""
            INSERT INTO movies (title, director, genre, year)
            VALUES (?, ?, ?, ?)
        """, ("既存映画", "既存監督", "ドラマ", 2020))

        conn.commit()
        conn.close()

        with patch.object(database, "DB_PATH", old_db_path):
            database.initialize_database()
            movies = database.get_all_movies()

        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["title"], "既存映画")
        self.assertEqual(movies[0]["rating"], 3)


    def test_search_movies_by_title(self):
        """映画タイトルで検索できる"""

        self.create_test_movies()

        movies = database.search_movies("インセプション")

        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["title"], "インセプション")

    def test_search_movies_by_director(self):
        """監督名で検索できる"""

        self.create_test_movies()

        movies = database.search_movies("新海誠")

        self.assertEqual(len(movies), 2)

    def test_search_movies_by_genre(self):
        """ジャンルで検索できる"""

        self.create_test_movies()

        movies = database.search_movies("アニメ")

        self.assertEqual(len(movies), 2)

    def test_search_movies_no_result(self):
        """該当する映画がない場合は空リストになる"""

        self.create_test_movies()

        movies = database.search_movies("該当なし")

        self.assertEqual(len(movies), 0)

    def test_search_movies_empty_keyword(self):
        """空文字で検索すると全件取得できる"""

        self.create_test_movies()

        movies = database.search_movies("")

        self.assertEqual(len(movies), 3)

    def test_search_movies_with_spaces(self):
        """検索キーワードの前後の空白を除去できる"""

        self.create_test_movies()

        movies = database.search_movies("  インセプション  ")

        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["title"], "インセプション")


    def test_sort_movies_by_year_ascending(self):
        """公開年の古い順に並び替えられる"""

        self.create_test_movies()

        movies = database.get_all_movies()
        sorted_movies = database.sort_movies(movies, "year_asc")

        years = [movie["year"] for movie in sorted_movies]

        self.assertEqual(years, [2010, 2016, 2019])

    def test_sort_movies_by_year_descending(self):
        """公開年の新しい順に並び替えられる"""

        self.create_test_movies()

        movies = database.get_all_movies()
        sorted_movies = database.sort_movies(movies, "year_desc")

        years = [movie["year"] for movie in sorted_movies]

        self.assertEqual(years, [2019, 2016, 2010])

    def test_sort_movies_by_rating_descending(self):
        """評価の高い順に並び替えられる"""

        self.create_test_movies()

        movies = database.get_all_movies()
        sorted_movies = database.sort_movies(movies, "rating_desc")

        ratings = [movie["rating"] for movie in sorted_movies]

        self.assertEqual(ratings, [5, 4, 3])

    def test_sort_movies_by_invalid_condition(self):
        """不正な並び替え条件の場合は登録順になる"""

        self.create_test_movies()

        movies = database.get_all_movies()
        sorted_movies = database.sort_movies(movies, "invalid")

        ids = [movie["id"] for movie in sorted_movies]

        self.assertEqual(ids, [1, 2, 3])


    def test_search_and_sort_movies(self):
        """検索結果を公開年の新しい順に並び替えられる"""

        self.create_test_movies()

        movies = database.search_movies("新海誠")
        sorted_movies = database.sort_movies(movies, "year_desc")

        years = [movie["year"] for movie in sorted_movies]

        self.assertEqual(len(sorted_movies), 2)
        self.assertEqual(years, [2019, 2016])
        

if __name__ == "__main__":
    unittest.main()