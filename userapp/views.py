from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.shortcuts import render
from .models import GPS
from adminapp.models import Login, Vechile_Register
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        print(email)
        print(password)

        try:
            user = Login.objects.get(email=email)
        except Login.DoesNotExist:
            messages.error(request, "❌ Invalid email or password.")
            return render(request, 'userapp/login.html')

        # Check hashed password
        if check_password(password, user.password):
            request.session['user_email'] = user.email  # store session manually
            messages.success(request, f"Welcome {user.username} 👋")
            return redirect('user_home')
        else:
            messages.error(request, "❌ Invalid email or password.")

    return render(request, 'userapp/login.html')



def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = Login.objects.get(email=email)
        except Login.DoesNotExist:
            messages.error(request, "❌ No account found with this email.")
            return render(request, 'userapp/forgot_password.html')

        # Generate new random password
        new_password = get_random_string(length=8)

        # Hash and save it
        user.password = make_password(new_password)
        user.save()

        # Send email
        try:
            subject = "Your Fleet Management Password Reset"
            message = (
                f"Hello {user.username},\n\n"
                f"Your password has been reset successfully.\n"
                f"Here is your new password:\n\n"
                f"🔑 {new_password}\n\n"
                f"Please log in and change it immediately.\n\n"
                f"Regards,\nFleet Management Team"
            )
            EmailMessage(subject, message, to = [email])
            messages.success(request, "✅ A new password has been sent to your email.")
        except Exception as e:
            messages.error(request, f"⚠️ Could not send email. ({e})")

    return render(request, 'userapp/forgot_password.html')


# Create your views here.

def user_home(request):
    email = request.session['user_email']
    if not email:
        return redirect("user_login")

    try:
        data = Login.objects.get(email=email)
        vechile_data = Vechile_Register.objects.filter(user_email=email)
        print(vechile_data)
    except ObjectDoesNotExist:
        return redirect("user_login")

    return render(request, 'userapp/index.html', {'user_data': data, "vechile_data" : vechile_data})




def gps_data_api(request):
    """Return latest GPS data for all vehicles of the logged-in user as JSON."""
    email = request.session.get('user_email')
    if not email:
        return JsonResponse({'error': 'User not logged in'}, status=401)

    # Get all vehicle numbers belonging to this user
    user_vehicles = Vechile_Register.objects.filter(user_email=email).values_list('vechile_number', flat=True)
    # Filter GPS data for those vehicles using __in
    data = list(
        GPS.objects.filter(vehicle_no__in=user_vehicles)
        .values('vehicle_no', 'lat', 'lon', 'speed', 'track_time')
    )

    return JsonResponse({'vehicles': data})

