
from fastapi import FastAPI, Request, Form, HTTPException
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


#映画データの読み込み
main.movies = main.load_movies() or []


#映画一覧画面
@app.get("/")
def index(request: Request):
    # HTMLに映画データを渡す
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"movies": main.movies}
    )


#映画登録画面の表示
@app.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add.html",
        context={}
    )


#映画登録処理
@app.post("/add")
def add_movie(
    request: Request,
    title: str = Form(...),
    director: str = Form(...),
    genre: str = Form(...),
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

    if success:
        return RedirectResponse(
                url="/",
                status_code=303
        )
    
    return templates.TemplateResponse(
        request=request,
        name="add.html",
        context={"error": "映画の登録に失敗しました。"},
        status_code=400
    )


#映画編集画面の表示
@app.get("/edit/{movie_id}")
def edit_page(request: Request, movie_id: int):

    #編集対象の映画を探す
    movie = None

    for item in main.movies:
        if item["id"] == movie_id:
            movie = item
            break

    #映画が見つからなかった場合
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="映画が見つかりません。"
        )

    #編集画面を表示
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"movie": movie}
    )


#　映画情報の更新処理
@app.post("/edit/{movie_id}")
def update_movie(
    request: Request,
    movie_id: int,
    title: str = Form(...),
    director: str = Form(...),
    genre: str = Form(...),
    year: int = Form(...),
    rating: int = Form(...)
):

    success = main.update_movie_record(
        movie_id,
        title,
        director,
        genre,
        year,
        rating
    )

    #　更新に成功した場合
    if success:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    #　更新に失敗した場合
    movie = None

    for item in main.movies:
        if item["id"] == movie_id:
            movie = item
            break

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="映画が見つかりません。"
        )

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "movie": movie,
            "error": "映画情報の更新に失敗しました。"
        },
        status_code=400
    )


#　映画削除処理
@app.post("/delete/{movie_id}")
def delete_movie(movie_id: int):

    success = main.delete_movie_record(movie_id)

    if success:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    raise HTTPException(
        status_code=404,
        detail="映画の削除に失敗しました。映画が存在しないか、保存に失敗した可能性があります。"
    )