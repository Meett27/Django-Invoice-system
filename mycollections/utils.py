from .models import Collection,CollectionTitle
import datetime
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site


def everyday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    try:
        data = CollectionTitle.objects.get(invoice_date=yesterday)
        items = Collection.objects.filter(invoice_number = data)
        all_data = CollectionTitle.objects.filter(invoice_date=yesterday)
        for ite in items:
            print(ite.item_rate)
            summation += ite.item_rate*ite.item_quantity
        Invoices,total =  len(all_data),summation
    except:
        return 0,0

   
    title = 'Summary'
    message = 'Hello {0}, Summary for {1}.No. of invoices:{2},Total amount:{3}'.format('Meet',yesterday,Invoices,total)
    email = 'meet2579@yahoo.com'
    user = 'trivedimeet505@yahoo.com'
    send_mail(title,message,email,[user],fail_silently=False)
