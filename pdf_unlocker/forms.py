from django import forms

class UploadPDFForm(forms.Form):
    file = forms.FileField()
    password = forms.CharField(widget=forms.PasswordInput)
