from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
#
from apps.blog.managers import PostManager
from apps.users.models import *
# App de terceros
from ckeditor_uploader.fields import RichTextUploadingField


class Topic(models.Model):
    """Class to Topic models"""
    name = models.CharField('Nombre Tema', max_length=255, unique=True)

    class Meta:
        """Metadata to Topic class"""
        verbose_name = 'tema'
        verbose_name_plural = 'temas'
        db_table = 'topic'

    def __str__(self):
        """object string representation"""
        return self.name


class Post(models.Model):
    """Class to Post model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=255, unique=True)
    content = RichTextUploadingField('Contenido')
    is_public = models.BooleanField(default=False)
    image = models.ImageField('Imagen', upload_to='posts')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    is_front_page = models.BooleanField(default=False)
    # Debe ser un campo único
    slug = models.SlugField(editable=False, max_length=300)

    objects = PostManager()

    class Meta:
        """Metadata to Post class"""
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        db_table = 'post'
        ordering = ['-created']

    def __str__(self):
        """object string representation"""
        return self.title

    def save(self, *args, **kwargs):
        """save slug atributte to object"""
        slug_unique = self.title
        self.slug = slugify(slug_unique)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """get unique url for each instance"""
        return reverse('blog:detail', kwargs={
            'slug': self.slug
        })

    def get_like_url(self):
        """get unique url for each instance when, an user to like"""
        return reverse('blog:like', kwargs={
            'slug': self.slug
        })

    @property
    def comments(self):
        """Return all comments relationed for each instance"""
        return self.comment_set.all()

    @property
    def get_all_comments(self):
        """Return the comments quantity relationed for each instance"""
        return self.comment_set.all().count()

    @property
    def get_all_views(self):
        """Return the views quantity relationed for each instance"""
        return self.view_set.all().count()

    @property
    def get_all_likes(self):
        """Return the likes quantity relationed for each instance"""
        return self.like_set.all().count()


class Comment(models.Model):
    """Class to Commnte model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # profile = models.ForeignKey('users.profile', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    content = RichTextUploadingField('Contenido')

    def __str__(self):
        """object string representation"""
        return self.user.username


class View(models.Model):
    """Class to Views model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        """object string representation"""
        return self.user.username


class Like(models.Model):
    """Class to like model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        """object string representation"""
        return self.user.username
