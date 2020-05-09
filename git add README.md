Django Background Tasks
-------------------------------------------------------------------

install django 
--------------
command  => pip install django
-------------------------------------------------------------------

Installation
-------------
Install from PyPI:
command  =>  pip install django-background-tasks
-------------------------------------------------------------------

running following commands
--------------------------
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
-------------------------------------------------------------------

update settings.py
-------------------
Step2 : 
Add to INSTALLED_APPS:
	INSTALLED_APPS = (
		# ...
		'background_task',
		# ...
	)	
-------------------------------------------------------------------

enable templates in settings.py:
--------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
-------------------------------------------------------------------

create new app
--------------
python manage.py startapp billing
-------------------------------------------------------------------

add the app name in the settings.py
-----------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd Party App
    'background_task',

    # Apps:
    'billing',
]
-------------------------------------------------------------------

create new urls in the billing app
----------------------------------
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home')
]
-------------------------------------------------------------------

update the main urls.py file
-----------------------------
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('billing/', include('billing.urls'))
]
-------------------------------------------------------------------

update model file in billing
----------------------------
from django.db import models


# Create your models here.
class BillingModel(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    number_1 = models.IntegerField()
    number_2 = models.IntegerField()
    total = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "total : {total}".format(total=self.total)
-------------------------------------------------------------------

update views.py
---------------
from django.shortcuts import render
from .tasks import billingtask
from .forms import BillingForm

# Create your views here.
def home(request):
    template_name = 'billing_home.html'
    context = {}

    if request.method == 'POST':
        form = BillingForm(request.POST or None)
        if form.is_valid():
            # obj = form.save(commit=False)

            name = str(request.user)
            number_1 = form.cleaned_data['number_1']
            number_2 = form.cleaned_data['number_2']

            billingtask(name=name, number_1=number_1, number_2=number_2)
            form = BillingForm()
    else:
        form = BillingForm()

    context['form'] = form
    return render(request, template_name, context)
	
-------------------------------------------------------------------

create tasks.py file
--------------------
from background_task import background
from django.contrib.auth.models import User
from .models import BillingModel

@background(schedule=10)
def billingtask(name: str = 'admin', number_1: int = 0, number_2: int = 0):
    # lookup user by id and send them a message
    name = name
    number_1 = number_1
    number_2 = number_2
    total = number_1 + number_2
    print('name = ', name, ' number_1 = ', number_1, ' number_2 = ', number_2,' total = ', total)
    BillingModel.objects.create(name=name, number_1=number_1, number_2=number_2, total=total)
-------------------------------------------------------------------

create html file:
------------------

under billing create folder "template" and a file called billing_home.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form method="POST" action=".">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" name="submit" value="submit">
    </form>


</body>
</html>
-------------------------------------------------------------------

run command :
-------------
python manage.py process_tasks

run command : 
python manage.py runserver
-------------------------------------------------------------------

and run :
---------
python manage.py runserver