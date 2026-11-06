from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=120)

    class Meta:
        model = User
        fields = ["username", "full_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()  # post_save signal creates the StudentProfile
            user.student_profile.full_name = self.cleaned_data["full_name"]
            user.student_profile.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["full_name", "college", "degree", "graduation_year", "cgpa", "skills", "resume_link"]
        widgets = {
            "skills": forms.TextInput(attrs={"placeholder": "Python, Java, SQL"}),
            "cgpa": forms.NumberInput(attrs={"min": "0", "max": "10", "step": "0.01"}),
        }

    def clean_cgpa(self):
        cgpa = self.cleaned_data["cgpa"]
        if cgpa < 0 or cgpa > 10:
            raise forms.ValidationError("CGPA must be between 0 and 10.")
        return cgpa
