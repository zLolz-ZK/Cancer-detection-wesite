from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.fields.files import ImageField
from django.forms import fields, widgets
from django.utils.translation import ugettext_lazy as _
from .models import Doctor, Patient, SomeImage
from crispy_forms.helper import FormHelper

class CustomDateInput(forms.DateInput):
    input_type = 'date'



class DoctorSignUpForm(UserCreationForm):
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    fname = forms.CharField(min_length=2,max_length=30, required=True, 
        widget=forms.TextInput(attrs={'placeholder' : 'Enter Your First Name' }))
    username = forms.CharField(min_length=2,max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder' : 'Enter Your First Name' }))
    mob_no = forms.CharField(min_length=10,max_length=10,
    widget=forms.TextInput(attrs={'placeholder' : 'Enter Your Mobile Number' }))
    class Meta:
        model = Doctor
        fields = [
            'password1',
            'password2',
            'fname',
            'lname',
            'username',
            #'password',
            'hospital_name',
            'email',
            "dob",
            "designation",
            "gender",
            "mob_no",
        ]
        widgets = {
        #'password': forms.PasswordInput(attrs={'placeholder' : 'Enter Your First Name' }),
        'lname' : forms.TextInput(attrs={'placeholder' : 'Enter Your Last Name' }),
        'hospital_name' : forms.TextInput(attrs={'placeholder' : 'Enter Your hospital Name' }),
        'designation' : forms.TextInput(attrs={'placeholder' : 'Enter Your Designation' }),
        
        'email' : forms.EmailInput(attrs={'placeholder' : 'Enter Your Email ID' }),
        "dob" : CustomDateInput(),
        }




class PatientRegistrationForm(forms.ModelForm):        
    fname = forms.CharField(min_length=2,max_length=30, required=True, 
        widget=forms.TextInput(attrs={'placeholder' : 'Enter Your First Name' } ))
    lname = forms.CharField(min_length=2,max_length=30, required=True, 
        widget=forms.TextInput(attrs={'placeholder' : 'Enter Your Last Name' } ))
    email_id = forms.CharField(min_length=5, required=False,
                 widget=forms.EmailInput(attrs={'placeholder' : 'Enter Your Email ID', 'size':60 } ),)
    def __init__(self, *args, **kwargs):
        super(PatientRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
    class Meta:
        model = Patient
        fields = [
        'patient_id',
        #'doctor',
        'fname',
        'lname',
        'email_id',
        'dob',
        'gender',
        'symptoms',
        'mob_no',
        'weight',
        'height',
        'img',
        #'cropping',
        'allergies',
        'family_history',
        'products_used',
        'previous_record',
        ]

        widgets = {
        'patient_id' : forms.TextInput(attrs={'placeholder' : 'Enter A unique Patient ID'} ),
        'dob' : CustomDateInput(),
        #'gender' : forms.ChoiceField(),
        'symptoms' : forms.Textarea(attrs={'placeholder' : 'Enter the Symptoms', 'rows':"4" , 'cols':"70"} ),
        'mob_no' : forms.TextInput(attrs={'placeholder' : 'Enter Mobile Number'} ),
        'weight' : forms.NumberInput(attrs={'placeholder' : 'Enter Weight'} ),
        'height' : forms.NumberInput(attrs={'placeholder' : 'Enter Height'} ),

        'allergies' : forms.Textarea(attrs={'placeholder' : "Enter the Patient's Allergies", 'rows':"4" , 'cols':"70" } ),
        'family_history' : forms.Textarea(attrs={'placeholder' : "Enter the Patient's Family History", 'rows':"4" , 'cols':"70"} ),
        'products_used' : forms.Textarea(attrs={'placeholder' : "Enter the Patient's Products Used if Any", 'rows':"4" , 'cols':"70"} ),
        'previous_record' : forms.Textarea(attrs={'placeholder' : "Enter the Patient's Previous Record if Any", 'rows':"4" , 'cols':"70"} ),
        }

class PatientReEditForm(forms.ModelForm):
    fname = forms.CharField(min_length=2,max_length=30, required=True, 
        widget=forms.TextInput(attrs={'placeholder' : 'Enter Your First Name' } ))
    lname = forms.CharField(min_length=2,max_length=30, required=False, 
        widget=forms.TextInput(attrs={'placeholder' : 'Enter Your Last Name' } ))
    email_id = forms.CharField(min_length=5, required=False,
                 widget=forms.EmailInput(attrs={'placeholder' : 'Enter Your Email ID', 'size':60 } ),)
    def __init__(self, *args, **kwargs):
        super(PatientReEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
    class Meta:
        model = Patient
        fields = [
            'patient_id',
            #'doctor',
            'fname',
            'lname',
            'email_id',
            'dob',
            'gender',
            'symptoms',
            'mob_no',
            'weight',
            'height',
            'img',

            'allergies',
            'family_history',
            'products_used',
            'previous_record',
            'img',
            'cropping',
        ]
        widgets = {
        'patient_id' : forms.TextInput(),

        'lname' : forms.TextInput(attrs = {'placeholder' : 'Re-Enter Last Name'}),
        'dob' : CustomDateInput(),
        #'gender' : forms.ChoiceField(),
        'symptoms' : forms.Textarea(attrs={'placeholder' : 'Re-Enter the Symptoms', 'rows':"4" , 'cols':"70"} ),
        'mob_no' : forms.TextInput(attrs={'placeholder' : 'Re-Enter Mobile Number'} ),
        'weight' : forms.NumberInput(attrs={'placeholder' : 'Re-Enter Weight'} ),
        'height' : forms.NumberInput(attrs={'placeholder' : 'Re-Enter Height'} ),

        'allergies' : forms.Textarea(attrs={'placeholder' : "Re-Enter the Patient's Allergies", 'rows':"4" , 'cols':"70" } ),
        'family_history' : forms.Textarea(attrs={'placeholder' : "Re-Enter the Patient's Family History", 'rows':"4" , 'cols':"70"} ),
        'products_used' : forms.Textarea(attrs={'placeholder' : "Re-Enter the Patient's Products Used if Any", 'rows':"4" , 'cols':"70"} ),
        'previous_record' : forms.Textarea(attrs={'placeholder' : "Re-Enter the Patient's Previous Record if Any", 'rows':"4" , 'cols':"70"} ),
        }

class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
    class Meta:
        model = Patient
        fields = [
            'feedback'
        ]
        widgets = {
            'feedback' : forms.Textarea(attrs={'placeholder' :'Please Enter some feedback. It will be Greatly Apperciated!',})
        }
        