from fastapi import FastAPI,Request,Depends,Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from db import Base,engine,get_db
from models import Game

Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static/",StaticFiles(directory="static"),name="static")


@app.get("/")
def home(request:Request, db:Session=Depends(get_db)):
    games = db.query(Game).all()
    return templates.TemplateResponse(
        "index.html",{"request":request,"games":games}
    )

@app.get("/game/{game_id}")
def item(request:Request,game_id:int,db:Session=Depends(get_db)):
    game = db.query(Game).filter(Game.id==game_id).first()
    return templates.TemplateResponse(
        "game.html",{"request":request,"game":game}
    )

@app.post("/game")
def create(title:str=Form(...),genre:str=Form(...),image:str=Form(...),db:Session=Depends(get_db)):
    new_g = Game(title=title,genre=genre,image=image)
    db.add(new_g)
    db.commit()
    db.refresh(new_g)
    return RedirectResponse("/",status_code=303)

