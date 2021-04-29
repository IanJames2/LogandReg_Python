from django.shortcuts import render, HttpResponse, redirect
from .models import Movie, User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    form = request.POST
    errors = User.objects.basic_validator_reg(form)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")
    else:
        pw_hash = bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
            first_name=form["first_name"],
            last_name=form["last_name"],
            email=form["email"],
            password=pw_hash
        )
    return redirect("/")

def login(request):
    form = request.POST
    errors = User.objects.basic_validator_log(form)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else: 
        user = User.objects.filter(email = request.POST['email'])
        if user:
            user_id = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user_id.password.encode()):
                request.session['user_id'] = user_id.id 
                return redirect('/addmovie')
    return redirect('/')
            # else:
            #     errors['password'] = "invalid login"
            #     return errors
    # request.session['user_id'] = logged_user.id
    # return redirect('/login')

    
     #if bcrypt.checkpw(form["password"].encode(), user.password.encode()) == False: 
        # messages.error(request, "Please check your email and password")
        # return redirect("/")


    #if user.password != form["password"]:
        #messages.error(request, "Please check your email and password")
        #return redirect("/")

def added_movie(request):
    form = request.POST
    errors = Movie.objects.basic_validator(form)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")
        
    movie = Movie.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        year = request.POST['year']
    )
    return redirect("/addmovie")

def movie_input(request):
    if "user_id" not in request.session:
        messages.error(request, "You must log in first!")
        return redirect("/")
    context = {
        'User_ID': User.objects.get(id = request.session['user_id'])
    }
    return render(request, "dashboard.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")    