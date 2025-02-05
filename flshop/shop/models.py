from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Собственная модель пользователя, основанная на AbstractUser.
    Здесь можно добавить дополнительные поля, если потребуется.
    """

    # Пример дополнительного поля (необязательно):
    # phone_number = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # Если хотите переопределить группы и права:
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.username


class Product(models.Model):
    """
    Модель товара (букета) с информацией: название, описание, цена, изображение.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Модель заказа, связывающая пользователя и список товаров с дополнительными полями:
    дата доставки, время доставки, адрес, комментарий и общая стоимость.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    products = models.ManyToManyField(Product, related_name='orders')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    delivery_address = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.pk} by {self.user.username}'

    def save(self, *args, **kwargs):
        """
        При сохранении заказа рассчитываем общую стоимость, суммируя цены всех выбранных товаров.
        Обратите внимание, что при первичном создании заказа ManyToMany-связи еще не установлены.
        Поэтому этот метод можно доработать, например, с использованием сигналов (post_save),
        либо рассчитать сумму в отдельном методе после добавления товаров.
        """
        if not self.total_price:
            total = sum(product.price for product in self.products.all())
            self.total_price = total
        super().save(*args, **kwargs)
