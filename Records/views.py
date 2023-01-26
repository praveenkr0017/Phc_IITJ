from django.shortcuts import render,redirect
from .models import User,Prescriptions
from django.contrib.auth.models import auth
from django.contrib import messages
from random import randint
import datetime as dt
import pytz
utc = pytz.UTC 

# Create your views here.

#_________________ PHC_Homepage __________________

def home(request):
    return render(request,"Home_page.html")




#_________________ Registration of Student __________________

def register_student(request):
    if request.method == 'POST':
        Student = User()
        Student.name = request.POST['Name']
        id = (request.POST['RollNo']).upper()
        Student.ID = id
        Student.gender = request.POST['Gender']
        Student.blood_Group = request.POST['BloodGroup']
        
        Mobile = request.POST['Mobile']
        if Mobile.isdigit() and len(Mobile)==10:  #Check for valid mobile number
            Student.mobile = Mobile
        else:
            messages.info(request,'!!! Invalid mobile number !!!')
            return redirect('register_student')
        
        Email = request.POST['email']
        Student.email = Email
        
        if request.POST['Password']==request.POST['ConfPassword']:
            Student.password = request.POST['Password']
        else:
            messages.info(request,'!!! Passwords do not match !!!')
            return redirect('register_student')
        
        Student.profile_img = request.FILES['ProfileImage']
        
        if User.objects.filter(ID=id).exists():   #To check if user id entered by enduser , already exists in the database because user id is unique
            messages.info(request,'!!! User ID already exists !!!')
            return redirect('register_student')
        if User.objects.filter(email=Email).exists():  #To check if email entered by enduser , already exists in the database because email is unique
            messages.info(request,'!!! Email id already exists !!!')
            return redirect('register_student')
        
        Student.save();
            
        return redirect('/')
    return render(request, "student_registration.html")



#_________________ Registration of Employee __________________

def register_employee(request):
    if request.method == 'POST':
        Employee = User()
        Employee.name = request.POST['Name']
        id = (request.POST['EmployeeID']).upper()
        Employee.ID = id
        Employee.gender = request.POST['Gender']
        Employee.blood_Group = request.POST['BloodGroup']
        
        Mobile = request.POST['Mobile']
        if Mobile.isdigit() and len(Mobile)==10:
            Employee.mobile = Mobile
        else:
            messages.info(request,'!!! Invalid mobile number !!!')
            return redirect('register_employee')
        
        Email = request.POST['email']
        Employee.email = Email
        
        if request.POST['Password']==request.POST['ConfPassword']:
            Employee.password = request.POST['Password']
        else:
            messages.info(request,'!!! Passwords do not match !!!')
            return redirect('register_employee')
        
        Employee.profile_img = request.FILES['ProfileImage']

        if User.objects.filter(ID=id).exists():   #To check if user id entered by enduser , already exists in the database because user id is unique
            messages.info(request,'!!! User ID already exists !!!')
            return redirect('register_employee')
        if User.objects.filter(email=Email).exists():  #To check if email entered by enduser , already exists in the database because email is unique
            messages.info(request,'!!! Email id already exists !!!')
            return redirect('register_employee')

        Employee.save();
            
        return redirect('/')    
    return render(request, "Emp_registration.html")



#_________________ Login __________________

def login(request):

    if request.method== 'POST':
        global id,PASSCODE,PASSWORD
        PASSCODE = request.POST.get('Passcode')
        if bool(PASSCODE):
            id = request.POST.get('ID') 
        else:
            id = (request.POST.get('ID')).upper()  #To avoid the case sensitive case
        PASSWORD = request.POST.get('Password')
        users = User.objects.all()
        if bool(id)==True and bool(PASSWORD)==True:     #To check if the login is done using userId-password or passcode 
            user = [j for j in users if j.ID==id and j.password==PASSWORD]
            if bool(user)==False:
                messages.info(request,'!!! Invalid credentials !!!')
                return redirect('login')
            else:
                #user = user[0]
                #user = auth.authenticate(email=user.email,password=user.password)
                #auth.login(request, user)
                
                #Generation of Passcode
                while True:
                    PASSCODE = randint(1000,9999)
                    user_temp = [x for x in users if x.passcode==PASSCODE]
                    if bool(user_temp)!=False:
                        pass
                    else:
                        break
                user[0].passcode = PASSCODE
                #Addition of expiry time during login using user id and password
                expiry_time_duration = dt.timedelta(minutes=1)     #Here we are getting the expiry time duration time gap basically.
                expiry_time_stamp = dt.datetime.now() + expiry_time_duration     #New expiry time stamp is obtained
                expiry_time_stamp = utc.localize(expiry_time_stamp)
                user[0].expiry = expiry_time_stamp  
                #End - Addition of expiry time during login using user id and password

                user[0].save()   #Saving of the passcode and the expiry time stamp
                #End-Gen of Passcode
                
                #messages.success(request,'Login succesful')
                return redirect('student')
        
        elif bool(PASSCODE)==True:
            user = [j for j in users if j.passcode==PASSCODE]
            time = utc.localize(dt.datetime.now())
            if bool(user)==False:
                messages.info(request,'!!! Invalid passcode !!!')
                return redirect('login')
            else:
                if time>user[0].expiry:
                    messages.info(request,'!!! Passcode Expired !!!')
                    return redirect('login')
                return redirect('student')

        messages.info(request,'!!! Please enter all valid credentials correctly !!!')
    return render(request, "login.html")




#_________________ Display of account i.e. prescription __________________

def student(request):

    #Diplay of Patient's record from User table
    users = User.objects.all()
    if bool(id)==True and bool(PASSWORD)==True:
        user = [j for j in users if j.ID==id][0]
        #Display of Prescriptions data from Prescriptions table
        prescriptions = Prescriptions.objects.all()
        prescriptions = [i for i in prescriptions[::-1] if i.ID==id]
    
    elif bool(PASSCODE)==True:
        user = [j for j in users if j.passcode==PASSCODE][0]

        #Display of Prescriptions data from Prescriptions table
        prescriptions = Prescriptions.objects.all()
        prescriptions = [i for i in prescriptions[::-1] if i.ID==user.ID]
    
    return render(request, "student.html",{'user':user,'presciptions':prescriptions})



#_________________ Updation of details __________________

def update(request):

    if request.method == 'POST':
        PrescriptionUpload = Prescriptions()
        PrescriptionUpload.ID = id
        PrescriptionUpload.date = (request.POST['date']).split('-')
        PrescriptionUpload.date = '-'.join(PrescriptionUpload.date[::-1])
        PrescriptionUpload.prescription_img = request.FILES['fileToUpload']
        PrescriptionUpload.save();
        
        #messages.success(request, "Prescription added successfully.")
        return redirect('student')

    return render(request, "update.html")



#_________________ Contact __________________

def contact(request):
    return render(request, "contact.html")


#________________ Logout ____________________

def logout(request):
    id = None
    return redirect('/')

