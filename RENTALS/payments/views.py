from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from .models import Payment
from .forms import PaymentForm
from properties.models import Property

def payment_list(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payments:payment_list')
    else:
        form = PaymentForm()

    payments = Payment.objects.all().order_by('-date')
    
    return render(request, 'payments/payments_view.html', {
        'payments': payments,
        'form': form,
    })