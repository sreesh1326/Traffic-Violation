from ultralytics import YOLO
import easyocr
import cv2
import numpy as np
import base64

model = YOLO("models/best.pt")
reader = easyocr.Reader(['en'], gpu=True)

def run_detection(image_bytes: bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    immg = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    results = model(img, conf=.4)[0]

    violations = []
    license_plate = None

    for box in results.boxes:
        cls_name = results.names[int(box.cls[0])]
        conf = float(box.conf[0])

        if cls_name == "license_plate":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            plate_region = img[y1:y2, x1:x2]
            ocr_result = reader.readtext(plate_region)
            if ocr_result:
                license_plate = ocr_result[0][1]
            else:
                violations.append({
                    "violations_type": cls_name,
                    "confidence": round(conf, 2),
                    "license_plate": None
                })

    if license_plate and violations:
        for v in violations:
            v["license_plate"] = license_plate
    
    annotated = results.plot()
    _, buffer = cv2. imencode('.jpg', annotated)
    annoted_b64 = base64.b64encode(buffer).decode('utf-8')

    return violations, annotated_b64