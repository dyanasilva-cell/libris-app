# livros/forms.py

from django import forms
from .models import Avaliacao

# 💡 Importações NECESSÁRIAS para a criação de usuário
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Obtém o modelo de usuário padrão (User)
User = get_user_model()


# -------------------------------------------------------------
# 1. FORMULÁRIO EXISTENTE: AvaliacaoForm
# -------------------------------------------------------------
class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nome', 'estrelas', 'texto']

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Seu nome'
            }),
            'texto': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Escreva sua avaliação...',
                'rows': 4
            }),
            'estrelas': forms.HiddenInput(),
        }

        labels = {
            'nome': 'Nome',
            'texto': 'Comentário',
            'estrelas': 'Avaliação',
        }


# -------------------------------------------------------------
# 2. FORMULÁRIO DE CRIAÇÃO DE CONTA DO USUÁRIO
# -------------------------------------------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Labels
        self.fields['username'].label = 'E-mail'
        self.fields['first_name'].label = 'Nome'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirme a Senha'

        # Placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Seu e-mail'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Seu nome'
        self.fields['password1'].widget.attrs['placeholder'] = 'Digite sua senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repita sua senha'

        # Classes CSS
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
