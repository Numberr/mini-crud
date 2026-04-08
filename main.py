import uvicorn
from fastapi import FastAPI, Query, HTTPException
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from models import UserResponse, UserCreate, UpdateRequest
from database import get_conn
from datetime import datetime


tags_metadata = [{"name": "products","description": "Операции с товарами",},{"name": "users","description": "Управление пользователями",},]

app = FastAPI(title='USERS TEST', openapi_tags=tags_metadata)

@app.post('/users', 
        response_model=UserResponse, 
        tags=['users'], 
        status_code=201
        )
async def create_user(payload: UserCreate):
    payload_dict = payload.model_dump()

    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                'insert into lesson_1.users (name, lastname, password, birthday) values (%s, %s, %s, %s) RETURNING id', 
                (payload_dict['name'], 
                 payload_dict['lastname'], 
                 payload_dict['password'], 
                 payload_dict['birthday']
                 )
                )
            payload_dict.update({
                            'id': cursor.fetchone()['id'],
                            'success': True,
                            'action_time': datetime.now()
                        })
            
        conn.commit()

    return payload_dict

@app.get('/users', 
        tags=['users'],
        response_model=UserResponse,
        status_code=200,
        )
async def get_user(
    id: int = Query(gt=0)
    ):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                'select * from lesson_1.users where id = %s', (id,)
            )
            data_dict = cursor.fetchone()

    if not data_dict:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    
    data_dict.update({
        'success': True,
        'action_time': datetime.now()
    })

    return data_dict

@app.put('/users',
        response_model=UserResponse, 
        tags=['users'], 
        status_code=200
        )
async def update_user(payload: UpdateRequest):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                sql.SQL("UPDATE lesson_1.users SET {} = %s WHERE id = %s RETURNING *").format(
                    sql.Identifier(payload.param_to_update)
                ),
                (payload.new_value, payload.id)
            )
            data = cursor.fetchone()

        if not data:
            raise HTTPException(status_code=404, detail='Пользователь не найден')
        
        data.update({
            'success': True,
            'action_time': datetime.now()
        })

        conn.commit()

    return data

@app.delete('/users',
            tags=['users'],
            status_code=200)
async def delete_user(id: int):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                'delete from lesson_1.users where id = %s', (id,)
            )

            if cursor.rowcount == 0:  # ни одна строка не удалена
                raise HTTPException(status_code=404, detail='Пользователь не найден')

        conn.commit()

    return {'success': True}


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)