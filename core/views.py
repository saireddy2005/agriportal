from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Count
from django.db.models.functions import TruncWeek, TruncDay
from .models import Notification
from .models import FarmerEntry, CropData, BusinessRecord, Notification, Activity, Report,MillEntry


# Home / Landing Page
def index(request):
    return render(request, 'core/index.html')


# Signup
def signup(request):

    if request.method == "POST":

        fullname = request.POST.get("fullname")
        email = request.POST.get("email")

        # Gmail validation
        if not email.endswith("@gmail.com"):
            messages.error(request,"Email must end with @gmail.com")
            return redirect("/signup/")

        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password match check
        if password != confirm_password:
            messages.error(request,"Passwords do not match")
            return redirect("/signup/")

        # Check if account exists
        if User.objects.filter(username=email).exists():
            messages.error(request,"Account already exists")
            return redirect("/signup/")

        # Create user
        User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        messages.success(request,"Account created successfully")

    return render(request,"core/signup.html")

    
# Login

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("/login/")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/home/")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "core/login.html")
# Logout
def user_logout(request):
    logout(request)
    return redirect('login')


# Home page activity feed
def home(request):

    activities = Activity.objects.all().order_by('-created_at')

    return render(request, 'core/home.html', {'activities': activities})


# Add activity
def add_activity(request):

    if request.method == "POST":

        entry_type = request.POST['entry_type']
        crop = request.POST['crop']
        bags = request.POST['bags']
        amount = request.POST['amount']
        lorry = request.POST['lorry']
        image = request.FILES['image']

        Activity.objects.create(
            entry_type=entry_type,
            crop=crop,
            bags=bags,
            amount=amount,
            lorry=lorry,
            image=image,
            user=request.user
        )

        return redirect('/home/')

    return render(request, 'core/add.html')


# Farmer entry
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import FarmerEntry, Notification


@login_required
def farmer_entry(request):

    if request.method == "POST":

        try:
            farmer_name = request.POST.get("farmer_name")
            village = request.POST.get("village")
            district = request.POST.get("district")
            mobile = request.POST.get("mobile")

            acres = request.POST.get("acres")
            crop_type = request.POST.get("crop_type")
            bags = request.POST.get("bags")
            amount = request.POST.get("amount")

            lorry_number = request.POST.get("lorry")
            image = request.FILES.get("image")

            # Save farmer entry
            FarmerEntry.objects.create(
                farmer_name=farmer_name,
                village=village,
                district=district,
                mobile=mobile,
                acres=acres,
                crop_type=crop_type,
                total_bags=bags,
                total_amount=amount,
                lorry_number=lorry_number,
                image=image
            )

            # 🔔 Send notification to all users
            users = User.objects.all()

            for u in users:
                Notification.objects.create(
                    user=u,
                    message=f"{request.user.username} submitted a new farmer entry"
                )

            messages.success(request, "Farmer data submitted successfully")

        except Exception as e:
            print(e)
            messages.error(request, str(e))

    return render(request, "core/farmer.html")
from django.contrib.auth.models import User
from .models import MillEntry, Notification
from django.contrib import messages


def mill_entry(request):

    if request.method == "POST":

        try:
            owner_name = request.POST.get("owner_name")
            mill_name = request.POST.get("mill_name")
            mill_address = request.POST.get("mill_address")
            district = request.POST.get("district")
            mobile = request.POST.get("mobile")
            paddy_type = request.POST.get("paddy_type")
            bags = request.POST.get("bags")
            lorry = request.POST.get("lorry")
            amount = request.POST.get("amount")
            image = request.FILES.get("image")

            MillEntry.objects.create(
                owner_name=owner_name,
                mill_name=mill_name,
                mill_address=mill_address,
                district=district,
                mobile=mobile,
                paddy_type=paddy_type,
                bags=bags,
                lorry=lorry,
                amount=amount,
                image=image
            )

            # Send notification to all users
            users = User.objects.all()

            for u in users:
                Notification.objects.create(
                    user=u,
                    message=f"{request.user.username} submitted a new mill entry"
                )

            messages.success(request, "Mill data submitted successfully")

        except Exception as e:
            print(e)
            messages.error(request, str(e))

    return render(request, "core/mill.html")

# Statistics page
from django.db.models.functions import  TruncDay
from django.db.models import Sum, Count
from django.utils import timezone

from .models import FarmerEntry, MillEntry   # ✅ added MillEntry
import json

def stats(request):


    print("TOTAL MILL RECORDS:", MillEntry.objects.count())   # ✅ ADD HERE
    # 🔹 CROP DATA (NO CHANGE)
    crop_data = FarmerEntry.objects.values('crop_type').annotate(total=Count('id'))
    print("CROP DATA:", list(crop_data))

    crop_labels = [x.get('crop_type') for x in crop_data]
    crop_values = [x.get('total') for x in crop_data]

    # 🔹 ❌ REMOVE WEEKLY DATA (replaced with mill data)

    # 🔹 ✅ MILL DATA (NEW)

    weekly_data = Activity.objects.annotate(
        week=TruncWeek('created_at', tzinfo=timezone.get_current_timezone())
    ).values('week').annotate(total=Count('id')).order_by('week')

    week_labels = [str(x['week']) for x in weekly_data]
    week_values = [x['total'] for x in weekly_data]

    # 🔹 DAILY DATA (NO CHANGE)
    daily_data = Activity.objects.annotate(
        day=TruncDay('created_at', tzinfo=timezone.get_current_timezone())
    ).values('day').annotate(total=Sum('amount')).order_by('day')

    day_labels = [str(x['day']) for x in daily_data]
    day_values = [x['total'] for x in daily_data]

    print("DAILY:", list(daily_data))

    # 🔹 CONTEXT (UPDATED)
    context = {
        'crop_labels': json.dumps(crop_labels),
        'crop_values': json.dumps(crop_values),

        # ✅ NEW MILL DATA (replace week)
       'week_labels': json.dumps(week_labels),
        'week_values': json.dumps(week_values),
        'day_labels': json.dumps(day_labels),
        'day_values': json.dumps(day_values)
    }

    return render(request, 'core/stats.html', context)
# Notifications
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def notifications(request):

    notes = Notification.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "core/notifications.html", {"notes": notes})


# Profile
def profile(request):

    reports = Report.objects.all()

    return render(request, 'profile.html', {'reports': reports})


# Report user
def report_user(request, user_id):

    if request.method == "POST":

        reason = request.POST.get('reason')

        Report.objects.create(
            reported_user_id=user_id,
            reported_by=request.user,
            reason=reason
        )

    return redirect('profile')


# Reported users (admin only)
def reported_users(request):

    if not request.user.is_superuser:
        return render(request, 'core/no_access.html')

    reports = Report.objects.all().order_by('-created_at')

    return render(request, 'core/reported_users.html', {'reports': reports})


# Aggregator page
def aggregator(request):
    return render(request, 'core/aggregator.html')


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        # convert email to lowercase
        email = email.lower()

        # check if email exists
        user = User.objects.filter(email=email).first()

        if user:
            # store email in session
            request.session['reset_email'] = email

            # move to reset password page
            return redirect('/reset-password/')

        else:
            messages.error(request,"Email ID is invalid")

    return render(request,"core/forgot_password.html")

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def reset_password(request):
    email=request.session.get('reset_email')
    print(email)
    email = request.session.get('reset_email')

    if not email:
        return redirect('/forgot-password/')

    redirect_flag = False

    if request.method == "POST":

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Password do not match")

        else:

            user = User.objects.filter(email=email).first()

            if user:

                user.set_password(new_password)
                user.save()

                if 'reset_email' in request.session:
                    del request.session['reset_email']

                messages.success(request, "Password updated successfully")

                redirect_flag = True

            else:
                messages.error(request, "User not found")

    return render(request, "core/reset_password.html", {"redirect": redirect_flag})


import json
from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.models import User
from .models import FarmerEntry, MillEntry, Notification

def stats(request):

    # Dashboard cards
    total_farmers = FarmerEntry.objects.count()
    total_mills = MillEntry.objects.count()
    total_users = User.objects.count()
    total_notifications = Notification.objects.count()

    # Crop Pie Chart
    crop_data = FarmerEntry.objects.values('crop_type').annotate(count=Count('id'))
    crop_labels = [i.get('crop_type') for i in crop_data]
    crop_values = [i.get('count')for i in crop_data]

    context = {
        "total_farmers": total_farmers,
        "total_mills": total_mills,
        "total_users": total_users,
        "total_notifications": total_notifications,
        "crop_labels": json.dumps(crop_labels),
        "crop_values": json.dumps(crop_values),
    }

    return render(request, "core/stats.html", context)

def harvesting_page(request):
    return render(request, "core/harvesting.html")

def harvest_farmer(request):
    return render(request, "core/harvest_farmer.html")

def harvester(request):
    return render(request, "core/harvester.html")

def harvest_farmer(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)

    return render(request, "core/harvest_farmer.html")



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HarvestFarmer


def harvest_farmer(request):
    if request.method == "POST":
        try:
            # ---------------------------
            # GET DATA FROM FORM
            # ---------------------------
            farmer_name = request.POST.get("farmer_name")
            village = request.POST.get("village")
            state = request.POST.get("state")
            phone = request.POST.get("phone")
            date = request.POST.get("date")
            operator_name = request.POST.get("operator_name")
            machine_number = request.POST.get("machine_number")

            # ---------------------------
            # TYPE CONVERSION (IMPORTANT)
            # ---------------------------
            acres = float(request.POST.get("acres", 0))
            time = request.POST.get("time")
            amount = int(request.POST.get("amount", 0))

            # ---------------------------
            # FILE UPLOAD
            # ---------------------------
            bill = request.FILES.get("bill")

            if not bill:
                raise Exception("Bill image is required")

            # ---------------------------
            # OPTIONAL VALIDATIONS
            # ---------------------------
            if not farmer_name.isalpha():
                raise Exception("Farmer name must be letters only")

            if not operator_name.isalpha():
                raise Exception("Operator name must be letters only")

            if len(phone) != 10 or not phone.isdigit():
                raise Exception("Phone number must be 10 digits")

            # Machine format check (AP34CJ6778)
            import re
            if not re.match(r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$', machine_number):
                raise Exception("Invalid machine number format")

            # ---------------------------
            # SAVE TO DATABASE
            # ---------------------------
            HarvestFarmer.objects.create(
                farmer_name=farmer_name,
                village=village,
                state=state,
                phone=phone,
                date=date,
                operator_name=operator_name,
                machine_number=machine_number.upper(),
                acres=acres,
                time=time,
                amount=amount,
                bill=bill
            )
            
            Notification.objects.create(
          
            message=f"{farmer_name} data added with operator {operator_name}"
        )

       
            messages.success(request, "Submitted Successfully")

            return redirect('harvest_farmer')   # reload same page

        except Exception as e:
            print("ERROR:", e)   # check terminal
            messages.error(request, f"FAILED: {e}")

            return redirect('harvest_farmer')

    # ---------------------------
    # GET REQUEST (PAGE LOAD)
    # ---------------------------
    return render(request, "core/harvest_farmer.html")

import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HarvesterOperator

def harvester_entry(request):
    if request.method == 'POST':

        operator_name = request.POST.get('operator_name')
        machine_number = request.POST.get('machine_number')
        date = request.POST.get('date')
        bill = request.FILES.get('file_upload')

        farmer_names = request.POST.getlist('farmer_name[]')
        villages = request.POST.getlist('village[]')
        acres = request.POST.getlist('acres[]')
        times = request.POST.getlist('time[]')
        amounts = request.POST.getlist('amount[]')

        # ✅ LOOP THROUGH EACH ROW
        for i in range(len(farmer_names)):

            # 🔴 VALIDATIONS

            if not farmer_names[i].replace(" ", "").isalpha():
                messages.error(request, "Farmer name should contain only letters")
                return redirect('harvester_entry')

            if not villages[i].replace(" ", "").isalpha():
                messages.error(request, "Village should contain only letters")
                return redirect('harvester_entry')

            try:
                acres_val = float(acres[i])
            except:
                messages.error(request, "Acres must be a number")
                return redirect('harvester_entry')

            if not re.match(r'^[A-Za-z0-9 ]+$', times[i]):
                messages.error(request, "Time must contain letters and numbers only")
                return redirect('harvester_entry')

            if not amounts[i].isdigit():
                messages.error(request, "Amount must be integer")
                return redirect('harvester_entry')

            # ✅ SAVE DATA (ONE ROW PER FARMER)
            HarvesterOperator.objects.create(
                operator_name=operator_name,
                machine_number=machine_number,
                date=date,
                farmer_name=farmer_names[i],
                village=villages[i],
                acres=acres_val,
                total_time=times[i],
                total_amount=float(amounts[i]),
                bill=bill
            )
         # 🔔 NOTIFICATION (ONLY ONCE)
        Notification.objects.create(
           
            message=f"{operator_name} submitted {len(farmer_names)} farmer records"
        )

        messages.success(request, "All data submitted successfully!")
        return redirect('harvester_entry')

    return render(request, 'core/harvester_entry.html')











from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import MillTransaction, FarmerTransaction

# ✅ Admin check
def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def account_management(request):

    # ADD DATA
    if request.method == 'POST':

        # Mill Entry
        if 'mill_submit' in request.POST:
            MillTransaction.objects.create(
                date=request.POST.get('mill_date'),
                mill_name=request.POST.get('mill_name'),
                amount=request.POST.get('mill_amount')
            )

        # Farmer Entry
        if 'farmer_submit' in request.POST:
            FarmerTransaction.objects.create(
                date=request.POST.get('farmer_date'),
                farmer_name=request.POST.get('farmer_name'),
                village=request.POST.get('village'),
                amount=request.POST.get('farmer_amount')
            )

        return redirect('account_management')


# SEARCH
mill_query = request.GET.get('mill_search', '')
farmer_query = request.GET.get('farmer_search', '')

# NEW filters
mill_date = request.GET.get('mill_date', '')
farmer_date = request.GET.get('farmer_date', '')
farmer_village = request.GET.get('farmer_village', '')

mill_data = MillTransaction.objects.all()
farmer_data = FarmerTransaction.objects.all()

# 🔹 MILL FILTER
if mill_query:
    mill_data = mill_data.filter(mill_name__icontains=mill_query)

if mill_date:
    mill_data = mill_data.filter(date=mill_date)


# 🔹 FARMER FILTER
if farmer_query:
    farmer_data = farmer_data.filter(farmer_name__icontains=farmer_query)

if farmer_date:
    farmer_data = farmer_data.filter(date=farmer_date)

if farmer_village:
    farmer_data = farmer_data.filter(village__icontains=farmer_village)


return render(request, 'core/account_management.html', {
    'mill_data': mill_data,
    'farmer_data': farmer_data
})

# DELETE MILL
def delete_mill(request, id):
    MillTransaction.objects.get(id=id).delete()
    return redirect('account_management')


# DELETE FARMER
def delete_farmer(request, id):
    FarmerTransaction.objects.get(id=id).delete()
    return redirect('account_management')



from django.shortcuts import redirect
from .models import Notification

def delete_notification(request, id):
    Notification.objects.filter(id=id).delete()
    return redirect('notifications')