
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import main

#FastAPIのインスタンスの作成
app = FastAPI()

#HTMLテンプレートを読み込むフォルダを指定
templates = Jinja2Templates(directory="templates")

#CSSなどの静的ファイルを読み込む
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


#映画一覧画面
@app.get("/")
def index(request: Request):

    #映画データを読み込む
    movies = main.load_movies()

    #データが正常なリストでない場合は空のリストにする
    if not isinstance(movies, list):
        movies = []

    # HTMLに映画データを渡す
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "movies": movies
        }
    )


#映画登録画面
@app.get("/add")
def show_add_form(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="add.html",
        context={
            "error": None
        }
    )


#映画登録処理
@app.post("/add")
def add_movie(
    request: Request,
    title: str = Form(...),
    director: str = Form(""),
    genre: str = Form(""),
    year: int = Form(...),
    rating: int = Form(...)
):

    success = main.add_movie_record(
        title,
        director,
        genre,
        year,
        rating
    )

    if not success:
        return templates.TemplateResponse(
            request=request,
            name="add.html",
            context={
                "error": "映画の登録に失敗しました。入力内容を確認してください。"
            },
            status_code=400
        )

    return RedirectResponse(
        url="/",
        status_code=303
    )