
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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
