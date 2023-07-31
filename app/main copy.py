from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=5e13bbbb", row_factory=dict_row)
        cursor = conn.cursor()
        print('Succesfully connected to the database.')
        break
    except Exception as error:
        time.sleep(2)
        print('Failed to connect to the database.')
        print('Error: ', error)


my_posts = [{'title': 'title of post', 'content': 'content of post', 'id': 1}, 
            {'title': 'favorite foods', 'content': 'I love pizza', 'id': 2}]


def find_post(id):
    for n, post in enumerate(my_posts):
        if post['id'] == id:
            print(n)
            return post, n
        return None, None


@app.get('/')
async def root():
    return {'message': 'Hello World !!'}


@app.get('/posts')
def get_post():
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute('INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *', 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute('SELECT * FROM posts WHERE id = %s', (str(id),))
    returned_post = cursor.fetchone()
    if not returned_post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id: {id} was not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return {'data': returned_post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('DELETE FROM posts WHERE id = %s RETURNING *', (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *', (post.title, post.content, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    return {'data': updated_post}
