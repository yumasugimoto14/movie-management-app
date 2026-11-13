
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import database
from web_app import app


class TestMovieAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # テスト専用の一時フォルダを作成
        cls.temp_dir = tempfile.TemporaryDirectory()

        # テスト用データベースの保存先
        cls.test_db_path = Path(cls.temp_dir.name) / "test_movies.db"

        # database.DB_PATHをテスト用のパスに変更
        cls.db_path_patcher = patch.object(
            database,
            "DB_PATH",
            cls.test_db_path
        )
        cls.db_path_patcher.start()

        # テスト用クライアントを作成
        cls.client = TestClient(app)

        # アプリケーションを起動
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls):
        # テストクライアントを終了
        cls.client.__exit__(None, None, None)

        # DB_PATHを元に戻す
        cls.db_path_patcher.stop()

        # 一時フォルダを削除
        cls.temp_dir.cleanup()

    def setUp(self):
        # 各テストの前に映画データを全て削除
        conn = database.get_connection()

        try:
            conn.execute("DELETE FROM movies")
            conn.commit()
        finally:
            conn.close()

    def create_movie(self):
        # テスト用の映画を登録
        return database.add_movie(
            "テスト映画",
            "テスト監督",
            "アクション",
            2024,
            5
        )

    def test_get_movies(self):
        """映画一覧を取得できる"""

        self.create_movie()

        response = self.client.get("/api/movies")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["title"], "テスト映画")

    def test_get_movie(self):
        """映画の詳細を取得できる"""

        movie_id = self.create_movie()

        response = self.client.get(
            f"/api/movies/{movie_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "テスト映画")

    def test_get_movie_not_found(self):
        """存在しない映画IDでは404になる"""

        response = self.client.get("/api/movies/999")

        self.assertEqual(response.status_code, 404)

    def test_create_movie(self):
        """映画を登録できる"""

        movie_data = {
            "title": "新しい映画",
            "director": "新しい監督",
            "genre": "アクション",
            "year": 2024,
            "rating": 5
        }

        response = self.client.post(
            "/api/movies",
            json=movie_data
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["movie"]["title"],
            "新しい映画"
        )

        # DBに登録されたことも確認
        movies = database.get_all_movies()
        self.assertEqual(len(movies), 1)

    def test_create_movie_invalid(self):
        """不正な映画データでは422になる"""

        movie_data = {
            "title": "",
            "director": "テスト監督",
            "genre": "アクション",
            "year": 2024,
            "rating": 5
        }

        response = self.client.post(
            "/api/movies",
            json=movie_data
        )

        self.assertEqual(response.status_code, 422)

    def test_update_movie(self):
        """映画情報を更新できる"""

        movie_id = self.create_movie()

        movie_data = {
            "title": "更新後の映画",
            "director": "更新後の監督",
            "genre": "ドラマ",
            "year": 2025,
            "rating": 4
        }

        response = self.client.put(
            f"/api/movies/{movie_id}",
            json=movie_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["movie"]["title"],
            "更新後の映画"
        )

        # DBのデータも更新されているか確認
        updated_movie = database.get_movie_by_id(movie_id)

        self.assertEqual(
            updated_movie["title"],
            "更新後の映画"
        )

    def test_update_movie_not_found(self):
        """存在しない映画IDでは404になる"""

        movie_data = {
            "title": "更新後の映画",
            "director": "更新後の監督",
            "genre": "ドラマ",
            "year": 2025,
            "rating": 4
        }

        response = self.client.put(
            "/api/movies/999",
            json=movie_data
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_movie(self):
        """映画を削除できる"""

        movie_id = self.create_movie()

        response = self.client.delete(
            f"/api/movies/{movie_id}"
        )

        self.assertEqual(response.status_code, 204)

        # 削除後に映画が存在しないことを確認
        deleted_movie = database.get_movie_by_id(movie_id)

        self.assertIsNone(deleted_movie)

    def test_delete_movie_not_found(self):
        """存在しない映画IDでは404になる"""

        response = self.client.delete("/api/movies/999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
