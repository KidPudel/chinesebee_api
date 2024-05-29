from cnocr import CnOcr

def rate_accuracy(image: str, target: str):
    ocr = CnOcr
    out = ocr.ocr(img_fp=image)
    print(out)
    return {
        "success": True
    }