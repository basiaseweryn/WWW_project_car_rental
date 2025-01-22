from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from account.forms import RegisterForm, AccountAuthentificationForm, AccountUpdateForm
from account.models import Account
from rental.models import RentalRecord


def register_view(request):
    context = {}
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  #not necessary since False is default, but just in case
            user.save()

            #account activation email

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

            subject = 'Activate Your Account'
            message = f'Hi {user.username},\n\nClick the link to activate your account:\n{activation_link}'

            send_mail(
                subject,
                message,
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )

            return render(request, 'account/activation_sent.html')
        else:
            context['register_form'] = form
    else:
        form = RegisterForm()
        context['register_form'] = form
    return render(request, 'account/register.html', context)

User = get_user_model()

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'account/activation_success.html')
    else:
        return HttpResponse('Activation link is invalid or expired.', status=400)

def password_reset_request_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        account = Account.objects.filter(email=email).first()

        if account:
            token = default_token_generator.make_token(account)
            uid = urlsafe_base64_encode(force_bytes(account.pk))

            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            subject = 'Password Reset Requested'
            message = f"Hi {account.username},\n\nClick the link below to reset your password:\n{reset_link}"

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [account.email])

            messages.success(request, "Password reset link sent to your email.")
            return redirect('password_reset_sent')
        else:
            messages.error(request, "No account found with that email.")

    return render(request, 'account/password_reset.html')

def password_reset_sent_view(request):
    return render(request, 'account/password_reset_sent.html')


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        account = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        account = None

    if account and default_token_generator.check_token(account, token):
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 and password2 and password1 == password2:
                account.set_password(password1)
                account.save()
                messages.success(request, "Password has been reset. You can now log in.")
                print("Password has been reset. You can now log in.")
                return redirect('password_reset_complete')
            else:
                messages.error(request, "Passwords do not match.")

        return render(request, 'account/password_reset_confirm.html', {'validlink': True})
    else:
        messages.error(request, "The password reset link is invalid or expired.")
        return render(request, 'account/password_reset_confirm.html', {'validlink': False})



def password_reset_complete_view(request):
    return render(request, 'account/password_reset_complete.html')



def logout_view(request):
    logout(request)
    return redirect("search")

def login_view(request):
    context = {}
    user= request.user
    if user.is_authenticated:
        return redirect("search")
    if request.POST:
        form = AccountAuthentificationForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("search")

    else:
        form = AccountAuthentificationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)




@login_required(login_url='login')
def rental_history_view(request):
    rentals = RentalRecord.objects.filter(account=request.user)

    return render(request, 'account/rental_history.html', {
        'rentals': rentals
    })

@login_required(login_url='login')
def rental_history_xml(request):
    rentals = RentalRecord.objects.filter(account=request.user)

    response = HttpResponse(content_type='application/xml')
    response['Content-Disposition'] = 'inline; filename="rental_history.xml"'

    response.write('<?xml version="1.0"?>\n')
    response.write('<?xml-stylesheet type="text/xsl" href="/static/rental_history.xsl"?>\n')
    response.write('<RentalHistory>\n')

    for rental in rentals:
        response.write('  <Rental>\n')
        response.write(f'    <Car>{rental.car.brand} {rental.car.model}</Car>\n')
        response.write(f'    <StartDate>{rental.start_date}</StartDate>\n')
        response.write(f'    <EndDate>{rental.end_date}</EndDate>\n')
        response.write(f'    <TotalPrice>{rental.total_price}</TotalPrice>\n')
        response.write('  </Rental>\n')

    response.write('</RentalHistory>')
    return response


@login_required
def account_view(request):
    current_date = datetime.now()
    upcoming_bookings = RentalRecord.objects.filter(account=request.user, start_date__gte=current_date).order_by('start_date')

    cancellable_bookings = upcoming_bookings.filter(start_date__gt=current_date + timedelta(days=7))

    return render(request, 'account/account.html', {
        'upcoming_bookings': upcoming_bookings,
        'cancellable_bookings': cancellable_bookings,
    })


@login_required
def cancel_booking(request, booking_id):
    booking = RentalRecord.objects.get(id=booking_id, account=request.user)

    #start_date.strftime('%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d')
    if booking.start_date.strftime('%Y-%m-%d') > (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'):
        booking.delete()
        return redirect('account')

    return HttpResponseForbidden("You cannot cancel a booking within 7 days of the rental.")


