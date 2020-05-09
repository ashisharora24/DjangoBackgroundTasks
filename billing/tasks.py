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