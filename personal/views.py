from django.shortcuts import render

from rental.forms import SearchForm




def home_screen_view(request):
    form = SearchForm()
    return render(request, 'rental/search.html', {'form': form})