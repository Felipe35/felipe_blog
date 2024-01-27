from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import datetime


# Create your models here.
def get_cur_date():
    date = datetime.datetime.now()
    cur_date = date.strftime("%m %d %Y")
    return cur_date



class Tag(models.Model):
    caption = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.caption}"
    
    class Meta:
        verbose_name_plural = "Tags"


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    e_mail = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Author Entries"

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


class Blog_db(models.Model):
    image = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="blogs")
    date = models.DateField(max_length=100)
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=200)
    content = models.CharField(max_length=250)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    blog_tags = models.ManyToManyField(Tag, null=False)

    class Meta:
        verbose_name_plural = "Blog Entries"

    def __str__(self):
        return f"{self.author}, {self.title}"

    def get_absolute_url(self):
        return reverse("post-detail-page", args=[self.slug])
    


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Blog_db, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return self.title