from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory database
todo_list = []

# Pydantic model for a ToDo item
class ToDo(BaseModel):
    id: int
    title: str
    completed: bool = False

# Home route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI To-Do App"}

# Get all ToDos
@app.get("/todos", response_model=List[ToDo])
def get_todos():
    return todo_list

# Get ToDo by ID
@app.get("/todos/{todo_id}", response_model=ToDo)
def get_todo(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="ToDo not found")

# Create new ToDo
@app.post("/todos", response_model=ToDo)
def create_todo(todo: ToDo):
    todo_list.append(todo)
    return todo

# Update ToDo by ID
@app.put("/todos/{todo_id}", response_model=ToDo)
def update_todo(todo_id: int, updated_todo: ToDo):
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="ToDo not found")

# Delete ToDo by ID
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            del todo_list[index]
            return {"message": "ToDo deleted successfully"}
    raise HTTPException(status_code=404, detail="ToDo not found")
