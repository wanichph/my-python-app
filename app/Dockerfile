# 1. เลือก Base Image ที่มีขนาดเล็กและเสถียร
FROM python:3.11-slim

# 2. กำหนด Environment Variables เพื่อเพิ่มความเร็วและการทำงานของ Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000

# 3. กำหนดโฟลเดอร์ทำงานหลักใน Container
WORKDIR /app

# 4. ติดตั้ง System Dependencies ที่จำเป็น (ถ้ามี)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. คัดลอก requirements.txt และติดตั้ง Python Packages
# (แยกขั้นตอนเพื่อประโยชน์ของ Docker Layer Cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 6. คัดลอก ซอร์สโค้ด ทั้งหมดเข้า Container
COPY . .

# 7. สร้างและเปลี่ยนไปใช้ Non-root User เพื่อความปลอดภัย
RUN useradd -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 8. เปิด พอร์ต สำหรับรับทราฟฟิก
EXPOSE 5000

# 9. สั่งรันแอปด้วย Production WSGI Server (Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
