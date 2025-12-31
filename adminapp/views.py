from django.contrib.auth import authenticate, login
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




def admin_home(request):
    v_regi = Vechile_Register.objects.all().count()
    # fines = Fines.objects.all().count()
    # money = Payments.objects.filter(status ="Success").aggregate(price_sum=Sum('amount'))
    # v_fines = V_Fines.objects.all().count()
    # context = {
    #     'data1' : v_regi,
    #     'data2' : fines,
    #     'data3' : money['price_sum'],
    #     'data4' : v_fines
    # }
    context = {
        'data1' : v_regi,
    }
    return render (request, './admin/dashboard.html', context = context)


def upload_vechile(request):
    login_users = Login.objects.all().order_by('username')

    if request.method == "POST":
        user_type = request.POST.get('user_type')  # "new" or "existing"

        gender = request.POST.get('gender')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        v_type = request.POST.get('v-type')
        v_year = request.POST.get('v-year')
        v_make = request.POST.get('v-make')
        v_model = request.POST.get('v-model')
        v_color = request.POST.get('v-color')
        v_mileage = request.POST.get('v-mileage')
        v_number = request.POST.get('v-number')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        s_name = request.POST.get('s-name')
        h_number = request.POST.get('h-number')

        u_image = request.FILES.get('user-image')
        v_image = request.FILES.get('myFile')

        if not v_image:
            return render(request, './admin/upload-vechile.html', {
                'msg': "⚠️ Vehicle image is required.",
                'login_users': login_users
            })

        login_user = None

        # 🧩 Case 1: New user
        if user_type == "new":
            if Login.objects.filter(email=email).exists():
                return render(request, './admin/upload-vechile.html', {
                    'msg': f'User with email {email} already exists! Please select "Existing User".',
                    'login_users': login_users
                })

            raw_password = get_random_string(length=8)
            print(raw_password)
            login_user = Login.objects.create(
                username=fname,
                lastname=lname,
                email=email,
                phone=phone,
                gender=gender,
                country=country,
                state=state,
                city=city,
                street_name=s_name,
                house_number=h_number,
                user_image=u_image,
                password=make_password(raw_password),
                account_status="Pending"
            )

            # send email (optional)
             # ✉️ Send password email
            try:
                subject = "Your Fleet Management Account Credentials"
                message = (
                    f"Hello {fname},\n\n"
                    f"Your account has been created successfully.\n"
                    f"Please use the following credentials to log in:\n\n"
                    f"Username: {email}\n"
                    f"Password: {raw_password}\n\n"
                    f"Please change your password after logging in.\n\n"
                    f"Regards,\nFleet Management Team"
                )
                EmailMessage(subject, message, to=[email])
                print(f"✅ Password email sent to {email}")
            except Exception as e:
                print(f"⚠️ Error sending email: {e}")

        # 🧩 Case 2: Existing user
        elif user_type == "existing":
            try:
                existing_email = request.POST.get('existing_user')
                login_user = Login.objects.get(email=existing_email)
            except Login.DoesNotExist:
                return render(request, './admin/upload-vechile.html', {
                    'msg': f'No existing user found. Please select a valid user.',
                    'login_users': login_users
                })

            fname = login_user.username
            lname = login_user.lastname
            email = login_user.email
            phone = login_user.phone
            gender = login_user.gender
            country = login_user.country
            state = login_user.state
            city = login_user.city
            s_name = login_user.street_name
            h_number = login_user.house_number
            u_image = login_user.user_image

        # 🚗 Save Vehicle
        Vechile_Register.objects.create(
            gender=gender,
            user_name=fname,
            user_lastname=lname,
            user_phone=phone,
            country=country,
            state=state,
            city=city,
            vechile_year=v_year,
            vechile_make=v_make,
            vechile_model=v_model,
            vechile_color=v_color,
            vechile_mileage=v_mileage,
            vechile_number=v_number,
            vechile_type=v_type,
            street_name=s_name,
            house_number=h_number,
            vechile_image=v_image,
            user_email=email,
            user_image=u_image,
        )

        msg = (
            "✅ Vehicle registered & Login created (Pending Approval)"
            if user_type == "new" else
            "✅ Vehicle registered for existing user"
        )
        return render(request, './admin/upload-vechile.html', {'msg': msg, 'login_users': login_users})

    return render(request, './admin/upload-vechile.html', {'login_users': login_users})




def v_deatils(request):
    data = Vechile_Register.objects.all()
    return render (request, './admin/view-details.html', {'view': data})

def popup(request, id):
    data = Vechile_Register.objects.get(id=id)
    return render (request, './admin/popup-form.html', {'view': data})

def fine(request):
    
    return render (request, './admin/fine.html')

def fine_details(request):
   
    return render (request, './admin/upload-fine-details.html')

def fine_edit(request, id):
    
    return render (request, './admin/fine-edit.html')



def logout(request):
    return redirect("home")