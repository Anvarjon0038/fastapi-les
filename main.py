from fastapi import FastAPI,HTTPException,Path,Query,Body
from typing import Optional, List, Dict,Annotated

from fastapi.params import Body
from pydantic import BaseModel,Field
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


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


class CreateUser(BaseModel):
    name: Annotated[
        str, Field(...,title='User name',min_length=3,max_length=15),
    ]
    age: Annotated[int,Field(...,title='User age',ge=1,le=120)]


users=[
    {'id': 1, 'name': 'Amin', 'age': 30,},
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

@app.post("/items/add")
async def add_item(post: PostCreate)-> Post:
    a=next((i for i in users if i['id']==post.author_id),None)
    if not a:
        raise HTTPException(status_code=404,detail='User not found')

    new_post_id=len(posts)+1
    new_post=({'id':new_post_id,'title': post.title,'body': post.body,'author':a})
    posts.append(new_post)

    return  Post(**new_post)

@app.get("/items/{id}")
async def items(id: Annotated[int,Path(...,title='post id',ge=1,lt=100)]) -> Post:
    for i in posts:
        if i['id'] == id:
            # return i
           return Post(**i)
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/user/add")
async def user_add(user: Annotated[
    CreateUser,
    Body(...,example={
        "name": "Username",
        "age": 1
    })
])-> User:

    new_user_id=len(users)+1
    new_user=({'id':new_user_id,'title': user.name,'age': user.age})
    users.append(new_user)

    return  User(**new_user)

@app.get("/search/")
async def search(post_id: Annotated[
    Optional[int],
    Query(title='id of post to search',ge=1,le=40)
])-> Dict[str,Optional[Post]]:
    if post_id:
        for i in posts:
            if i['id']==post_id:
                # return i
                return {"data": Post(**i)}
        raise HTTPException(status_code=404,detail="Post not found")
    else:
        return {"data":"No posts id provided"}

