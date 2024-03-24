# hate_speech
#open project folder in terminal and run the following commands: 
1.pip install virtualenvwrapper
2.mkvirtualenv hate-speech
3.workon hate-speech
4.https://github.com/UB-Mannheim/tesseract/wiki (go to this url and download the latest package and install. Add it in the environment variable)
5.pip install -r requirements.txt
6.python manage.py makemigrations
7.python manage.py migrate
8.python manage.py createsuperuser (follow instructions)
9.python manage.py runserver
10.Register
11.Login
To access the admin panel, go to http://localhost:8000/admin
