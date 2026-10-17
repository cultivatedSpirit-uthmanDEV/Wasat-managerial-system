from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Worker, Order, Delivery
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm, CustomerForm, WorkerForm, DeliveryForm
from django.db.models import Q

# Create your views here.


@login_required
def dashboard(request):
    total_order = Order.objects.all().count()
    pending_orders = Order.objects.filter(status=Order.Status.PENDING).all().count()
    processing_orders = Order.objects.filter(status=Order.Status.PROCESSING).all().count()
    ready_orders = Order.objects.filter(status=Order.Status.READY).all().count()
    out_for_delivery_orders = Order.objects.filter(status=Order.Status.OUT_FOR_DELIVERY).count()
    DELIVERED = Order.objects.filter(status=Order.Status.DELIVERED).all().count()
    CANCELLED = Order.objects.filter(status = Order.Status.CANCELLED).all().count()
    PARTIALLY_DELIVERED = Order.objects.filter(status = Order.Status. PARTIALLY_DELIVERED).all().count()

    context = {
        'total_order' : total_order,
        'pending_orders' : pending_orders,
        'processing_orders' : processing_orders,
        'ready_orders' : ready_orders,
        'out_for_delivery_orders' : out_for_delivery_orders ,
        'DELIVERED': DELIVERED,
        'CANCELLED' : CANCELLED,
        'PARTIALLY_DELIVERED':  PARTIALLY_DELIVERED
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

    total_delivered = form.get_total_delivered()
    remaining_quantity = form.get_remaining_quantity()

    if request.method == "POST" and form.is_valid():
        delivery = form.save(commit=False)
        delivery.order = order
        delivery.save()
        
        total_delivered = form.get_total_delivered()
        remaining_quantity = form.get_remaining_quantity()


        if total_delivered != order.quantity and remaining_quantity != 0:
            order.status = Order.Status.PARTIALLY_DELIVERED
        
            
        elif total_delivered >= order.quantity:
            order.status = Order.Status.DELIVERED

        order.save(update_fields=["status", "updated_at"])
        return redirect("order-detail", pk=order.pk)


    context = {
    "form": form,
    "order": order,
    "remaining_quantity" :  remaining_quantity,
    "total_delivered" : total_delivered
    }
    

    return render(
        request,
        "Actions/create_delivery.html",
        context
    )

def delivery_list(request):
    deliveries = Delivery.objects.all().order_by('created_at')
    context = {
        "deliveries" : deliveries
    }
    return render (request, 'lists/delivery_list.html', context)

# i want to implement search bar

def search_delivery(request):
    query = request.GET.get('q')
    deliveries = Delivery.objects.select_related(
        'order',
        'order__customer',


    )

    if query:
        deliveries = deliveries.filter(
            Q(order__customer__name__icontains = query)
             |Q(order__quantity__icontains = query)
               |Q(recipient__icontains = query)  
        )
    else:
        deliveries = Delivery.objects.all()


    context = {
        'deliveries' : deliveries,
        'query' : query
    }

    return render(request,'lists/delivery_list.html', context )


def search_order(request):
    query = request.GET.get('q')
    orders = Order.objects.prefetch_related(
        'assigned_workers'
    ).select_related(
        'customer'
    )

    if query:
        orders = orders.filter(
          Q(customer__name__icontains = query)
            |Q(assigned_workers__name__icontains = query)
             |Q(created_at__icontains = query))

    else:
        orders = Order.objects.all()


    context = {
        'query' : query,
        'orders': orders
    }


    return render(request,  "lists/order_list.html", context)


def search_customer(request):
    query = request.GET.get('q')
    customer = Customer.objects.all()

    if query:
        customer = customer.filter(
            Q(name__icontains = query)
        )

    else:
        customer = Customer.objects.all()

    return render(request, 'lists/customer_list', context={
        'query' : query,
        'customer' : customer
    })








