from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.template import loader
from django.shortcuts import render
from django.core.mail import EmailMessage
from .models import *
from django.utils.crypto import get_random_string
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.db import transaction



def admin_login_page(request):
    """
    Handles admin login.
    GET: Show login page
    POST: Authenticate and login admin
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # Only allow staff/admin users
                login(request, user)  # Start session
                return redirect("admin_home")  # Replace with your dashboard URL name
            else:
                messages.error(request, "You do not have admin privileges.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "admin/admin-login-page.html")



@never_cache
@login_required(login_url='admin_login')
def admin_home(request):
    v_regi = Vechile_Register.objects.all().count()
    context = {
        'data1' : v_regi,
    }
    return render (request, './admin/dashboard.html', context = context)

@never_cache
@login_required(login_url="admin_login")
@transaction.atomic
def upload_vechile(request):
    # ONLY NORMAL USERS (NO SUPERUSER)
    user_login_url = request.build_absolute_uri(reverse("user_login"))
    login_users = User.objects.filter(
        is_superuser=False,
        is_staff=False
    ).order_by("username")
    if request.method == "POST":

        user_type = request.POST.get("user_type")  # new / existing
        # -------------------------
        # USER INPUT
        # -------------------------
        gender = request.POST.get("gender")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        phone = int(request.POST.get("phone"))
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        street_name = request.POST.get("street_name")
        house_number = request.POST.get("house_number")
        user_image = request.FILES.get("user_image")
        # -------------------------
        # VEHICLE INPUT
        # -------------------------
        vechile_year = request.POST.get("vechile_year")
        vechile_make = request.POST.get("vechile_make")
        vechile_model = request.POST.get("vechile_model")
        vechile_color = request.POST.get("vechile_color")
        vechile_mileage = request.POST.get("vechile_mileage")
        vechile_number = request.POST.get("vechile_number")
        vechile_type = request.POST.get("vechile_type")
        vechile_image = request.FILES.get("vechile_image")
        if not vechile_image:
            return render(request, "./admin/upload-vechile.html", {
                "msg": "⚠️ Vehicle image is required",
                "login_users": login_users
            })
        # =====================================================
        # 🧩 CASE 1: NEW USER
        # =====================================================
        if user_type == "new":
            if User.objects.filter(username=email).exists():
                return render(request, "./admin/upload-vechile.html", {
                    "msg": "⚠️ User already exists. Choose existing user.",
                    "login_users": login_users
                })

            raw_password = get_random_string(8)
            user = User.objects.create(
                username=email,
                email=email,
                first_name=fname,
                last_name=lname,
                password=make_password(raw_password),
                is_staff=False,
                is_superuser=False
            )
            profile = UserProfile.objects.create(
                user=user,
                phone=phone,
                gender=gender,
                country=country,
                state=state,
                city=city,
                street_name=street_name,
                house_number=house_number,
                user_image=user_image,
                account_status="Pending"
            )
            message = (
                    f"Hello {fname},\n\n"
                    f"Your account has been created successfully.\n"
                    f"Please use the following credentials to log in:\n\n"
                    f"Click here to login: {user_login_url}\n\n"
                    f"Username: {email}\n"
                    f"Password: {raw_password}\n\n"
                    f"Please change your password after logging in.\n\n"
                    f"Regards,\nFleet Management Team"
                )

            # 📧 SEND EMAIL
            EmailMessage(
                subject="Your Login Credentials",
                body = message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            ).send(fail_silently=False)

        # =====================================================
        # 🧩 CASE 2: EXISTING USER
        # =====================================================
        else:
            user_id = request.POST.get("existing_user")
            user = User.objects.get(id=user_id)
            profile = user.profile
            fname = user.first_name
            lname = user.last_name
            email = user.email
            phone = profile.phone
            gender = profile.gender
            country = profile.country
            state = profile.state
            city = profile.city
            street_name = profile.street_name
            house_number = profile.house_number
            user_image = profile.user_image

        # =====================================================
        # 🚗 SAVE VEHICLE (ALL FIELDS MAPPED)
        # =====================================================
        Vechile_Register.objects.create(
            user=user,
            gender=gender,
            user_name=fname,
            user_lastname=lname,
            user_email=email,
            user_phone=phone,
            vechile_year=vechile_year,
            vechile_make=vechile_make,
            vechile_model=vechile_model,
            vechile_color=vechile_color,
            vechile_mileage=vechile_mileage,
            vechile_number=vechile_number,
            vechile_type=vechile_type,
            country=country,
            state=state,
            city=city,
            street_name=street_name,
            house_number=house_number,
            user_image=user_image,
            vechile_image=vechile_image
        )

        return render(request, "./admin/upload-vechile.html", {
            "msg": "✅ Vehicle registered successfully",
            "login_users": login_users
        })

    return render(request, "./admin/upload-vechile.html", {
        "login_users": login_users
    })


@never_cache
@login_required(login_url="admin_login")
def v_details(request):
    data = (
        Vechile_Register.objects
        .select_related("user", "user__profile")
        .all()
    )
    return render(
        request,
        "./admin/view-details.html",
        {"view": data}
    )



@login_required(login_url="admin_login")
def approve_user(request, user_id):
    profile = UserProfile.objects.get(user_id=user_id)
    profile.account_status = "Approved"
    profile.save()
    return redirect("v_details")


@login_required(login_url="admin_login")
def reject_user(request, user_id):
    profile = UserProfile.objects.get(user_id=user_id)
    profile.account_status = "Rejected"
    profile.save()
    return redirect("v_details")


@never_cache
@login_required(login_url='admin_login')
def popup(request, id):
    data = Vechile_Register.objects.get(id=id)
    return render (request, './admin/popup-form.html', {'view': data})



@never_cache
@login_required(login_url='admin_login')
def add_emp(request):
   
    return render (request, './admin/add-emp.html')






@never_cache
@login_required(login_url='admin_login')
def fine(request):
    return render (request, './admin/fine.html')




@never_cache
@login_required(login_url='admin_login')
def fine_edit(request, id):
    
    return render (request, './admin/fine-edit.html')

@never_cache
def logout(request):
    """
    Logs out the user by destroying the session
    and redirects to the home/login page.
    """
    django_logout(request)  # This clears the session and logs out the user
    messages.success(request, "You have been successfully logged out.")
    return redirect("admin_login")  # Replace "home" with your login page if needed
