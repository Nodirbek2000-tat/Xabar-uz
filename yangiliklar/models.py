

from django.utils import timezone
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import  AbstractUser

Regular,Premium ="regular","premimum"
Ordinary,Admin = "ordinary","admin"
UZB,RUS,ENG="uzb","rus","eng"


class Users_info(AbstractUser):
    profile_picture_url=models.URLField()
    country=models.CharField(max_length=50,null=False,blank=False)
    last_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    subcription=models.CharField(max_length=30,choices=[
        (Regular,"Regular"),
        (Premium,"Premium")
    ],default=Regular)
    role =models.CharField(max_length=30,choices=[
        (Ordinary,"Ordinary"),
        (Admin,"Admin")
    ],default=Ordinary)
    language=models.CharField(max_length=30,choices=[
        (UZB,"O'znek"),
        (ENG,"ENGLISH"),
        (RUS,"RUS"),
    ],default=UZB)

    def __str__(self):
        return self.get_full_name()





class Tag(models.Model):
    name=models.CharField(max_length=50)
    slug= models.SlugField(unique=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    slug = models.SlugField(unique=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.Status.Published)






# News.published.all()
#News.objects.all()


class New(models.Model):

    class Status(models.TextChoices):
        Draft="DF", "Draft"
        Published = "PB","Published"
    title=models.CharField(max_length=250,null=False,blank=False)
    descripton=models.TextField(null=False,blank=False)
    slug = models.SlugField(unique=True,blank=True)
    image=models.ImageField( upload_to="news_image/",null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    author_id=models.ForeignKey(Users_info,on_delete=models.CASCADE)
    view_count=models.PositiveIntegerField(default=0)
    shared_count=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.Draft)
    like_count=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    published_time=models.DateTimeField(default=timezone.now)
    is_trending=models.BooleanField(default=False)

    objects=models.Manager()
    published=PublishedManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    class Meta:
        ordering=["-published_time"]

    def __str__(self):
        return self.title



class News_Tag(models.Model):
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE)
    new=models.ForeignKey(New,on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.tag} - {self.new}"

class Comments(models.Model):
    class Status(models.TextChoices):
        Draft="DF", "Draft"
        Published = "PB","Published"
    user=models.ForeignKey(Users_info,on_delete=models.CASCADE)
    comment_text=models.TextField()
    new=models.ForeignKey(New,on_delete=models.CASCADE)
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.Draft)
    is_active=models.BooleanField(default=True)
    like_count=models.PositiveIntegerField(default=0)
    is_parent=models.BooleanField(default=False)

    published=PublishedManager()


    def __str__(self):
        return f" {self.user} - {self.comment_text}"


class Contact(models.Model):
    full_name = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.full_name} - {self.subject}"






class Advertisement(models.Model):

    title=models.CharField(max_length=150)
    slug=models.SlugField(unique=True,blank=True)
    image=models.ImageField(upload_to='advertisements/',null=True,blank=True)
    is_active=models.BooleanField(default=True)
    # start_time=models.DateTimeField()
    # end_time=models.DateTimeField()
    click_count=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title








