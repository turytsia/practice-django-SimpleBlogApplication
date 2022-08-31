from django.db import models
from django.utils.text import slugify

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images", null = True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.blogs.count()})'

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

class Review(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    content = models.TextField(max_length=2000)

    def __str__(self):
        return f'{self.username} ({self.email})'

class Blog(models.Model):
    image = models.ImageField(upload_to="images", null = True)
    name = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='blogs')
    slug = models.SlugField(editable=False, null=True,unique=True)
    tags = models.ManyToManyField(Tag,related_name='blogs')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', null=True)
    reviews = models.ManyToManyField(Review, related_name="reviews", blank = True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args,**kwargs):
        self.slug = slugify(self.name)
        super(Blog, self).save(args, kwargs)