from fastapi import FastAPI

app = FastAPI()

#get - to get info from server
#post - create something new
#put - changing existing things
#delete - deleting

# all_to_dos = [
#     {'todo_id': 1, "todo_name": "sports", "todo_descrip": "gym"},
#     {'todo_id': 2, "todo_name": "shop", "todo_descrip": "buy clothes"},
#     {'todo_id': 3, "todo_name": "study", "todo_descrip": "do Hw"},
#     {'todo_id': 4, "todo_name": "eat", "todo_descrip": "Make dinner"}
# ]

# @app.get("/")
# def index():
#     return {"message": "Hello World"}

# @app.get("/todos/{todo_id}")
# def get_todo(todo_id: int):
#     for todo in all_to_dos:
#         if todo['todo_id'] == todo_id:
#             return {'result': todo}
        
# @app.get("/todos")
# def get_todo(first_n: int = None):
#     if first_n:
#         return all_to_dos[:first_n]
#     else:
#         return all_to_dos
    
# @app.post('todos')
# def create_todo(todo: dict):
#     new_todo_id = max(todo['todo_id'] for todo in all_to_dos) + 1
#     new_todo = {'todo_id': new_todo_id, 
#                 "todo_name": todo['todo_name'], 
#                 "todo_descrip": todo['todo_descrip']},

#     all_to_dos.append(new_todo)
#     return new_todo

# @app.put('/todos/{todo_id}')
# def update_todo(todo_id: int, updated_todo: int):
#     for todo in all_to_dos:
#         if todo['todo_id'] == todo_id:
#             pass