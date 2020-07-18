# from django.db import models
# from django.contrib.login.models import User


# class Collection(models.Model):
#     subject = models.CharField(max_length=300, blank=True)
#     owner = models.CharField(max_length=300, blank=True)
#     note = models.TextField(blank=True)
#     created_by = models.ForeignKey(User,
#         related_name="collections", blank=True, null=True,
#         on_delete=models.SET_NULL)

#     def __str__(self):
#         return str(self.id)


# class CollectionTitle(models.Model):
#     """
#     A Class for Collection titles.

#     """
#     collection = models.ForeignKey(Collection,
#         related_name="has_titles", on_delete=models.CASCADE)
#     name = models.CharField(max_length=500, verbose_name="Title")
#     language = models.CharField(max_length=3)


from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Collection(models.Model):
    invoice_no = models.IntegerField()
    invoice_date = models.DateField(default = now)
    # GSTIN = models.CharField(unique=True)
    # SKU = models.CharField(max_length=256)
    # tax_amounts = models.PositiveIntegerField()
    # total_amounts = models.PositiveIntegerField()
    vendor_name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    created_by = models.ForeignKey(User,related_name='collections',blank=True,null=True,on_delete=models.SET_NULL)
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,11}$', message="Enter correctly!")
    #phone_number = models.CharField(validators=[phone_regex],max_length=12,blank=True)

    def __str__(self):
        return str(self.id)

class Document(models.Model):
    pdf_copy = models.FileField(upload_to='pdf', null=True, blank=True)


class CollectionTitle(models.Model):
    """
    A Class for Collection titles.

    """
    collection = models.ForeignKey(Collection,related_name='invoice',on_delete=models.CASCADE)
    item_description = models.CharField(max_length=256)
    item_quantity = models.PositiveIntegerField()
    item_rate = models.PositiveIntegerField()