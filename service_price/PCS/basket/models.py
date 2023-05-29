from django.db import models
from products.models import Product
# Create your models here.


class Basket(models.Model):
    total_dns = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_mvideo = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_regard = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Cart id: {}".format(self.id)


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, null=True, blank=True, on_delete=models.CASCADE)
    # Basket foriegn key
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product_total = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    # product total
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        try:
            return str(self.basket.id)
        except AttributeError:
            return self.product.name
