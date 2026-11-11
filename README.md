
# 映画管理アプリ

## 概要
PythonとFastAPIを使用して作成した映画管理アプリです。
映画の登録・一覧表示・編集・削除を行うことができます。

## 主な機能
- 映画の一覧表示
- 映画の新規登録
- 映画情報の編集
- 映画の削除
- 映画タイトル・監督名・ジャンルによる検索
- 公開年による並び替え
- 評価による並び替え
- 検索結果の件数表示
- SQLiteによるデータ保存
- 入力値の検証
- ユニットテスト

## 使用技術
- Python
- FastAPI
- Jinja2
- HTML
- CSS
- JSON
- unittest

## 環境構築

### 1. リポジトリをクローン
```bash
git clone https://github.com/yumasugimoto14/movie-management-app.git
cd movie-management-app
```

### 2. 仮想環境を作成
```bash
python3 -m venv .venv
```

### 3. 仮想環境を有効化
```bash
source .venv/bin/activate
```

### 4. 必要なライブラリをインストール
```bash
python -m pip install -r requirements.txt
```

## アプリの起動方法
```bash
uvicorn web_app:app --reload
```

ブラウザで以下にアクセスしてください。

http://127.0.0.1:8000/

## テスト方法
```bash
python -m unittest discover -s tests -v
```

## ディレクトリ構成
```text
movie-management-app/
├── main.py
├── web_app.py
├── movies.json
├── requirements.txt
├── README.md
├── tests/
│   └── test_main.py
├── templates/
│   ├── index.html
│   ├── add.html
│   └── edit.html
└── static/
    └── style.css
```
