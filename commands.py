import os

os.system("python manage.py makemigrations dukaanBanao")
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")