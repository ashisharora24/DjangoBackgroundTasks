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