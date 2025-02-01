from django.shortcuts import render
from .models import Photo
from django.shortcuts import redirect
from .forms import PhotoForm
from django.shortcuts import get_object_or_404


def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photos/photo_list.html', {'photos': photos})


def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'photos/upload_photo.html', {'form': form})


def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        photo.delete()
        return redirect('photo_list')
    return render(request, 'photos/delete_photo.html', {'photo': photo})