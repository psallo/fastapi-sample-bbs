from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Form
from starlette.staticfiles import StaticFiles
import bbs_db as db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})


@app.get("/bbs")
def bbs(req: Request):
    return templates.TemplateResponse("bbs.html", {"request": req})


@app.get("/bbs_list")
def bbs_list(req: Request):
    rows = db.read_all()
    print(rows)
    return templates.TemplateResponse("bbs_list.html", {"request": req, "rows": rows})


@app.get("/bbs_read/{no}")
def bbs_list(req: Request, no: int):
    row = db.read_one(no)
    print(row)
    return templates.TemplateResponse("bbs_read.html", {"request": req, "row": row})


@app.get("/bbs_insert")
def bbs_insert_page(req: Request):
    return templates.TemplateResponse("bbs_insert.html", {"request": req})


@app.post("/bbs_insert")
def bbs_insert(req: Request,
               title: str = Form(...),
               content: str = Form(...),
               writer: str = Form(...)):
    data = ([title, content, writer])
    print(data)
    db.bbs_insert(data)
    return RedirectResponse(url="bbs_list", status_code=303)


@app.get("/bbs_update/{no}")
def bbs_update_page(req: Request, no: int):
    row = db.read_one(no)
    return templates.TemplateResponse("bbs_update.html", {"request": req, "row": row})


@app.post("/bbs_update")
def bbs_update(req: Request,
               no: int = Form(...),
               title: str = Form(...),
               content: str = Form(...),
               writer: str = Form(...)):
    data = ([title, content, no])
    db.update(data)
    return RedirectResponse(url="bbs_list", status_code=303)


@app.post("/bbs_delete")
def delete(req: Request, no: int = Form(...)):
    db.delete(no)
    return RedirectResponse(url="bbs_list", status_code=303)


@app.get("/bbs_search")
def bbs_search(req: Request, q: str):
    print("서버에서 받은 q값>> ",q)
    rows = db.bbs_search(q)
    return templates.TemplateResponse("bbs_list.html", {"request": req, "rows": rows})

@app.get("/chart")
def chart(req: Request):
    return templates.TemplateResponse("chart.html", {"request": req})