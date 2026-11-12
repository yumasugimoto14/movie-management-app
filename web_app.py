
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import database


# FastAPIアプリケーションを作成
app = FastAPI()

# HTMLテンプレートの保存場所
templates = Jinja2Templates(directory="templates")

# CSSファイルの保存場所
app.mount("/static", StaticFiles(directory="static"), name="static")


def validate_movie_input(title, director, year, rating):
    #映画の入力値を検証する
     
    if not title.strip():
        raise HTTPException(
            status_code=400,
            detail="映画タイトルを入力してください。"
        )

    if not director.strip():
        raise HTTPException(
            status_code=400,
            detail="監督名を入力してください。"
        )

    if not 1888 <= year <= 2100:
        raise HTTPException(
            status_code=400,
            detail="公開年は1888〜2100の範囲で入力してください。"
        )

    if not 1 <= rating <= 5:
        raise HTTPException(
            status_code=400,
            detail="評価は1〜5の範囲で入力してください。"
        )


# アプリ起動時にデータベースを初期化
@app.on_event("startup")
def startup():
    database.initialize_database()


# 映画一覧画面
@app.get("/")
def index(
    request: Request, 
    keyword: str = "", 
    sort_by:str = "id"
):
    # 検索キーワードの前後の空白を削除
    keyword = keyword.strip()

    # 並び替え条件を取得
    sort_options = ["id", "year_asc", "year_desc", "rating_desc"]

    if sort_by not in sort_options:
        sort_by = "id"

    #　キーワードが入力されている場合は検索する
    if keyword:
        movies = database.search_movies(keyword)
    #　キーワードが空の場合は全件取得する
    else:
        movies = database.get_all_movies()

    #　並び替えを行う
    movies = database.sort_movies(movies, sort_by)

    movie_count = len(movies)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "movies": movies,
            "keyword": keyword,
            "sort_by": sort_by,
            "movie_count": movie_count
        }
    )


# 映画登録画面
@app.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add.html",
        context={}
    )


# 映画登録処理
@app.post("/add")
def add_movie(
    title: str = Form(...),
    director: str = Form(...),
    genre: str = Form(...),
    year: int = Form(...),
    rating: int = Form(...)
):
    validate_movie_input(title, director, year, rating)
    
    database.add_movie(title, director, genre, year, rating)

    return RedirectResponse(url="/", status_code=303)


# 映画編集画面
@app.get("/edit/{movie_id}")
def edit_page(request: Request, movie_id: int):
    movies = database.get_all_movies()

    target_movie = None

    for movie in movies:
        if movie["id"] == movie_id:
            target_movie = movie
            break

    if target_movie is None:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"movie": target_movie}
    )


# 映画編集処理
@app.post("/edit/{movie_id}")
def edit_movie(
    movie_id: int,
    title: str = Form(...),
    director: str = Form(...),
    genre: str = Form(...),
    year: int = Form(...),
    rating: int = Form(...)
):
    validate_movie_input(title, director, year, rating)
    
    database.update_movie(
        movie_id, 
        title, 
        director, 
        genre, 
        year, 
        rating
    )

    return RedirectResponse(url="/", status_code=303)


# 映画削除処理
@app.post("/delete/{movie_id}")
def delete_movie(movie_id: int):
    database.delete_movie(movie_id)

    return RedirectResponse(
        url="/",
        status_code=303
    )


@app.get("/api/movies")
def get_movies():
    #　映画一覧を取得するAPI

    movies = database.get_all_movies()

    return [dict(movie) for movie in movies]


#　映画詳細取得API
@app.get("/api/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = database.get_movie_by_id(movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="映画が見つかりません。"
        )

    return dict(movie)