from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.text import slugify
from django.template import loader
from django.db.models import Q
from articles.models import Article, Category, SubCategory, Like, Notifications, get_user_notifications

# Create your views here.
def index(request):
    articles = Article.objects.filter(
        articleParent=None
        ).order_by('-publish_date')
    context = {"articles" : articles, "author" : request.user}
    template = loader.get_template("articles/index.html")
    return HttpResponse(template.render(context, request))

def post(request, slug=None):
    if not slug:
        return redirect('accueil')
    articles = Article.objects.filter(
        slug=slug,
        articleParent=None
        ).order_by('-publish_date')
    if not len(articles) :
        return redirect('accueil')
    context = {
        "articles" : articles,
        "author" : request.user
        }
    template = loader.get_template("articles/post.html")
    return HttpResponse(template.render(context, request))

def myPost(request):
    if not request.user.is_authenticated:
        return redirect('accueil')
    message = None
    articles = Article.objects.filter(
        author = request.user
        ).order_by('-publish_date')
    if not len(articles) :
        message = "Vous n'avez effecter aucun poste ou réagir à un aucun poste !"
    context = {
        "articles" : articles,
        "author" : request.user,
        "message" : message
        }
    template = loader.get_template("articles/index.html")
    return HttpResponse(template.render(context, request))

def publish(request):
    if not request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        #traiter le formulaire
        author = request.user
        title = request.POST.get("title")
        content = request.POST.get("commentaire")
        subcategory_id = request.POST.get("subcategory")
        subCategory = SubCategory.objects.get(
            id = subcategory_id
        )
        slug = slugify(title)
        if request.POST.get('input_picture') != '' :
            thumbnail = request.FILES['input_picture']
            article = Article.objects.create(
                author = author,
                title = title,
                content = content,
                subCategory = subCategory,
                slug = slug,
                thumbnail = thumbnail,
            )
        else:
            article = Article.objects.create(
                author = author,
                title = title,
                content = content,
                subCategory = subCategory,
                slug = slug,
            )
        article.followers.add(request.user)

        return JsonResponse(
                data={
                    "user": request.user.username,
                    "is_delete" : True,
                }
            )
    
    categories = Category.objects.order_by('name')
    try:
        context = {
        "categories" : categories,
        "subcategories" : categories[0].get_subcategory()
        }
    except:
        context = {
        "categories" : categories,
        "subcategories" : [],
        }
    template = loader.get_template("articles/publish.html")
    return HttpResponse(template.render(context, request))

def edit(request, slug=None, id=None):
    if not request.user.is_authenticated or slug or id:
        return redirect('accueil')
    if request.method == "GET":
        try:
            article = Article.objects.get(id=id)
            return JsonResponse(
                data={
                    "user": request.user,
                    "is_delete" : True,
                }
            )
        except:
            return JsonResponse(
                data={
                    "user": request.user,
                    "is_delete" : False,
                }
            )

def follow(request, slug=None, id=None):
    if (not request.user.is_authenticated) or not slug or not id:
        return redirect(request.META['HTTP_REFERER'])
    if request.method == "GET":
        try:
            article = Article.objects.get(id=id)
            if not request.user in article.get_followers_list():
                article.followers.add(request.user)
            else:
                article.followers.remove(request.user)
            article.save()
        except:
            print('ex')
            pass
        return redirect(request.META['HTTP_REFERER'])

def delete(request, slug=None, id=None):
    if (not request.user.is_authenticated) or not slug or not id:
        return redirect('accueil')
    if request.method == "GET":
        try:
            article = Article.objects.get(id=id)
            if article.articleParent:
                redirect_url = article.articleParent.get_absolute_url()
            article.delete()
        except:
            redirect_url = 'post_'
        return redirect(redirect_url)

def respons(request, slug, id):
    try:
        article = Article.objects.filter(
            slug=slug,
            id=id
        )
    except:
        return redirect('post_')
    context = {
        "articles" : article,
        "author" : request.user
        }
    if len(article):
        if request.user.is_authenticated:
            notifications = Notifications.objects.filter(article=article[0])
            for notification in notifications:
                notification.viewer.add(request.user)
        template = loader.get_template("articles/post.html")
        return HttpResponse(template.render(context, request))
    else:
        return redirect('post_')

def comment(request, slug, id):
    if request.user.is_authenticated and request.method == 'POST':
        try:
            articleParent = Article.objects.filter(id=id)[0]
            #articleParent.followers.add(request.user)
        except AttributeError as e:
            return JsonResponse(data={
                "username" : request.user.username,
                "is_connect" : request.user.is_authenticated,
                "article" : False
            })

        author = request.user
        content = request.POST.get("commentaire")
        if request.POST.get('input_picture') != '' :
            thumbnail = request.FILES['input_picture']
            article = Article.objects.create(
                author = author,
                content = content,
                subCategory = articleParent.subCategory,
                articleParent = articleParent,
                slug = slug,
                thumbnail = thumbnail,
            )
        else:
            article = Article.objects.create(
                author = author,
                content = content,
                subCategory = articleParent.subCategory,
                articleParent = articleParent,
                slug = slug,
            )
        try:
            Notifications.objects.get(article=articleParent, reaction=Notifications.RESPONS).viewer.clear()
        except:
            pass
        article.followers.add(request.user)

        return JsonResponse(data={
            "username" : request.user.username,
            "is_connect" : request.user.is_authenticated,
            "article" : True
        })
    return JsonResponse(data={
        "username" : '',
        "is_connect" : request.user.is_authenticated,
        "article" : True
    })

def category(request, slug=None):
    if not slug:
        return redirect('accueil')
    try:
        cat = Category.objects.get(slug=slug)
        context = {
            "category" : cat,
            "message" : "",
            "author" : request.user
        }
    except :
        context = {
            "category" : "Aucune publication n'est associé à cette categorie !" ,
            "message" : "Aucune publication n'est associé à cette categorie !" 
        }
    template = loader.get_template("articles/categories.html")
    return HttpResponse(template.render(context, request)) 

def subcategory(request, slug=None):
    if not slug:
        return redirect('accueil')
    try:
        subcat = SubCategory.objects.get(slug=slug)
        context = {
            "category" : subcat,
            "message" : "",
            "author" : request.user
        }
    except :
        context = {
            "category" : "Aucune publication n'est associé à cette sous-categorie !" ,
            "message" : "Aucune publication n'est associé à cette sous-categorie !" 
        }
    template = loader.get_template("articles/categories.html")
    return HttpResponse(template.render(context, request)) 

def like(request, slug=None, id=None):
    if(slug==None or id==None or not request.user.is_authenticated):
        return JsonResponse(data={
            'is_connect' : request.user.is_authenticated,
            'request_is_done' : False,
        })

    articles = Article.objects.filter(id=id)
    user = request.user
    if articles != {} and len(articles) == 1:
        like, created = Like.objects.get_or_create(
            author = user,
            article = articles[0]
        )
        if not created :
            like.notice = Like.LIKE
            like.save()

        notification, _ = Notifications.objects.get_or_create(
            article = articles[0],
            reaction = Notifications.LIKE
        )
        notification.viewer.clear()
        notification.viewer.add(user)
        notification.save()
        articles[0].followers.add(request.user)

        return JsonResponse(data={
            'is_connect' : request.user.is_authenticated,
            'request_is_done' : True,
            'like_nber' : articles[0].get_like_number(),
            'dislike_nber' : articles[0].get_dislike_number(),
            'respons_number' : articles[0].get_respons_number(),
        })
    return JsonResponse(data={
        'is_connect' : request.user.is_authenticated,
        'request_is_done' : False,
        'like_nber' : articles[0].get_like_number(),
        'dislike_nber' : articles[0].get_dislike_number(),
        'respons_number' : articles[0].get_respons_number(),
    })

def dislike(request, slug=None, id=None):
    if(slug==None or id==None or not request.user.is_authenticated):
        return JsonResponse(data={
            'is_connect' : request.user.is_authenticated,
            'request_is_done' : True
        })
    articles = Article.objects.filter(id=id)
    user = request.user
    if articles != {} and len(articles) == 1:
        like, created = Like.objects.get_or_create(
            author = user,
            article = articles[0]
        )
        if not created :
            like.notice = Like.DISLIKE
            like.save()
        notification, _ = Notifications.objects.get_or_create(
            article = articles[0],
            reaction = Notifications.DISLIKE
        )
        notification.viewer.clear()
        notification.viewer.add(user)
        notification.save()        
        articles[0].followers.add(request.user)
    return JsonResponse(data={
        'is_connect' : request.user.is_authenticated,
        'request_is_done' : True,
        'like_nber' : articles[0].get_like_number(),
        'dislike_nber' : articles[0].get_dislike_number(),
        'respons_number' : articles[0].get_respons_number(),
    })

def unnotice(request, slug=None, id=None):
    if(slug==None or id==None or not request.user.is_authenticated):
        return JsonResponse(data={
            'is_connect' : request.user.is_authenticated,
            'request_is_done' : True
        })
    articles = Article.objects.filter(id=id)
    user = request.user
    if len(articles) == 1:
        like = Like.objects.filter(
            author = user,
            article = articles[0]
        )
        like.delete()
        notification, _ = Notifications.objects.get_or_create(
            article = articles[0],
            reaction = Notifications.LIKE
        )
        notification.viewer.remove(user)
        notification.save()
    return JsonResponse(data={
        'is_connect' : request.user.is_authenticated,
        'request_is_done' : True,
        'like_nber' : articles[0].get_like_number(),
        'dislike_nber' : articles[0].get_dislike_number(),
        'respons_number' : articles[0].get_respons_number(),
    })

def get_populare_category(request):
    if request.method == 'GET':
        #traiter le formulaire
        categories = Category.objects.all()
        context  = {
            "categories" : categories
        }
        template = loader.get_template("articles/populare_category.html")
        return HttpResponse(template.render(context, request))

def get_populare_subcategory(request):
    if request.method == 'GET':
        #traiter le formulaire
        subcategories = SubCategory.objects.all().filter()
        context  = {
            "subcategories" : subcategories
        }
        template = loader.get_template("articles/populare_subcategory.html")
        return HttpResponse(template.render(context, request))

def get_suggestion_category(request):
    if request.method == 'GET':
        #traiter le formulaire
        categories = Category.objects.all()
        context  = {
            "categories" : categories
        }
        template = loader.get_template("articles/surgestion_category.html")
        return HttpResponse(template.render(context, request))

def get_subject(request):
    if request.method == 'GET':
        #traiter le formulaire
        articles = Article.objects.filter(articleParent=None)[:10]
        context  = {
            "articles" : articles
        }
        template = loader.get_template("articles/subject.html")
        return HttpResponse(template.render(context, request))

def get_subcategory(request, id):
    if request.method == 'GET':
        try:
            category = Category.objects.filter(id=id)[0]
            subcategories = dict()
            for subcategory in category.get_subcategory():
                subcategories[subcategory.id] = subcategory.name
        except:
            print('ex')
            subcategories = {}
        return JsonResponse(data=subcategories)

def get_notification(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context  = {
            "categories" : categories,
            "user" : request.user
        }
        template = loader.get_template("articles/surgestion_category.html")
        return HttpResponse(template.render(context, request))

def notification(request):
    if not request.user.is_authenticated:
        return redirect('accueil')
    notifications = get_user_notifications(user=request.user)
    context = {"notifications" : notifications, "author" : request.user}
    template = loader.get_template("articles/notification.html")
    return HttpResponse(template.render(context, request))

def search(request):
    results = []
    if request.method == "GET":

        query = request.GET.get('search')

        if query == '':

            query = 'None'

        results = Article.objects.filter(
            Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query) | Q (subCategory__name__icontains=query) | Q (slug__icontains=query) | Q (subCategory__category__name__icontains=query)
        )

    return render(request, 'articles/search.html', {'query': query, 'results': results})