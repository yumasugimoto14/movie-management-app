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


if __name__ == "__main__":
    unittest.main()