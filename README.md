<p>
  <a href="https://exarth.com/">
  <img src="https://exarth.com/static/exarth/theme/logo-red-1000.svg" height="150">
  </a>
</p>
<hr>

# Realtime-Chat
### REDIS, DJANGO CHANNELS, HTMX

#### Getting the files
Download zip file or <br>
Clone with git + remove git folder

<br><br><br>

## Setup

#### - Create Virtual Environment
###### # Mac
```
python3 -m venv venv
source venv/bin/activate
```

###### # Windows
```
pip install virtualenv 
virtualenv venv 
venv\Scripts\activate.bat 
```

<br>

#### - Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

<br>

#### - Migrate to database
```
python manage.py migrate
python manage.py createsuperuser
```

<br>

#### - Run application
```
python manage.py runserver
```

<br>

#### - Generate Secret Key ( ! Important for deployment ! )
```
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
exit()
```


