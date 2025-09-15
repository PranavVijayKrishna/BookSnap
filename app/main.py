from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from . import preprocess
from . import ocr

app = FastAPI()

app.include_router(preprocess.router)
app.include_router(ocr.router2)

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
    # file size calc
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file_size_mb = file_size / (1024 ** 2)
    file.file.seek(0)

    try:
        # reading file into memory
        file_content = await file.read()
        in_memory_file = BytesIO(file_content)

        # open as image
        image = Image.open(in_memory_file)

        image_format = image.format
        image_height = image.height
        image_width = image.width
    
    except UnidentifiedImageError:
        raise HTTPException(status_code = 400, detail = "Please upload an image file.")

    return {"message": "File received!", 
            "filename": file.filename, 
            "size in bytes": file_size, 
            "size in megabytes": round(file_size_mb, 2), 
            "image format": image_format,
            "image width": image_width,
            "image height": image_height}

    