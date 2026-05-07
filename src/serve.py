from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import joblib
import os

app = FastAPI()

# Đọc tên bucket từ biến môi trường (được đặt trong systemd service)
S3_BUCKET = os.environ["CLOUD_BUCKET"]
S3_MODEL_KEY = "models/latest/model.pkl"
MODEL_PATH = os.path.expanduser("~/models/model.pkl")

LABEL_MAP = {0: "thấp", 1: "trung_bình", 2: "cao"}


def download_model():
    """Tải file model.pkl từ S3 về máy khi server khởi động."""
    # TODO 2.6.1: Tạo boto3 S3 client
    s3 = boto3.client("s3")

    # TODO 2.6.2-2.6.4: Download file model từ S3 về local
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    s3.download_file(S3_BUCKET, S3_MODEL_KEY, MODEL_PATH)

    # TODO 2.6.5: In thông báo thành công
    print(f"Model downloaded from s3://{S3_BUCKET}/{S3_MODEL_KEY} → {MODEL_PATH}")


# Gọi hàm này khi module được import (chạy khi server khởi động)
download_model()
model = joblib.load(MODEL_PATH)


class PredictRequest(BaseModel):
    features: list[float]


@app.get("/health")
def health():
    """Endpoint kiểm tra sức khỏe server. GitHub Actions dùng endpoint này để xác nhận deploy thành công."""
    # TODO 2.6.6: Trả về dict {"status": "ok"}
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    """
    Endpoint suy luận.

    Đầu vào: JSON {"features": [f1, f2, ..., f12]}
    Đầu ra:  JSON {"prediction": <0|1|2>, "label": <"thấp"|"trung_bình"|"cao">}

    Thứ tự 12 đặc trưng (khớp với FEATURE_NAMES trong tests):
        fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
        chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density,
        pH, sulphates, alcohol, wine_type
    """
    # TODO 2.6.7: Kiểm tra số lượng đặc trưng
    if len(req.features) != 12:
        raise HTTPException(status_code=400, detail="Expected 12 features (wine quality)")

    # TODO 2.6.8: Gọi model.predict([req.features]) để lấy kết quả dự đoán
    prediction = int(model.predict([req.features])[0])

    # TODO 2.6.9: Trả về dict chứa "prediction" (int) và "label" (string)
    return {"prediction": prediction, "label": LABEL_MAP[prediction]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
