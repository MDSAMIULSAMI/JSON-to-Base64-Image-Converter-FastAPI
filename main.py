from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
import io
import base64
import pytesseract
import json

app = FastAPI()

class Base64Image(BaseModel):
    image_data: str

def base64_to_text(base64_image: str) -> str:
    try:
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/extract-json")
def extract_json_from_image(image_input: Base64Image):
    try:
        extracted_text = base64_to_text(image_input.image_data)
        structured_data = json.loads(extracted_text)
        return {"structured_data": structured_data}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Extracted text is not a valid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
