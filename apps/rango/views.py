# -*- coding:utf-8 -*-
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore

# from django.templatetags.static import
from .models import Category, Page
from .forms import CategoryForm, PageForm
from .forms import UserForm, UserProfileForm


# Create your views here.
def _index(request):
    category_list = Category.objects.order_by('-links')
    context_dict = {'categories': category_list}
    template_name = 'rango/rango_index.html'
    print(request.user.is_authenticated())

    # print(request.session, type(request.session))
    return render(request, template_name=template_name, context=context_dict)


def index_(request):
    template_name = 'rango/rango_index.html'

    category_list = Category.objects.all()
    page_list = Page.objects.order_by('-views')
    context_dict = {'categorirs': category_list, 'pages': page_list}

    visits = int(request.COOKIES.get('visits', 1))
    reset_last_visit_time = False
    response = render(request, template_name, context=context_dict)

    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 5:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
        context_dict['visits'] = visits
        response = render(request, template_name, context_dict)

    if reset_last_visit_time:
        response.set_cookie('last_visit', datetime.now())
        response.set_cookie('visits', visits)
    return response


def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    response = render(request, 'rango/rango_index.html', context_dict)
    print('last_visit:', request.session['last_visit'])
    print('visits:', request.session['visits'])

    return response


def category(request, category_name_slug):
    template_name = 'rango/category.html'
    context_dict = {}

    try:
        _category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = _category.name

        pages = Page.objects.filter(category=_category)
        context_dict['pages'] = pages
        context_dict['category'] = _category
    except Category.DoesNotExist:
        print('`Category` dont exist')

    return render(request, template_name, context_dict)


@login_required
def like_category(request):
    cat_id = None
    likes = 0

    if request.method == 'GET':
        cat_id = request.GET['category_id']

    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        likes = cat.likes + 1
        cat.likes = likes
        cat.save()
    return HttpResponse(likes)


def about(request):
    template_name = 'rango/about.html'

    return render(request, template_name)


def add_category(request):
    template_name = 'rango/add_category.html'

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # print form

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    # print(form.hidden_fields)
    # print(form.visible_fields)
    return render(request, template_name, context={'form': form})


def register(request):
    template_name = 'rango/register.html'
    registered = False

    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, template_name,
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    template_name = 'rango/login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, template_name, {})


@login_required
def restricted(request):
    print('si login:', request.user.is_authenticated())
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
