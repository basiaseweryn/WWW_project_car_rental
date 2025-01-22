from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from rental.forms import SearchForm, BookingForm
from rental.models import Car, RentalRecord, City


def is_car_available(car, start_date, end_date):
    # Check for overlapping rental records
    overlapping_rentals = RentalRecord.objects.filter(
        car=car,
        start_date__lt=end_date,
        end_date__gt=start_date
    )
    return not overlapping_rentals.exists()

def search_view(request):
    form = SearchForm()
    return render(request, 'rental/search.html', {'search_form': form})

def results_view(request):
    context = {}
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            city = form.cleaned_data.get('city')

            cars_in_city = Car.objects.filter(city=city, is_available=True)
            available_cars = cars_in_city.exclude(
                rentalrecord__start_date__lt=end_date,
                rentalrecord__end_date__gt=start_date
            )

            context = {
                'available_cars': available_cars,
                'start_date': start_date,
                'end_date': end_date,
                'city': city,
                'search_form' : form
                }
            return render(request, 'rental/search_results.html', context)
    else:
        form = SearchForm()

    context['search_form'] = form
    return render(request, 'rental/search.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, RentalRecord
from .forms import BookingForm
from datetime import datetime


from django.utils.dateparse import parse_date

@login_required(login_url='login')
def book_car_view(request, car_id):

    #print("Request Path:", request.path)
    #print("GET parameters:", request.GET)

    car = get_object_or_404(Car, id=car_id)
    #print(car_id)
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    #print("Start Date (raw):", start_date_str)
    #print("End Date (raw):", end_date_str)

    if not start_date_str or not end_date_str:
        return redirect('search')


    date_format = '%Y-%m-%d'
    start_date = datetime.strptime(start_date_str, date_format)
    end_date = datetime.strptime(end_date_str, date_format)


    rental_days = (end_date - start_date).days or 1

    base_price = car.dailyPrice * rental_days

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            is_driver_under_25 = form.cleaned_data['is_driver_under_25']
            is_not_driver = form.cleaned_data['is_not_driver']
            add_insurance = form.cleaned_data['add_insurance']

            young_driver_fee = 10 * rental_days if is_driver_under_25 else 0
            insurance_fee = 0.2 * float(base_price) if add_insurance else 0
            total_price = float(base_price) + young_driver_fee + insurance_fee

            # Save the rental
            RentalRecord.objects.create(
                account=request.user,
                car=car,
                start_date=start_date,
                end_date=end_date,
                total_price=round(total_price, 2)
            )


            return render(request, 'rental/booking_done.html', {
                'car': car,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'rental_days': rental_days,
                'base_price': round(base_price, 2),
                'young_driver_fee': round(young_driver_fee, 2),
                'insurance_fee': round(insurance_fee, 2),
                'total_price': round(total_price, 2),
            })

    else:
        form = BookingForm()

    return render(request, 'rental/book_car.html', {
        'car': car,
        'form': form,
        'base_price': round(base_price, 2),
        'rental_days': rental_days
    })


def booking_done_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    base_price = request.GET.get('base_price')
    young_driver_fee = request.GET.get('young_driver_fee')
    insurance_fee = request.GET.get('insurance_fee')
    total_price = request.GET.get('total_price')

    return render(request, 'rental/booking_done.html', {
        'car': car,
        'start_date': start_date,
        'end_date': end_date,
        'base_price': base_price,
        'young_driver_fee': young_driver_fee,
        'insurance_fee': insurance_fee,
        'total_price': total_price,
    })



