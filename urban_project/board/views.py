from django.shortcuts import render, redirect
from board.models import Advertisement
from board.forms import AdvertisementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from .models import Profile


def logout_view(request):
    logout(request)
    return redirect('home')

#from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})

def advertisement_detail(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})

@login_required
def add_advertisement(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})

@login_required
def edit_advertisement(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        if form.is_valid():
            form.instance.author = request.user
            form.save()

            return redirect('board:advertisement_detail', pk=advertisement.pk)
            # return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'board/edit_advertisement.html', {'form': form, 'advertisement': advertisement})

@login_required
def delete_advertisement(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)
    if request.method == "POST":
        advertisement.delete()
        return redirect('board:advertisement_list')
    return render(request, 'board/delete_advertisement.html', {'advertisement': advertisement})


@login_required
def like_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)

    if request.user.profile:
        if request.user in advertisement.likes.all():
            advertisement.likes.remove(request.user)
        else:
            advertisement.likes.add(request.user)

        # Update stats
        request.user.profile.total_likes += 1 if request.user not in advertisement.likes.all() else -1
        request.user.profile.save()
    else:
        # Handle case where user doesn't have a profile
        pass

    return redirect('board:advertisement_detail', pk=advertisement.pk)

@login_required
def dislike_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)

    if request.user.profile:
        if request.user in advertisement.dislikes.all():
            advertisement.dislikes.remove(request.user)
        else:
            advertisement.dislikes.add(request.user)

    # Update stats
        advertisement.author.profile.total_dislikes += 1 if request.user not in advertisement.dislikes.all() else -1
        advertisement.author.profile.save()
    else:
        pass
    return redirect('board:advertisement_detail', pk=advertisement.pk)
