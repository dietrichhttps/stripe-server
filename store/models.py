from django.db import models


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class Discount(models.Model):
    name = models.CharField(max_length=255)
    percent_off = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage (e.g., 10.00 for 10%)")
    stripe_coupon_id = models.CharField(max_length=255, blank=True, null=True, help_text="Stripe coupon ID if created in Stripe")
    
    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"
    
    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'


class Tax(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tax percentage (e.g., 20.00 for 20%)")
    stripe_tax_rate_id = models.CharField(max_length=255, blank=True, null=True, help_text="Stripe tax rate ID if created in Stripe")
    
    def __str__(self):
        return f"{self.name} ({self.percentage}%)"
    
    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Taxes'


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='orders')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_price(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total = total * (1 - self.discount.percent_off / 100)
        return total
    
    @property
    def currency(self):
        items = self.items.all()
        if items:
            # Use currency from first item, assuming all items have same currency
            return items[0].currency
        return 'usd'
    
    def __str__(self):
        return f"Order #{self.id} - {self.items.count()} items"
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
