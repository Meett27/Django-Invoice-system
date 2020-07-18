from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Collection,CollectionTitle
from .forms import *
from django.db import transaction
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
# Create your views here.

url = ''

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('/logic/')

		if group == 'admin':
			return view_func(request, *args, **kwargs)
		
		else:
			return redirect('/logic/')

	return wrapper_function


def managermail(request,mail):
    subject = 'An agent Just added new invoice.Link For access Token'
    body =str(get_current_site(request))+'/invoice/viewmanager/'
    myemail = 'meet2579@yahoo.com'
    reciepent = str(mail)
    send_mail(subject,body,myemail,[reciepent],fail_silently=False)


class HomepageView(TemplateView): 
    template_name = "mycollections/base.html"
    model = Collection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collections'] = self.model.objects.filter(created_by=self.request.user)
        return context

class CollectionListView(ListView):
    model = Collection
    template_name = 'mycollections/collection_list.html'
    context_object_name = 'invoices'

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            context = super().get_context_data(**kwargs)
            context['invoices'] = Collection.objects.all()
            return context
        else:
            return redirect('/logic/')

class UploadBookView(CreateView):
    model = Collection
    form_class = DocumentForm
    context_object_name = 'uploaded_file'
    success_url = '/logic/collection/create'
    template_name = 'mycollections/uploadbook.html'

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'mycollections/collection_detail.html'
    context_object_name = 'invoice_details'

    def get_context_data(self, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(**kwargs)
        return context

class CollectionCreate(CreateView):
    model = Collection
    template_name = 'mycollections/collection_create.html'
    form_class = CollectionForm
    success_url = '/logic/'

    def managermail(self,request,mail):
        subject = 'Link For Detail'
        body =str(get_current_site(request))+'/collection/manager/'
        myemail = 'meet2579@yahoo.com'
        reciepent = str(mail)
        send_mail(subject,body,myemail,[reciepent],fail_silently=False)

    def get_context_data(self, **kwargs):
        data = super(CollectionCreate, self).get_context_data(**kwargs)
        upload = Document.objects.filter().order_by('-id').first()
        global  url
        if self.request.POST:
            data['titles'] = CollectionTitleFormSet(self.request.POST)
            data['upload'] = url   
            mail = Collection.objects.filter(created_by=self.request.user).values('email').order_by('id')
            #self.managermail(self.request,'trivedimeet505@gmail.com')
        else:
            data['titles'] = CollectionTitleFormSet()
            data['upload'] = url
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            #form.instance.created_by = 'demo123'
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(CollectionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mycollections:homepage')


    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(CollectionCreate, self).dispatch(*args, **kwargs)


class CollectionUpdate(UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'mycollections/collection_create.html'

    def get_context_data(self, **kwargs):
        data = super(CollectionUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = CollectionTitleFormSet(self.request.POST, instance=self.object)
        else:
            data['titles'] = CollectionTitleFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(CollectionUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mycollections:collection_detail', kwargs={'pk': self.object.pk})

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(CollectionUpdate, self).dispatch(*args, **kwargs)


class CollectionDelete(DeleteView):
    model = Collection
    template_name = 'mycollections/confirm_delete.html'
    success_url = reverse_lazy('mycollections:homepage')


def upload(req):
    userid = req.user.id
    if req.method == 'POST':
        print('post')
        filename = req.FILES['pdf_copy']
        if filename.size > 2097152:
            # messages.error(req, 'File above limit')
            return render(req, 'hello.htm')
        print(filename.size)
        fs = FileSystemStorage()
        name = fs.save(filename.name, filename)

        global url
        url = fs.url(name)

    return redirect('/logic/collection/create')

