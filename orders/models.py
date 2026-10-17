from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    whatsapp_num = models.CharField(max_length=11)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Worker(models.Model):
    name = models.CharField(max_length=100)
    whatsapp_num = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        READY = "READY", "Ready"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"
        PARTIALLY_DELIVERED = "PARTIALLY_DELIVERED", "Partially Delivered"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    order_number = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            super().save(*args, **kwargs)
            self.order_number = f"ORD-{self.id:05d}"

        super().save(*args, **kwargs)
    def __str__(self):
        return self.order_number
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    price = models.DecimalField(max_digits=12,decimal_places=2,)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    expected_completion_date = models.DateField()
    assigned_workers = models.ManyToManyField(
        Worker,
        null=True,
        blank=True,
        related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class Process(models.Model):
        order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="processes")
        worker = models.ForeignKey(
            Worker,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="processes"
        )

        start_time = models.DateTimeField(null=True, blank=True)
        completion_time = models.DateTimeField(null=True, blank=True)
        notes = models.TextField(blank=True)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)


class Delivery(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete= models.CASCADE,
        related_name="deliveries",
        blank=True,
        null=True)
    quantity_delivered = models.PositiveIntegerField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivered_by = models.CharField(max_length=150, blank=True)
    recipient = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    address = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


