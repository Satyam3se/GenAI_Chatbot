from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('hr', 'HR'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Select Your Role")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user, role=self.cleaned_data['role'])
        return user
