
# API設計書

## 1. 概要

映画管理アプリで使用するREST APIの設計書。

FastAPIとSQLiteを使用し、映画情報の取得・登録・更新・削除を行う。

## 2. エンドポイント一覧

| No. | HTTPメソッド | URL | 処理 |
|---|---|---|---|
| 1 | GET | /api/movies | 映画一覧取得 |
| 2 | GET | /api/movies/{movie_id} | 映画詳細取得 |
| 3 | POST | /api/movies | 映画登録 |
| 4 | PUT | /api/movies/{movie_id} | 映画更新 |
| 5 | DELETE | /api/movies/{movie_id} | 映画削除 |

## 3. 映画データの構造

| 項目 | データ型 | 必須 |
|---|---|---|
| id | integer | No |
| title | string | Yes |
| director | string | Yes |
| genre | string | Yes |
| year | integer | Yes |
| rating | integer | Yes |

## 4. 各APIの仕様

### 4-1. 映画一覧取得

- メソッド：GET
- URL：/api/movies
- 成功時：200 OK
- 処理：登録されている映画一覧をJSON形式で返す。

### 4-2. 映画詳細取得

- メソッド：GET
- URL：/api/movies/{movie_id}
- 成功時：200 OK
- エラー時：404 Not Found
- 処理：指定されたIDの映画情報を返す。

### 4-3. 映画登録

- メソッド：POST
- URL：/api/movies
- 成功時：201 Created
- エラー時：422 Unprocessable Entity
- 処理：受け取った映画情報をデータベースに登録する。

### 4-4. 映画更新

- メソッド：PUT
- URL：/api/movies/{movie_id}
- 成功時：200 OK
- エラー時：404 Not Found、422 Unprocessable Entity
- 処理：指定されたIDの映画情報を更新する。

### 4-5. 映画削除

- メソッド：DELETE
- URL：/api/movies/{movie_id}
- 成功時：204 No Content
- エラー時：404 Not Found
- 処理：指定されたIDの映画情報を削除する。

## 5. バリデーション

- titleは空欄にしない。
- directorは空欄にしない。
- genreは空欄にしない。
- yearは整数とする。
- ratingは1〜5の整数とする。

## 6. エラー処理

| ステータスコード | 内容 |
|---|---|
| 404 | 指定した映画が存在しない |
| 422 | 入力データが不正 |
| 500 | サーバー内部エラー |
