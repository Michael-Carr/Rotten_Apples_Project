from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request,'index.html')

def hub(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'games': Vgame.objects.all()
    }
    return render(request,'hub.html',context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.validate(request.POST)
        if errors:
            for error in errors.values():
                messages.error(request,error)
            return redirect('/')
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(username=username,email=email,password=pw_hash)
        request.session['user_id'] = user.id
        request.session['user_name'] = user.username
        return redirect('/hub')

    return redirect('/')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        logged_user = User.objects.filter(username=username) 
        if logged_user:
            logged_user = logged_user[0]
            
            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = logged_user.username
                return redirect('/hub')
            else:
                messages.error(request,"This password isnt't correct")
                return redirect('/')
        else:
            messages.error(request,"This user doesn't exist!")
            return redirect('/')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def addgame(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request,'addgame.html')

def newgame(request):
    errors = Vgame.objects.validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addgame')
    Vgame.objects.create(
        title = request.POST['title'],
        platform = request.POST['platform'],
        release_date = request.POST['release_date'],
        description = request.POST['description'],
        image_url = request.POST['image_url']
    )

    return redirect('/hub')

def showgame(request, game_id):
    if 'user_id' not in request.session:
            return redirect('/')
    show_game = Vgame.objects.get(id=game_id)
    context = {
        'showgame':show_game,
        'post': GameReview.objects.all()
    }

    return render(request,'showgame.html',context)

def edit(request, game_id):
    edit_game = Vgame.objects.get(id=game_id)
    context = {
        'edit': edit_game,        
    }
    return render(request, 'edit.html',context)

def update(request, game_id):
    errors = Vgame.objects.validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{game_id}/edit')
    to_update = Vgame.objects.get(id=game_id)
    to_update.title = request.POST['title']
    to_update.platform = request.POST['platform']
    to_update.release_date = request.POST['release_date']
    to_update.description = request.POST['description']
    to_update.image_url = request.POST['image_url']
    to_update.save()
    return redirect('/hub')

def delete(request, game_id):
    if 'user_id' not in request.session:
            return redirect('/')
    to_delete = Vgame.objects.get(id=game_id)
    to_delete.delete()
    return redirect('/hub')

def create_post(request,id):
    post = request.POST['post']
    poster = User.objects.get(id = request.session["user_id"])

    review = Vgame.objects.get(id=id)
    GameReview.objects.create(post=post,poster=poster,review=review)
    #return redirect('/hub')

    return redirect(f'/{review.id}')


def delete_post(request,id):
    delete_post = GameReview.objects.get(id=id)
    delete_post.delete()
    return redirect('/hub')

def add_like(request,id):
    liked_post = GameReview.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_post.likes.add(user_liking)
    return redirect('/hub')