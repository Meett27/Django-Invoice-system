from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *


class CollectionTitleForm(forms.ModelForm):

    class Meta:
        model = CollectionTitle
        exclude = ()
        widgets = {
            'invoice_date': forms.DateInput()
        }

CollectionTitleFormSet = inlineformset_factory(
    Collection, CollectionTitle, form=CollectionTitleForm,
    fields='__all__', extra=2, can_delete=True
    )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('pdf_copy',)

class CollectionForm(forms.ModelForm):

    class Meta:
        model = Collection
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('invoice_no'),
                Field('invoice_date'),
                Field('vendor_name'),
                Field('email'),
                Fieldset('Add titles',
                    Formset('titles')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
                )
            )

