from django.shortcuts import render
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your views here.


class category(models.Model):
    categories = models.CharField(max_length=200, unique=True)
    categories_image = models.ImageField(
        upload_to='photos/categories', default='No image available')
    categories_discription = models.TextField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.categories)
        super(category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
