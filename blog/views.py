# Importing the some libraries and functions which are required for the site
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .models import Post, BlogComments
from django.contrib import messages
from blog.templatetags import extras

# Home page for the blog posts (Blog page on website)
def bloghome(request):
    a = reversed(Post.objects.all())
    ls = {'posts':a}
    return render(request,'blog/bloghome.html',ls)


# Fetching the blog with required sno as slug and sending to blogpost.html with the comments and replies
def blogpost(request,slug):
    a = Post.objects.filter(sno = slug) # Fetching the required Post
    # Handling the number of view (Please suggest Improvements)
    b = Post.objects.filter(sno = slug).first()
    b.views = b.views+1
    b.save()

    # Fetching the comments whose parent is none means comment
    comments = reversed(BlogComments.objects.filter(post=a[0],parent=None))
    no = BlogComments.objects.filter(post=a[0],parent=None).count() # Number of comments

    # Fetching the replies and collecting all replies respective to their parent comment in dictionary
    replies = reversed(BlogComments.objects.filter(post=a[0]).exclude(parent=None))
    replydict = {}
    for reply in replies:
        if(reply.parent.sno in replydict.keys()):
            replydict[reply.parent.sno].append(reply)
        else:
            replydict[reply.parent.sno] = [reply]
    
    # For the Latest Posts
    latest = Post.objects.all()

    # Sending all the variables to the blogpost.html file 
    return render(request,'blog/blogpost.html',{'post':a[0],'latest':latest[0:4],'comments':comments ,'number':no,'replyDict':replydict})


# Function that handles the Comment
def PostComment(request):
    if request.method == "POST":

        parent = request.POST.get('serialnoreply')
        # If the request is from the form whose hidden input name serialnoreply is empty then it is comment and if it is not empty then it is a reply
        if(parent==" "):
            # comment
            comment = request.POST.get('comment')
            user = request.user
            postId = request.POST.get('postid')
            post = Post.objects.get(sno=postId)
            c = BlogComments(comment=comment,user=user,post=post)
            c.save()
            messages.success(request,'Your comment has been posted successfully')
        else:
            # Reply
            reply = request.POST.get('reply')
            user = request.user
            postId = request.POST.get('postid')
            post = Post.objects.get(sno=postId)
            p = BlogComments.objects.filter(sno=parent)[0]
            c = BlogComments(comment=reply,user=user,post=post,parent=p)
            c.save()
            messages.success(request,'Your reply has been posted successfully')

    # Redirecting to the same post when a comment is published
    return redirect(f'http://127.0.0.1:8000/blog/{post.sno}')