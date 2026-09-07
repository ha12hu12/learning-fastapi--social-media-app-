FROM python:3.11.3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 1- FROM      → الأساس الذي نبني عليه
# 2- WORKDIR   → مجلد الذي  نعمل فيه باقي الأكواد داخل الـ Container
# 3- COPY      → نسخ ملفات المشروع
# 4- RUN       → تنفيذ أمر أثناء بناء الـ Image
# 5- CMD       → الأمر الافتراضي عند تشغيل الـ Container