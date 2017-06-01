from django.shortcuts import redirect, render
from clients.forms import RegisterForm


def index(request):
    return render(request, 'clients/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'clients/register.html', {'form': form})