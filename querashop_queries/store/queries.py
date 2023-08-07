from django.db.models import Avg, Count, Sum
from datetime import datetime, timedelta
from store.models import Employee ,Company ,Customer ,Product ,Order

def young_employees(job: str):
    return Employee.objects.filter(age__lt=30, job=job)

def cheap_products():
    avgPrice = Product.objects.aaggregate(Avg('price'))['price__avg']
    cheap = Product.objects.filter(price__lt=avgPrice).order_by('price')
    return cheap

def products_sold_by_companies():
    companies = Company.objects.prefetch_related('product_set')
    result = []
    for company in companies:
        products_sold = [(product.name, product.sold) for product in company.product_set.all()]
        result.append((company.name, products_sold))
    return result

def sum_of_income(start_date: str, end_date: str):
    start_date_obj = datetime.strptime(start_date ,'%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date ,'%Y-%m-%d')
    
    income_sum = Order.objects.filter(date__gte=start_date_obj, date__lte=end_date_obj).aggregate(Sum('price'))['price__sum']

    return income_sum

def good_customers():
    # Calculate the date range for the past month
    today = datetime.now().date()
    last_month_start = (today - timedelta(days=30)).replace(day=1)
    
    # Retrieve customers with more than 10 purchases in the past month
    return Customer.objects.annotate(purchase_count=Count('purchase')).filter(
        purchase__purchase_date__gte=last_month_start,
        purchase_count__gt=10
    )

def nonprofitable_companies():
    return Company.objects.annotate(
        product_count=Count('product', filter=models.Q(product__price__lt=100))
    ).filter(product_count__gte=4)
