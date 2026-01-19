from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.shortcuts import render
from .models import CurrentTable
from adminapp.models import UserProfile, Vechile_Register
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout


@never_cache
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, "❌ Invalid email or password.")
            return render(request, "userapp/user_login.html")

        # Check if UserProfile exists
        if not hasattr(user, 'profile'):
            messages.error(request, "❌ Profile not found. Contact admin.")
            return render(request, "userapp/user_login.html")

        profile = user.profile
        status = profile.account_status

        # Handle different account statuses
        if status == "Pending":
            messages.warning(request, "⏳ Your account is pending approval. Please wait for admin approval.")
            return render(request, "userapp/user_login.html")
        elif status == "Rejected":
            messages.error(request, "❌ Your account has been rejected. Contact support.")
            return render(request, "userapp/user_login.html")
        elif status == "Approved":
            # Login successful
            login(request, user)
            messages.success(request, f"Welcome {user.get_full_name() or user.get_username()} 👋")
            return redirect("user_home")
        else:
            messages.error(request, "❌ Unknown account status. Contact support.")
            return render(request, "userapp/user_login.html")

    # GET request
    return render(request, "userapp/user_login.html")




@never_cache
@login_required(login_url="user_login")
def user_home(request):
    # Get the currently logged-in user
    user = request.user

    # Try to get UserProfile, handle missing profile gracefully
    try:
        profile = user.profile
    except ObjectDoesNotExist:
        # If profile doesn't exist, redirect or show error
        return redirect("user_login")

    # Fetch vehicles registered by this user
    vechile_data = Vechile_Register.objects.filter(user=user)

    return render(
        request,
        'userapp/user_index.html',
        {
            'user_data': profile,       # pass profile instead of old Login table
            'vechile_data': vechile_data
        }
    )








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






def gps_data_api(request):
    """Return latest GPS data for all vehicles of the logged-in user as JSON."""
    email = request.session.get('user_email')
    if not email:
        return JsonResponse({'error': 'User not logged in'}, status=401)

    # Get all vehicle numbers belonging to this user
    user_vehicles = Vechile_Register.objects.filter(user_email=email).values_list('vechile_number', flat=True)
    # Filter GPS data for those vehicles using __in
    data = list(
        CurrentTable.objects.filter(vehicleno__in=user_vehicles)
        .values('vehicleno', 'lat', 'lon', 'speed', 'tracktime') # add unit number also
    )

    return JsonResponse({'vehicles': data})



@never_cache
def user_logout(request):
    """
    Logs out the user by destroying the session
    and redirects to the home/login page.
    """
    django_logout(request)  # This clears the session and logs out the user
    messages.success(request, "You have been successfully logged out.")
    return redirect("user_login")  # Replace "home" with your login page if needed