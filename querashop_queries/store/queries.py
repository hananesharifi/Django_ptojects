from django.db.models import Sum, Avg, Count
from datetime import datetime, timedelta

from store.models import Company, Product, Employee, Customer, Order


def young_employees(job: str):
    return Employee.objects.filter(age__lt=30, job=job)


def cheap_products():
    average_price = Product.objects.aggregate(avg_price=Avg('price'))['avg_price']
    cheap_products = Product.objects.filter(price__lt=average_price).order_by('price')
    return cheap_products.values_list('name', flat=True)

def products_sold_by_companies():
    companies = Company.objects.all()
    result = []

    for company in companies:
        sold_products = company.product_set.aggregate(total_sold=Sum('sold'))['total_sold']
        result.append((company.name, sold_products))
    
    return result


def sum_of_income(start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    return Order.objects.filter(time__gte=start_date, time__lte=end_date).aggregate(income=Sum('price'))['income']


def good_customers():
    last_month_start = datetime.now() - timedelta(days=30)
    valuable_customers = Customer.objects.filter(level='G',order__time__gte=last_month_start).annotate(total_orders=Count('order')).filter(total_orders__gt=10)
    
    result = [(customer.name, customer.phone) for customer in valuable_customers]
    return result


def nonprofitable_companies():
    companies = Company.objects.all()
    result = []

    for company in companies:
        low_sold_products = 0

        for product in company.product_set.all():
            if product.sold < 100:
                low_sold_products += 1

        if low_sold_products >= 4:
            result.append(company.name)

    return result



