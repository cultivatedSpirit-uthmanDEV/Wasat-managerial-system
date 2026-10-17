from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Worker, Order
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm, CustomerForm, WorkerForm, DeliveryForm

# Create your views here.


@login_required
def dashboard(request):
    total_order = Order.objects.count()
    pending_orders = Order.objects.filter(status=Order.Status.PROCESSING).count()
    processing_orders = Order.objects.filter(status=Order.Status.PROCESSING).count()
    ready_orders = Order.objects.filter(status=Order.Status.READY).count()
    out_for_delivery_orders = Order.objects.filter(status=Order.Status.OUT_FOR_DELIVERY).count()
    DELIVERED = Order.objects.filter(status=Order.Status.DELIVERED).count()
    CANCELLED = Order.objects.filter(status = Order.Status.CANCELLED).count()

    context = {
        'total_order' : total_order,
        'pending_orders' : pending_orders,
        'processing_orders' : processing_orders,
        'ready_orders' : ready_orders,
        'out_for_delivery_orders' : out_for_delivery_orders ,
        'DELIVERED': DELIVERED,
        'CANCELLED' : CANCELLED,
    }

    return render(request, 'dashboard.html' , context)

def customer_list(request):
    customers = Customer.objects.all().order_by("-created_at")

    return render(
        request,
        "lists/customer_list.html",
        {"customers": customers},
    )


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    return render(
        request,
        "details/customer_detail.html",
        {"customer": customer},
    )


def worker_list(request):
    workers = Worker.objects.all().order_by("name")

    return render(
        request,
        "lists/worker_list.html",
        {"workers": workers},
    )

def order_list(request):
    orders = Order.objects.select_related(
        "customer").prefetch_related(
        "assigned_workers", "deliveries").order_by("-created_at")

    return render(
        request,
        "lists/order_list.html",
        {"orders": orders},
    )

def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related(
            "customer").prefetch_related(
            "assigned_workers","deliveries"),
        pk=pk
    )

    return render(
        request,
        "details/order_detail.html",
        {"order": order},
    )

# CRUD for management

def create_order(request):
    if request.method == "POST":

        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("order-list")

        print("FORM ERRORS:", form.errors)

    else:
        form = OrderForm()

    return render(
        request,
        "Actions/create_order.html",
        {"form": form}
    )

def create_worker(request):
    form = WorkerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("worker-list")

    context = {
        "form" : form
    }

    return render(request, 'Actions/create_worker.html', context)

def create_customer(request):
    form =  CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('customer-list')

    context = {
        'form': form
    }

    return render(request, 'Actions/create_customer.html', context)

def create_delivery(request, pk):
    order = get_object_or_404(Order, pk=pk)

    form = DeliveryForm(
        request.POST or None,
        order=order
    )

    if request.method == "POST" and form.is_valid():
        delivery = form.save(commit=False)
        delivery.order = order
        delivery.save()

        return redirect("order-detail", pk=order.pk)

    return render(
        request,
        "orders/delivery_form.html",
        {
            "form": form,
            "order": order,
        }
    )





