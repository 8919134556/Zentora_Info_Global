from django.db import models
from datetime import datetime

from matplotlib.pyplot import title




class Vechile_Register(models.Model):
    id = models.AutoField(primary_key=True)

    gender = models.CharField(verbose_name='Gender', db_column="gender", max_length=50, blank=False,
                                  null=False)
    user_name = models.CharField(verbose_name='User_Name', db_column="user_name", max_length=50, blank=False,
                                  null=False)
    user_lastname = models.CharField(verbose_name='User_Lastname', db_column="user_lastname", max_length=50, blank=False,
                                  null=False)
    user_email = models.EmailField(db_column='user_email', verbose_name='User_Email', max_length=100, null=True, blank=True)
    
    user_phone = models.BigIntegerField(verbose_name='User_Phone', db_column="user_phone", blank=False,
                                  null=False)
    vechile_year = models.CharField(verbose_name='Vechile_Year', db_column="vechile_year", max_length=50, blank=False,
                                  null=False)
    vechile_make = models.CharField(verbose_name='Vechile_Make', db_column="vechile_make", max_length=50, blank=False,
                                  null=False)
    vechile_model = models.CharField(verbose_name='vechile_model', db_column="vechile_model", max_length=50, blank=False,
                                  null=False)
    vechile_color = models.CharField(verbose_name='Vechile_Color', db_column="vechile_color", max_length=50, blank=False,
                                  null=False)
    
    vechile_mileage = models.CharField(verbose_name='Vechile_Mileage', db_column="vechile_mileage", max_length=50, blank=False,
                                  null=False)
    vechile_number = models.CharField(verbose_name='vechile_number', db_column="vechile_number", max_length=50, blank=False,
                                  null=False)
    vechile_type= models.CharField(verbose_name='vechile_type', db_column="vechile_type", max_length=50, blank=False,
                                  null=True)

    country= models.CharField(verbose_name='Country', db_column="country", max_length=50, blank=False,
                                  null=True)
    state= models.CharField(verbose_name='State', db_column="state", max_length=50, blank=False,
                                  null=True)
    city= models.CharField(verbose_name='City', db_column="city", max_length=50, blank=False,
                                  null=True)
    
    street_name= models.CharField(verbose_name='Street_Name', db_column="street_name", max_length=50, blank=False,
                                  null=False)
    house_number= models.CharField(verbose_name='House_Number', db_column="house_number", max_length=50, blank=False,
                                  null=False)
        
 
    user_image = models.FileField(verbose_name='User_Image', db_column="user_image", upload_to='User/Profile-image/', blank=True,)

    vechile_image = models.FileField(verbose_name='Vechile_image', db_column="Vechile_image", upload_to='User/Vechile-image/', blank=True,)

   
    datetime_created = models.DateTimeField(default=datetime.now)
    
    class Meta:
        db_table='Vechile_Register'
    



# class Login(models.Model):
#     username = models.CharField(max_length=100)
#     lastname = models.CharField(max_length=100, blank=True, null=True)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     gender = models.CharField(
#         max_length=10,
#         choices=[('Male', 'Male'), ('Female', 'Female')],
#         blank=True,
#         null=True
#     )
#     password = models.CharField(max_length=128)
#     account_status = models.CharField(
#         max_length=20,
#         default="Pending"  # default status when account is created
#     )
#     country = models.CharField(max_length=100, blank=True, null=True)
#     state = models.CharField(max_length=100, blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     street_name = models.CharField(max_length=200, blank=True, null=True)
#     user_image = models.ImageField(upload_to='user_images/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.username} {self.lastname or ''}".strip()


class Login(models.Model):
    username = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')],
        blank=True,
        null=True
    )
    password = models.CharField(max_length=128)
    account_status = models.CharField(
        max_length=20,
        default="Pending"  # default status when account is created
    )
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    street_name = models.CharField(max_length=200, blank=True, null=True)
    house_number = models.CharField(
        verbose_name='House_Number',
        db_column="house_number",
        max_length=50,
        blank=True,
        null=True
    )
    user_image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} {self.lastname or ''}".strip()
