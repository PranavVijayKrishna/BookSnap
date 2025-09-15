from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
import pytesseract
import numpy as np
import cv2 as cv
from .api_handler import clean_raw_string, get_book_info

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

router2 = APIRouter(
    prefix = "/ocr",
    tags = ["ocr"],
)

@router2.get("/test2")
def test_preprocess():
    return {"message": "Preprocessing router connected!"}

# image cleanup 

@router2.post("/")
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

        extracted_text = pytesseract.image_to_string(processed_img)

        cleaned_text = clean_raw_string(extracted_text)

        api_result = get_book_info(cleaned_text)
        

        if isinstance(api_result, dict):
            title = api_result.get("title", "Title not found")
            return {"extracted_text": extracted_text, 
                    "cleaned text": cleaned_text,
                    "book info": api_result
                    }
        else:
            return{"Error": api_result}
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"An error occured during processing: {str(e)}")


    #return {"message": "Preprocessing done successfully!", "filename": file.filename}