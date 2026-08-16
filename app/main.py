from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.api import users
from app.api import records
from app.api import categories
import app.models
from app.database import Base, engine

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(users.router)
app.include_router(records.router)
app.include_router(categories.router)

Base.metadata.create_all(bind=engine)

def render_page(request: Request, template_name: str):
    """指定されたHTMLテンプレートを返す。"""
    return templates.TemplateResponse(request=request, name=template_name)


@app.get("/", include_in_schema=False)
def home():
    """最初に開く画面をログイン画面へ案内する。"""
    return RedirectResponse(url="/login", status_code=302)


@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request):
    return render_page(request, "login.html")


@app.get("/register", response_class=HTMLResponse, include_in_schema=False)
def register_page(request: Request):
    return render_page(request, "register.html")


# /records/ は既存のJSON APIなので、画面用URLは末尾スラッシュなしにする。
@app.get("/records", response_class=HTMLResponse, include_in_schema=False)
def records_page(request: Request):
    return render_page(request, "records.html")


@app.get("/record-detail", response_class=HTMLResponse, include_in_schema=False)
def record_detail_page(request: Request):
    return render_page(request, "record-detail.html")


@app.get("/record-form", response_class=HTMLResponse, include_in_schema=False)
def record_form_page(request: Request):
    return render_page(request, "record-form.html")


# /categories/ は既存のJSON APIなので、画面用URLは末尾スラッシュなしにする。
@app.get("/categories", response_class=HTMLResponse, include_in_schema=False)
def categories_page(request: Request):
    return render_page(request, "categories.html")


@app.get("/category-form", response_class=HTMLResponse, include_in_schema=False)
def category_form_page(request: Request):
    return render_page(request, "category-form.html")


@app.get("/settings", response_class=HTMLResponse, include_in_schema=False)
def settings_page(request: Request):
    return render_page(request, "settings.html")
