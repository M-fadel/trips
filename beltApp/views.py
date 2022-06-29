from multiprocessing import context
from re import S, T, U
from tkinter import E
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
        # redirect the user back to the form to fix the errors
            return redirect('/')
        else:
            users = User.objects.filter(Email=request.POST['Email'])
            if len(users) == 0:
                password = request.POST.get('password')
                a=User.objects.create(
                    fName= request.POST.get('fName'),
                    lName = request.POST.get('lName'),
                    Email = request.POST.get('Email'),
                    # encrypting password
                    password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode()
                )
                a.save()
                context={
                    "user": a
                }
                request.session['users'] = a.id
                return redirect('/trips')
            else:
                messages.error(request, "User already exist!")
                return redirect('/')

def login(request):
    if request.method == 'POST':
        a = User.objects.filter(Email = request.POST['Email'])
        if len(a)==1:
            if not bcrypt.checkpw(request.POST['Password'].encode('utf8'),a[0].password.encode('utf8')):
                messages.error(request, "Email or Password is incorrect!")
                return redirect('/')
            else:
                context = {
                    "user": a[0]
                }
                request.session['users'] = a[0].id
                return redirect('/trips')
        else:
            messages.error(request, "User dose not exist!")
            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if not 'users' in request.session:
        return redirect('/')
    else:
        u =User.objects.get(id = request.session['users'])
        a = User.objects.all()
        t = trips.objects.all()
        context = {
            "user": u ,
            "users": a ,
            "trips": t ,
        }
        return render(request, 'board.html', context)

def trip(request):
    u =User.objects.get(id = request.session['users'])
    context = { 'user':u}
    return render(request, 'trip.html',context)

def create(request):
    if request.method == 'POST':
        errors = trips.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/trip')
        else:
            dest = request.POST['dest']
            SDate = request.POST['SDate']
            EDate = request.POST['EDate']
            plan = request.POST['plan']
            u =User.objects.get(id = request.session['users'])  
            trip = trips.objects.create(
                dest = dest ,
                SDate = SDate ,
                EDate = EDate ,
                plan = plan ,
                user = u
            )
            
            return redirect('/trips')

def delete(request ,number):
    t = trips.objects.get(id = number)
    t.delete()
    return redirect("/trips")

def edit(request ,number):
            t = trips.objects.get(id = number)
            u = User.objects.get(id = request.session['users'])
            SDate =  t.SDate.strftime("%Y-%m-%d")
            EDate =  t.EDate.strftime("%Y-%m-%d")
            context = {
                "trip": t ,
                "user": u,
                "start":SDate,
                "end": EDate
            }
            return render(request,"Edit.html",context)

def update(request ,number):
    if request.method == 'POST':
        errors = trips.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{number}')
        else:
            t = trips.objects.get(id = number)
            t.dest = request.POST['dest']
            t.SDate = request.POST['SDate']
            t.EDate = request.POST['EDate']
            t.plan = request.POST['plan']
            t.save()
            return redirect("/trips")

def info(request,number):
    t = trips.objects.get(id = number)
    context = { "trip": t }
    return render(request, 'info.html',context)

def join (request,number):
    u = User.objects.get(id = request.session['users'])
    t = trips.objects.get(id = number)
    t.memebers.add(u)
    t.save()
    
    return redirect("/trips")
def cancel (request,number):
    trip = trips.objects.get(id = number)
    user = User.objects.get(id = request.session['users'])
    trip.memebers.remove(user)
    return redirect("/trips")