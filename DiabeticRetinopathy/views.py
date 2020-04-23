import base64
from fastai.vision import *


from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect



# Create your views here.
from DiabeticRetinopathy.forms import RegisterForm, LoginForm, ReportForm
from DiabeticRetinopathy.models import Report
from .render import Render




def homeview(request):
    global load_learner
    if not request.user.is_authenticated:
        if request.method == 'POST' and 'register' in request.POST:
            registerform = RegisterForm(request.POST)
            if registerform.is_valid():
                user = registerform.save()
                new_user = authenticate(email=registerform.cleaned_data['email'],
                                        password=registerform.cleaned_data['password1'],
                                        )
                login(request, new_user)
                return redirect('DR:homeview')
            else:
                return HttpResponse('{}'.format(registerform.errors))
        elif request.method == 'POST' and 'login' in request.POST:
            loginform = LoginForm(request.POST)
            if loginform.is_valid():
                user_obj = loginform.cleaned_data.get('user_obj')
                login(request, user_obj)
                return redirect('DR:homeview')
            else:
                return HttpResponse('{}'.format(loginform.errors))
        else:
            loginform = LoginForm()
            registerform = RegisterForm()
            return render(request,'DiabeticRetinopathy/login.html',{'loginform': loginform, 'registerform':registerform})
    else:
        if request.method == 'POST':
            if 'upload' in request.POST:
                reportform = ReportForm(request.POST, request.FILES)
                if reportform.is_valid():
                    report = reportform.save()
                    report = Report.objects.get(uuid__exact=report.uuid)
                    learn = load_learner('')
                    category = learn.predict(open_image(report.photo.path))[0]
                    request.session['category'] = category.__int__()
                    params = {
                        'first_name': report.first_name,
                        'last_name': report.last_name,
                        'age': report.age,
                        'gender': report.gender,
                        'photo': report.photo,
                        'date1': report.date,
                        'category': request.session.get('category'),
                        'pid': report.uuid
                    }
                    return render(request,'DiabeticRetinopathy/report.html',params)
            if 'Download' in request.POST:
                report = Report.objects.latest('date')
                params = {
                'first_name'    : report.first_name,
                'last_name'     : report.last_name,
                'age'           : report.age,
                'gender'        : report.gender,
                'photo'         : report.photo,
                'date1'         : report.date,
                'category'      : request.session.get('category')
                }
                return Render.render('DiabeticRetinopathy/pdf.html', params)
        reportform = ReportForm()
        return render(request,'DiabeticRetinopathy/upload.html',{'reportform':reportform})

def user_logout(request):
    logout(request)
    return redirect('DR:homeview')

def teamview(request):
    return render(request,'DiabeticRetinopathy/team.html')