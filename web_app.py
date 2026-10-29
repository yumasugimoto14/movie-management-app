
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

#FastAPIのインスタンスの作成
app = FastAPI()

#HTMLテンプレートを読み込むフォルダを指定
templates = Jinja2Templates(directory="templates")


#トップページ
@app.get("/")
def index(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
