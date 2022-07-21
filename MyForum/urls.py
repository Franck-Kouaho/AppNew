from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from accounts.views import signup, logout_user, login_user, myProfile
from articles.views import index, post, respons, publish, get_populare_category, get_subject, get_populare_subcategory, get_suggestion_category, category, subcategory, get_subcategory, comment, like, dislike, unnotice, myPost, follow, delete, notification, edit, search

from MyForum import settings

urlpatterns = [
    path('', index, name="accueil"),
    path('search/', search, name="search"),
    path('publish/', publish, name="publish"),
    path('like/<slug:slug>/<int:id>/', like, name="like"),
    path('dislike/<slug:slug>/<int:id>/', dislike, name="dislike"),
    path('comment/<slug:slug>/<int:id>/', comment, name="comment"),
    path('unnotice/<slug:slug>/<int:id>/', unnotice, name="unnotice"),
    path('mypost/', myPost, name="mypost"),
    path('post/', post, name="post_"),
    path('post/<str:slug>/', post, name="post"),
    path('post/<str:slug>/<int:id>/', respons, name="respons"),
    path('edit/<str:slug>/<int:id>/', edit, name="edit"),
    path('delete/<str:slug>/<int:id>/', delete, name="delete"),
    path('follow/<str:slug>/<int:id>/', follow, name="follow"),
    path('category/<str:slug>/', category, name="category"),
    path('subcategory/<str:slug>/', subcategory, name="subcategory"),
    path('get-sub-category/<int:id>/', get_subcategory, name="get-subcategory"),
    path('get-popular-category/', get_populare_subcategory, name="get-popular-category"),
    path('get-subject/', get_subject, name="get-subject"),
    #path('get-popular-category/', get_populare_category, name="get-popular-category"),
    path('get-surgestion-category/', get_suggestion_category, name="get-surgestion-category"),
    path('notification/', notification, name="notification"),
    path('home/', index, name="home"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('signup/', signup, name="signup"),
    path('my-profile/', myProfile, name="my-profile"),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
