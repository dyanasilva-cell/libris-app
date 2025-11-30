from django import forms
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nome', 'estrelas', 'texto']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome'
            }),
            'estrelas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1, 'max': 5,
                'placeholder': 'De 1 a 5 estrelas'
            }),
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva sua avaliação aqui...',
                'rows': 3
            }),
        }
        labels = {
            'nome': 'Nome',
            'estrelas': 'Estrelas (1 a 5)',
            'texto': 'Comentário',
        }
