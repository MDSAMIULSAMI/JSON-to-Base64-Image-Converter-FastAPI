from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import pytesseract

app = FastAPI()

class JSONData(BaseModel):
    data: dict

def json_to_base64(json_data: dict) -> str:
    text = "\n".join(f"{key}: {value}" for key, value in json_data.items())
    image = Image.new('RGB', (500, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    draw.text((10, 10), text, fill=(0, 0, 0), font=font)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return base64_image

def base64_to_text(base64_image: str) -> str:
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text.strip()

@app.post("/convert")
def process_json(json_input: JSONData):
    try:
        base64_image = json_to_base64(json_input.data)
        extracted_text = base64_to_text(base64_image)
        return {"base64_image": base64_image, "extracted_text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
