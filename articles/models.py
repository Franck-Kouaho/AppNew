from django.urls import reverse
from django.db import models

from accounts.models import CustomUser

# Create your models here.

class Category(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.TextField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

    def get_subcategory(self):
        return SubCategory.objects.filter(category=self).order_by('name')

    def get_article(self):
        return Article.objects.filter(subCategory__category=self, articleParent=None).order_by('-publish_date')
    
    def get_article_number(self):
        return Article.objects.filter(subCategory__category=self, articleParent=None).count()

    def get_subcategorie_number(self):
        return SubCategory.objects.filter(category=self).count()

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        
class SubCategory(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse("subcategory", kwargs={"slug": self.slug})

    def get_article(self):
        return Article.objects.filter(subCategory=self, articleParent=None).order_by('-publish_date')

    def get_article_number(self):
        return Article.objects.filter(subCategory=self, articleParent=None).count()

    class Meta:
        verbose_name = "Sous-catégorie"
        verbose_name_plural = "Sous-catégories"

class Article(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=128)
    content = models.TextField(blank=True)
    subCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    articleParent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    followers = models.ManyToManyField(CustomUser, default=author, related_name="followers")
    slug = models.SlugField(max_length=128)
    thumbnail = models.ImageField(upload_to="postImage", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.author}: {self.title}"
    
    def get_absolute_url(self):
        return reverse("respons", args=(self.slug, self.id))

    def get_delete_url(self):
        return reverse('delete', kwargs={"slug" : self.slug, "id" : self.id})

    def get_edit_url(self):
        return reverse('edit', kwargs={"slug" : self.slug, "id" : self.id})

    def get_comment_url(self):
        return reverse('comment', kwargs={"slug" : self.slug, "id" : self.id})

    def get_like_number(self):
        return Like.objects.filter(article=self, notice=Like.LIKE).count()

    def get_dislike_number(self):
        return Like.objects.filter(article=self, notice=Like.DISLIKE).count()

    def get_all_respons(self):
        arts = Article.objects.filter(articleParent=self)
        all_articles = list(arts)
        for art in arts:
            all_articles.append(list(art.get_all_respons()))
        return tuple(all_articles)

    def get_respons_number(self):
        arts = Article.objects.filter(articleParent=self)
        nber = arts.count()
        for art in arts:
            nber = nber + art.get_respons_number()
        return nber

    def get_respons(self):
        return Article.objects.filter(articleParent=self)

    def get_liker(self):
        return Like.objects.filter(article=self, notice=Like.LIKE)

    def get_disliker(self):
        return Like.objects.filter(article=self, notice=Like.DISLIKE)

    def add_follower(self, user):
        self.followers.add(user)
        self.save()
    
    def get_followers_list(self):
        return self.followers.all()

    def get_followers_numbers(self):
        return self.followers.all().count()

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

class Respons(Article):
    def __str__(self) -> str:
        return f"{self.author} --> {self.articleParent.author} : {self.articleParent.title}"
    class Meta:
        proxy = True
        verbose_name = "Réponse"
        verbose_name_plural = "Réponses"

class Like(models.Model):
    LIKE = 'LK'
    DISLIKE = 'DL'
    NOTICE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    notice = models.CharField(
        max_length=2,
        choices=NOTICE_CHOICES,
        default=LIKE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'article'], name='unique_author_article'),
        ]

    def __str__(self) -> str:
        return f"{self.author}: {self.notice}"
    
class Notifications(models.Model):
    LIKE = 'LK'
    DISLIKE = 'DL'
    RESPONS = 'RP'
    NOTICE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
        (RESPONS, 'Respons'),
    ] 
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    viewer = models.ManyToManyField(CustomUser)
    date = models.DateTimeField(auto_now=True)
    reaction = models.CharField(
        max_length=2,
        choices=NOTICE_CHOICES,
        null=False
    )

    def get_viewer_list(self):
        return self.viewer

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reaction', 'article'], name='unique_reaction_article'),
        ]
        ordering = ['-date']

def get_user_notifications(user):
    return Notifications.objects.filter(article__followers=user).order_by('-date')
    
# class User(CustomUser):
#     def get_user_article(self):
#         return Article.objects.filter(author=self)

#     def get_user_article_number(self):
#         return Article.objects.filter(author=self).count()