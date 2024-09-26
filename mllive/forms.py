from django import forms
from .models import SklearnModel, SklearnModelInput


class SklearnModelForm(forms.ModelForm):
    class Meta:
        model = SklearnModel
        fields = ['model_name', 'model_file',]
        widgets = {
            'model_file': forms.ClearableFileInput(attrs={'accept': '.pkl,.joblib'}),
        }
        help_texts = {
            'model_file': 'Please upload a file with a .pkl or .joblib extension.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model_file'].help_text = (
            f'<span class="text-white">{self.fields["model_file"].help_text}</span>'
        )


class SklearnModelInputForm(forms.ModelForm):
    class Meta:
        model = SklearnModelInput
        fields = ['input_name']
