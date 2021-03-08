# importing some functions and libraries
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Home page for the Blog (Home Link on the website)
def home(request):
    return render(request,'home/home.html')

# About Page on the website
def about(request):
    return render(request,'home/about.html')

# contact Page on the website
def contact(request):
    if(request.method=="POST"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Handling the worng inputs in the form
        if(len(name)<4 or len(email)<10):
            messages.error(request,'Please fill the form correctly')
        else:
            a = Contact(name=name,email=email,message=message)
            Contact.save(a)
            messages.success(request,'Your query has been submitted successfully we will contact you shortly')
        return render(request,'home/contact.html')

    return render(request,'home/contact.html')

# Search button functionality and Handling Search Queries
def search_result(request):
    if(request.method=='GET'):
        query = request.GET.get('query')
        if(query==None):
            return render(request,'home/home.html')
        data = {'query':query}
        # Limitng the Characters in the Search
        if(len(query)>78):
            data['posts'] = "" # No results(Empty posts)
        else:
            a1 = Post.objects.filter(title__icontains=query) # If query in title
            a2 = Post.objects.filter(content__icontains = query) # if query in content
            a = a1.union(a2) # Taking union of above two query sets
            data['posts'] = a
            data['number'] = len(a) # No of results
            if(data['number']==0): # If results is zero then sending message
                messages.error(request,"No results found for your query")

        return render(request,'home/search.html',data)
    return render(request,'home/search.html')

# Function for Handle all the working related with signup
def handleSignUp(request):

    # If the request come from a SignUp form then only do all the things
    if request.method == "POST":
        # Get the data of the signup
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        conpassword = request.POST['conpassword']
        ls = name.split(" ")
        # Validating for the input data
        if(User.objects.filter(username=username).exists()): # If user already exits
            messages.error(request,'Username Already Exists please choose some different name')
            return redirect('home')
        if(len(username)>15): # If username is greater then given limit
            messages.error(request,'Username exceeds 15 characters limit')
            return redirect('home')
        elif(username.isalnum()==False): # If username contains other then numbers and characters
            messages.error(request,'Username only containes letters and numbers')
            return redirect('home')
        elif(password!=conpassword): # If Password and Confirm Password Does not Match
            messages.error(request,'Password does not matches')
            return redirect('home')
        elif(" " not in name): # If the name is only first name (Suggest More efficient way)
            messages.error(request,'Please Enter your full name')
            return redirect('home')
        # If no error occur then Creating the user
        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = ls[0]
            myuser.last_name = ls[1]
            myuser.save()
            messages.success(request,'Congratulations....Your account has been created successfully')
            return redirect('home')

    # Else return the 404 Error(on Manually opening this url when request is not Post )
    else:
        return HttpResponse('404','Not Found')

# Function for Handling all the working related with the Login
def handleLogin(request):

    # If the request come from a Login form then only do all the things
    if(request.method=="POST"):
        username = request.POST['loginusername']
        password = request.POST['loginpassword']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Loged in")
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials, Please try agian')
            return redirect('home')
    # Else return the 404 Error(on Manually opening this url when request is not Post )
    return HttpResponse("404","error")

# Logout Function(If the user is login then it will Logout else do nothing)
def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully loged out")
    return redirect('home')


