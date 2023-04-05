from django import forms



class MotagraSelectForm(forms.Form):
    motagra_name = forms.CharField(label ='اسم المتاجرة',max_length=64)