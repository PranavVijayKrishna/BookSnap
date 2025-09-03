from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
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

@app.post("/upload")
async def create_upload_file(file: UploadFile):
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file_size_mb = file_size / (1024 ** 2)
    file.file.seek(0)

    file_content = await file.read()
    in_memory_file = BytesIO(file_content)

    image = Image.open(in_memory_file)

    image_format = image.format
    image_height = image.height
    image_width = image.width

    return {"message": "File received!", 
            "filename": file.filename, 
            "size in bytes": f'{file_size:.2f}', 
            "size in megabytes": f'{file_size_mb:.2f}', 
            "image format": image_format,
            "image widht": image_width,
            "image height": image_height}

    