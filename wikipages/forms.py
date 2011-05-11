from django import forms
from wikipages.models import Page
# Create the form class.
class PageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'mce'}))
    class Meta:
        model = Page
        exclude = ('url', 'template_name')
