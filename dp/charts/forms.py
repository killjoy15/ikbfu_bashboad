from django import forms

class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

#??????
# class ExportForm(forms.Form):
#     articles = forms.ModelMultipleChoiceField(
#         # queryset = Article.objects.all(), # or .filter(…) if you want only some articles to show up
#         #  вписать данные в виде списка кортежей
#         widget  = forms.CheckboxSelectMultiple
#     )

# class ModelMultipleChoiceField(**kwargs)