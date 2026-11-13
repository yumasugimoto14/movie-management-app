
# API設計書

## 1. 概要

映画管理アプリで管理している映画情報を、
外部のプログラムから取得・登録・更新・削除するためのREST API。

## 2. エンドポイント一覧

| HTTPメソッド | URL | 内容 |
|---|---|---|
| GET | /api/movies | 映画一覧取得 |
| GET | /api/movies/{movie_id} | 映画詳細取得 |
| POST | /api/movies | 映画登録 |
| PUT | /api/movies/{movie_id} | 映画更新 |
| DELETE | /api/movies/{movie_id} | 映画削除 |

## 3. 映画データの項目

| 項目 | データ型 | 内容 |
|---|---|---|
| id | integer | 映画ID |
| title | string | 映画タイトル |
| director | string | 監督名 |
| genre | string | ジャンル |
| year | integer | 公開年 |
| rating | integer | 評価（1〜5） |

## 4. HTTPステータスコード

| コード | 意味 |
|---|---|
| 200 | リクエスト成功 |
| 201 | データ登録成功 |
| 204 | 削除成功（レスポンス本文なし） |
| 400 | 入力値エラー |
| 404 | 対象データが存在しない |
| 422 | リクエストデータの検証エラー |
| 500 | サーバー内部エラー |

## 5. POST・PUTのリクエスト例

{
    "title": "インセプション",
    "director": "クリストファー・ノーラン",
    "genre": "SF",
    "year": 2010,
    "rating": 5
}

## 6. 使用技術

- Python
- FastAPI
- SQLite
- Pydantic
- HTML
- CSS
