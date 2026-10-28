import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import main


class TestMovieApp(unittest.TestCase):
    #映画管理アプリのテスト

    def setUp(self):
        #各テストの前に実行する初期設定
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_file_name = main.FILE_NAME
        self.original_movies = main.movies

        #テスト専用のJSONファイルを使用する
        main.FILE_NAME = os.path.join(
            self.temp_dir.name, "movies.json"
        )
        main.movies = []

    def tearDown(self):
        #各テストの後に実行する後片付け
        main.FILE_NAME = self.original_file_name
        main.movies = self.original_movies
        self.temp_dir.cleanup()

    def create_movie(self, movie_id=1, title="テスト", director="テスト",
                    year=2026, genre="テスト", rating=4):
        #テスト用の映画データを作成する
        return{
            "id": movie_id,
            "title": title,
            "director": director,
            "year": year,
            "genre": genre,
            "rating": rating
        }

    def test_load_movies_when_file_does_not_exist(self):
        #JSONファイルが存在しない場合、空リストを返す
        result = main.load_movies()

        self.assertEqual(result, [])

    def test_save_and_load_movies(self):
        #映画データを保存し、正しく読み込める
        movie = self.create_movie()
        main.movies = [movie]

        result = main.save_movies()

        self.assertTrue(result)
        self.assertTrue(os.path.exists(main.FILE_NAME))

        loaded_movies = main.load_movies()
        self.assertEqual(loaded_movies, [movie])

    def test_load_movies_with_invalid_json(self):
        #JSONの形式が不正な場合、Noneを返す
        with open(main.FILE_NAME, "w", encoding="utf-8") as file:
            file.write("{invalid file")

        with redirect_stdout(StringIO()):
            result = main.load_movies()

        self.assertIsNone(result)

    def test_load_movies_with_invalid_data_format(self):
        #JSONの最上位がリストでない場合、Noneを返す
        with open(main.FILE_NAME, "w", encoding="utf-8") as file:
            json.dump({"title": "テスト映画"}, file)

        with redirect_stdout(StringIO()):
            result = main.load_movies()

        self.assertIsNone(result)

    def test_load_movies_with_missing_required_key(self):
        #映画データに必要なキーがない場合、Noneを返す
        invalid_movie = {
            "id": 1,
            "title": "テスト",
        }

        with open(main.FILE_NAME, "w", encoding="utf-8") as file:
            json.dump([invalid_movie], file)

        with redirect_stdout(StringIO()):
            result = main.load_movies()

        self.assertIsNone(result)

    def test_get_next_id(self):
        #次の映画IDを正しく取得できる
        main.movies = [
            self.create_movie(movie_id=1),
            self.create_movie(movie_id=3, title="別の映画"),
        ]

        self.assertEqual(main.get_next_id(), 4)

    def test_get_next_id_when_movies_is_empty(self):
        #映画データが空の場合、IDの１を返す
        main.movies = []

        self.assertEqual(main.get_next_id(), 1)

    def test_add_movie(self):
        #映画を登録できる
        user_inputs = [
            "新しい映画",
            "新しい監督",
            "テスト",
            "2026",
            "4",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with redirect_stdout(StringIO()):
                main.add_movie()

        self.assertEqual(len(main.movies), 1)
        self.assertEqual(main.movies[0]["id"], 1)
        self.assertEqual(main.movies[0]["title"], "新しい映画")
        self.assertEqual(main.movies[0]["director"], "新しい監督")
        self.assertEqual(main.movies[0]["genre"], "テスト")
        self.assertEqual(main.movies[0]["year"], 2026)
        self.assertEqual(main.movies[0]["rating"], 4)

        #JSONファイルにも保存されていることを確認する
        with open(main.FILE_NAME, "r", encoding="utf-8") as file:
            saved_movies = json.load(file)

        self.assertEqual(saved_movies, main.movies)

    def test_add_movie_with_empty_title(self):
        #タイトルが空欄の場合、登録しない
        with patch("builtins.input", return_value=" "):
            with redirect_stdout(StringIO()):
                main.add_movie()
            
        self.assertEqual(main.movies, [])

    def test_add_movie_with_invalid_year(self):
        #公開年が整数でない場合、登録しない
        user_inputs = [
            "新しい映画",
            "新しい監督",
            "テスト",
            "abc",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with redirect_stdout(StringIO()):
                main.add_movie()
        
        self.assertEqual(main.movies, [])

    def test_add_movie_with_invalid_rating(self):
        #評価が１～５の範囲外の場合、登録しない
        user_inputs = [
            "新しい映画",
            "新しい監督",
            "ジャンル",
            "2026",
            "10",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with redirect_stdout(StringIO()):
                main.add_movie()

        self.assertEqual(main.movies, [])

    def test_add_movie_rolls_back_when_save_fails(self):
        #保存に失敗した場合、登録を取り消す。
        with patch("builtins.input", side_effect=[
            "新しい映画", "新しい監督", "ジャンル", "2026", "3",
        ]):
            with patch.object(main, "save_movies", return_value=False):
                with redirect_stdout(StringIO()):
                    main.add_movie()

        self.assertEqual(main.movies, [])

    def test_find_movie_by_id(self):
        #指定したIDの映画を取得できる
        movie = self.create_movie()
        main.movies = [movie]

        result = main.find_movie_by_id(1)
        self.assertEqual(result, movie)

    def test_find_movie_by_id_not_found(self):
        #存在しないIDの場合、Noneを返す
        movie = self.create_movie()
        main.movies = [movie]

        result = main.find_movie_by_id(2)

        self.assertIsNone(result)

    def test_search_movie(self):
        #タイトルの一部で検索でき、大文字小文字を区別しない
        main.movies = [
            self.create_movie(title="The Matrix"),
            self.create_movie(movie_id=2, title="Inception"),
        ]

        with patch("builtins.input", return_value="matrix"):
            output = StringIO()
            with redirect_stdout(output):
                main.search_movie()

        self.assertIn("The Matrix", output.getvalue())
        self.assertNotIn("Inception", output.getvalue())

    def test_edit_movie(self):
        #映画の情報を編集できる
        movie = self.create_movie()
        main.movies = [movie]

        #ID、タイトル、監督、公開年、ジャンル、評価
        user_inputs = [
            "1",
            "変更後の映画",
            "",
            "2020",
            "",
            "5",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with redirect_stdout(StringIO()):
                main.edit_movie()

        self.assertEqual(main.movies[0]["title"], "変更後の映画")
        self.assertEqual(main.movies[0]["director"], "テスト")
        self.assertEqual(main.movies[0]["year"], 2020)
        self.assertEqual(main.movies[0]["genre"], "テスト")
        self.assertEqual(main.movies[0]["rating"], 5)

        #編集結果がファイルにも保存されていることを確認
        with open(main.FILE_NAME, "r", encoding="utf-8") as file:
            saved_movies = json.load(file)

        self.assertEqual(saved_movies, main.movies)

    def test_edit_movie_with_invalid_year(self):
        #編集時に不正な公開年を入力した場合、変更しない
        movie = self.create_movie()
        main.movies = [movie]
        original_movie = movie.copy()

        user_inputs = ["1", "", "", "abc", "", ""]

        with patch("builtins.input", side_effect=user_inputs):
            with redirect_stdout(StringIO()):
                main.edit_movie()

        self.assertEqual(main.movies[0], original_movie)

    def test_edit_movie_rolls_back_when_save_fails(self):
        #編集の保存に失敗した場合、元の情報に戻す
        movie = self.create_movie()
        main.movies = [movie]
        original_movie = movie.copy()

        user_inputs = ["1", "変更後", "", "", "", ""]

        with patch("builtins.input", side_effect=user_inputs):
            with patch.object(main, "save_movies", return_value=False):
                with redirect_stdout(StringIO()):
                    main.edit_movie()
                
        self.assertEqual(main.movies[0], original_movie)

    def test_delete_movie(self):
        #確認でｙを入力すると、映画を削除できる
        movie = self.create_movie()
        main.movies = [movie]
        main.save_movies()

        with patch("builtins.input", side_effect=["1", "y"]):
            with redirect_stdout(StringIO()):
                main.delete_movie()
            
        self.assertEqual(main.movies, [])

        with open(main.FILE_NAME, "r", encoding="utf-8") as file:
            saved_movies = json.load(file)

        self.assertEqual(saved_movies, [])

    def test_delete_movie_cancelled(self):
        #確認でｎを入力すると削除しない
        movie = self.create_movie()
        main.movies = [movie]

        with patch("builtins.input", side_effect=["1", "n"]):
            with redirect_stdout(StringIO()):
                main.delete_movie()

        self.assertEqual(main.movies, [movie])

    def test_delete_movie_rolls_back_when_save_fails(self):
        #削除の保存に失敗した場合、映画をもとの位置に戻す
        first_movie = self.create_movie(movie_id=1, title="映画A")
        second_movie = self.create_movie(movie_id=2, title="映画B")
        main.movies = [first_movie, second_movie]

        with patch("builtins.input", side_effect=["1", "y"]):
            with patch.object(main, "save_movies", return_value=False):
                with redirect_stdout(StringIO()):
                    main.delete_movie()

        self.assertEqual(main.movies, [first_movie, second_movie])

    def test_filter_by_genre(self):
        #ジャンルを指定して映画を絞り込める
        main.movies = [
            self.create_movie(title="SF映画", genre="SF"),
            self.create_movie(movie_id=2, title="ドラマ", genre="ドラマ"),
        ]

        with patch("builtins.input", return_value="SF"):
            output = StringIO()
            with redirect_stdout(output):
                main.filter_by_genre()

        self.assertIn("SF映画", output.getvalue())
        self.assertNotIn("ドラマ", output.getvalue())

    def test_sort_movies_by_year_ascending(self):
        #公開年の古い順に並べ替えられる
        main.movies = [
            self.create_movie(movie_id=1, title="新しい映画", year=2024),
            self.create_movie(movie_id=2, title="古い映画", year=2000),
        ]

        with patch("builtins.input", return_value="1"):
            output = StringIO()
            with redirect_stdout(output):
                main.sort_movies()

        result = output.getvalue()
        self.assertLess(
            result.index("古い映画"),
            result.index("新しい映画"),
        )

    def test_sort_movies_by_year_descending(self):
        #公開年の新しい順に並べ替えられる
        main.movies = [
            self.create_movie(movie_id=1, title="古い映画", year=2000),
            self.create_movie(movie_id=2, title="新しい映画", year=2024),
        ]

        with patch("builtins.input", return_value="2"):
            output = StringIO()
            with redirect_stdout(output):
                main.sort_movies()

        result = output.getvalue()
        self.assertLess(
            result.index("新しい映画"),
            result.index("古い映画"),
        )

    def test_sort_movies_by_rating(self):
        #評価の高い順に並べ替えられる
        main.movies = [
            self.create_movie(movie_id=1, title="低評価映画", rating=2),
            self.create_movie(movie_id=2, title="高評価映画", rating=5),
        ]

        with patch("builtins.input", return_value="3"):
            output = StringIO()
            with redirect_stdout(output):
                main.sort_movies()

        result = output.getvalue()
        self.assertLess(
            result.index("高評価映画"),
            result.index("低評価映画"),
        )

if __name__ == "__main__":
    unittest.main()