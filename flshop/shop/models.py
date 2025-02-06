# models.py
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
    CATEGORY_CHOICES = [
        ('flower', 'Цветы'),
        ('bouquet', 'Букеты'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True)

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
        Мы сохраняем заказ перед расчётом общей стоимости, чтобы можно было работать с ManyToMany-связями.
        """
        is_new = self.pk is None  # Проверка, новый ли объект

        # Сначала сохраняем заказ, чтобы был создан ID
        super().save(*args, **kwargs)

        # После сохранения добавляем товары в ManyToMany-связь
        if is_new:  # Только если заказ новый
            total = sum(product.price for product in self.products.all())
            self.total_price = total
            # Нужно сохранить объект после изменения общей стоимости
            super().save(*args, **kwargs)
