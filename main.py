from os import name

from fastapi import FastAPI,HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel
app=FastAPI()

class User(BaseModel):
    id: int
    name: str
    age: int

class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


users=[
    {'id': 1, 'name': 'Alex', 'age': 30,},
    {'id': 2, 'name': 'John', 'age': 24},
    {'id': 3, 'name': 'Bob', 'age': 43},
    {'id': 4, 'name': 'Maxim', 'age': 64},
    {'id': 5, 'name': 'Alex', 'age': 87}
]

posts=[
    {'id': 1,'title': 'News 1','body': 'Text1','author': users[0]},
    {'id': 2,'title': 'News 2','body': 'Text2','author': users[1]},
    {'id': 3,'title': 'News 3','body': 'Text3','author': users[2]},
    { 'id': 4,'title': 'News 4','body': 'Text4','author': users[3]},
    {'id': 5,'title': 'News 5','body': 'Text5','author': users[4]},
]


@app.get("/")
def home() -> list:
    #return {"Data": "message"}
    #return "Hello World"
    a=[]
    for i in range(1,10):
       a.append(i)
    return a

@app.get("/contact")
async def contact()-> int:
    return  404

# @app.get("/items")
# async def items() -> List[Post]:
#     post_obj=[]
#     for i in posts:
#         post_obj.append(id=i['id'],title=i['title'],body=i['body'])
#     return post_obj



@app.get("/items")
async def items() -> List[Post]:
    return [Post(**i) for i in posts]

@app.get("/items/{id}")
async def items(id: int=1) -> dict:
    for i in posts:
        if i['id'] == id:
            # return i
            return Post(**i)
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/search/")
async def search(post_id: Optional[int]=None)-> Dict[str,Optional[Post]]:
    if post_id:
        for i in posts:
            if i['id']==post_id:
                # return i
                return {"data": Post(**i)}
        raise HTTPException(status_code=404,detail="Post not found")
    else:
        return {"data":"No posts id provided"}