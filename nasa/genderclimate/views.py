from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserForm
from healthfacilities.views import search_health_facilities



def home_view(request):
# Example data for counts
    users_count = 100
    doctors_count = 20
    facilities_count = 80
    
    context = {
        'users_count': users_count,
        'doctors_count': doctors_count,
        'facilities_count': facilities_count,
    }

    return render(request, 'home.html', context)


def user_register_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # save both User and UserProfile data
            return redirect('login')
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})


def search_area(request):
    query = request.GET.get('query', '')
    area = request.GET.get('area', '')

    return redirect(f'/healthfacilities/search/?query={query}&area={area}')


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})
