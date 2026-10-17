from django import forms
from orders.models import Order, Customer, Worker, Delivery

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer",
            "description",
            "quantity",
            "price",
            "expected_completion_date",
            "assigned_workers",
        ]

        widgets = {
            "expected_completion_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4}),
            "assigned_workers": forms.SelectMultiple(
                attrs={
                    "class": "worker-select",
                }
            ),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
          'name', 'phone', 'whatsapp_num','address'
        ]


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = [
            'name', 'whatsapp_num','role', 'is_active'
        ]

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = [
            "delivery_date",
            "delivered_by",
            "recipient",
            "quantity_delivered",
            "notes",
        ]


        widgets = {
        "delivery_date" : forms.DateInput(
            attrs={'type' : 'date'}
        )
    }

    def __init__(self, *args, order=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order

   

    def get_total_delivered(self):
        if self.order is None:
            return 0

        return sum(
            delivery.quantity_delivered or 0
            for delivery in self.order.deliveries.all()
        )
    def get_remaining_quantity(self):

       return ( self.order.quantity - self.get_total_delivered())


    def clean_quantity_delivered(self):
            quantity = self.cleaned_data["quantity_delivered"]
            remaining = self.get_remaining_quantity()

            if quantity > remaining or quantity == 0:
               raise forms.ValidationError(
                f"Only {remaining} units remain to be delivered."
            )

            return quantity
        