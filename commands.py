import os

os.system("pip install -r requirements.txt")
os.system("python manage.py makemigrations dukaanBanao")
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
