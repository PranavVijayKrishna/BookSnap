from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
import pytesseract
import numpy as np
import cv2 as cv

router = APIRouter(
    prefix = "/preprocess",
    tags = ["Preprocessing"],
)

@router.get("/test")
def test_preprocess():
    return {"message": "Preprocessing router connected!"}

# image cleanup 

@router.post("/")
async def preprocess(file: UploadFile):
    try:
        # reading file into memory
        file_content = await file.read()
        #in_memory_file = BytesIO(file_content)
        
        np_array = np.frombuffer(file_content, np.uint8)

        image = cv.imdecode(np_array, cv.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code = 400, detail = "Invalid image file. Please upload a valid image file.")
            
        #preprocessing
        
        gray_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        scale = 150 # 1.5x magnification
        width = int(image.shape[1] * scale / 100)
        height = int(image.shape[0] * scale / 100)
        resized_img = cv.resize(gray_img, (width, height))

        blurred_img =cv.GaussianBlur(resized_img, (5, 5), 0)
        (T, processed_img) = cv.threshold(blurred_img, 127, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        success, buffer = cv.imencode(".jpg", processed_img) # returns a tuple 
        if not success:
            raise HTTPException(status_code = 500, detail = "Failed to encode image.")
        
        io_stream = BytesIO(buffer)

        return StreamingResponse(io_stream, media_type="image/jpeg")
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"An error occured during processing: {str(e)}")


    #return {"message": "Preprocessing done successfully!", "filename": file.filename}