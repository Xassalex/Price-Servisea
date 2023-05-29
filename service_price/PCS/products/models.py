from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(default='default-product.png', blank=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('products:filtered_products', args=[self.slug])



    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)

    url_dns = models.CharField(max_length=250, db_index=True)
    url_mvideo = models.CharField(max_length=250, db_index=True)
    url_regard = models.CharField(max_length=250, db_index=True)

    price_dns = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_mvideo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_regard = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(default='default-product.png', blank=True)
    # изображенье должно быть 140х140

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
