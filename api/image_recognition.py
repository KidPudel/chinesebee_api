from cnocr import CnOcr
import base64
from PIL import Image
from io import BytesIO
import logging

def score_accuracy(image: str, target: str):
    try:
        cleared_image = image.split(',')[1]
        decoded_image = base64.b64decode(cleared_image)
        
        img = Image.open(BytesIO(decoded_image))
        
        ocr = CnOcr(rec_model_name="densenet_lite_136-gru")
        out = ocr.ocr(img_fp=img)
        print(out)
        if len(out) == 0 or out[0]["text"] != target:
            return {
                "success": True,
                "score": 0
            }
        
        
        return {
            "success": True,
            "score": out[0]["score"]
        }
    except Exception as e:
        print(e)
        logging.error("FUCK")
        logging.error(e)
        
    