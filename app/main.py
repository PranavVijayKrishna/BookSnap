from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello and Welcome to BookSnap!"}

@app.get("/about")
def about():
    return {"about": "BookSnap helps you find and manage books!"}

@app.get("/contact")
def contact():
    return {"email": "booksnap@gmail.com"}

@app.get("/hello/{name}")
def greeter(name: str):
    return {"message": f'Hello, {name}!'}

