from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from PIL import Image
import os
from numpy import asarray

from detector.models import Doctor, Patient, SomeImage
from .forms import DoctorSignUpForm, PatientReEditForm, PatientRegistrationForm, FeedbackForm
from . import skin_cancer_detector


def convert_to_int_list(raw_coordinates:tuple):#or list
    coordinates = [int(i) for i in raw_coordinates.split(',')]
    return coordinates


def home_view(request):
    if request.user.is_authenticated:
        print('User has logged in')

    return render(request, 'detector/index.html')

def welcome_view(request):
    if request.user.is_authenticated:
        print('User has logged in')

    return render(request, 'detector/welcome.html')

def registration(request):
    form = DoctorSignUpForm()
    if request.method == "POST":
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            
            form.save()
            messages.success(request,"success!")
            return redirect(reverse('detector:login'))
    return render(request, 'detector/registration.html', {'form': form})

def login_view(request):    
    if request.method=='POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect(reverse('detector:home'))
        else:
            messages.error(request,'Incorrect Username or password')
    return render(request,'detector/login.html',)

@login_required
def logout_view(request):
    doctor = get_object_or_404(Doctor, username = request.user.username) 
    if not doctor.is_valid:
        return render(request,'detector/NotValid.html')
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse("detector:home"))
    return render(request,'detector/home.html',{})

@login_required
def new_patient(request):
    doctor = get_object_or_404(Doctor, username = request.user.username) 
    if not doctor.is_valid:
        return render(request,'detector/NotValid.html')
    form = PatientRegistrationForm()
    if request.method == "POST":
        #patient_id = form.cleaned_data['patient_id']
        #image = get_object_or_404(Patient, patient_id=patient_id) if patient_id else None
        form = PatientRegistrationForm(request.POST, files=request.FILES, instance=None)
        print(form)

        if form.is_valid():
            print('reached')
            patient = form.save(commit=False)
            patient.doctor = doctor
            patient.save()
            new_patient = get_object_or_404(Patient, doctor = doctor, patient_id=patient.patient_id)
            new_patient.image = patient.img
            return HttpResponseRedirect(reverse('detector:welcome'))

    context = {
        'form' : form,
    }
    return render(request, 'detector/patientreg.html', context)


#rewrite this whole view
@login_required
def result(request,slug):
    doctor = get_object_or_404(Doctor, username = request.user.username) 
    patient = get_object_or_404(Patient, patient_id=slug, doctor = doctor)
    if not doctor.is_valid:
        return render(request,'detector/NotValid.html')
    form = FeedbackForm(instance=patient)
    print(patient.accuracy)
    coordinates = convert_to_int_list(patient.cropping)
    img = Image.open(patient.img)
    #img.show()
    #print(img.size)
    #url = patient.image.url
    #print(url)
    
    path = str(patient.img)[:-4] + '_cropped' + str(patient.img)[-4:]
    cropped_img = 'media/' + path
    print(cropped_img)
    img.crop(coordinates).save(cropped_img)
    patient.image = path
    print('..')
    result = skin_cancer_detector.prediction(cropped_img)
    #patient.image = result['vis_path'] not needed
    #result = 0 # skin_cancer_detector.prediction(cropped_img)
    print(result)
    patient.accuracy = result['acc']
    patient.result = result['class']

    #patient.result = result
        
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        print('reached')
        print(form)
        
        feedback = form.cleaned_data['feedback']
    
        patient.feedback = feedback 
        print('----------------------------------')
        #return HttpResponseRedirect(reverse('detector:result', kwargs={'slug': slug}))
        return HttpResponseRedirect(reverse('detector:welcome'))

    context = {
        'form' : form,
        'patient': patient,
    }
    return render(request,'detector/result2.html',context)



#@login_required
class OldPatientsList(ListView):
    model = Patient
    template_name = 'detector/patient_list.html' 
    context_object_name = 'patients'
    paginate_by = 10 
    def get_queryset(self):
        
        doctor = get_object_or_404(Doctor,email=self.request.user.email)
        
        obj = Patient.objects.filter(doctor=doctor)
        print("-----------------------")
        print(obj)
        return obj
    
    

#@login_required
class PatientView(DetailView):
    model = Patient
    context_object_name = 'patient'
    slug_field = 'patient_id'
    template_name = 'detector/patientprofile.html'

    def get_object(self, queryset=None):
        #print(self.kwargs)
        
        #    return HttpResponseRedirect(reverse("detector:patient_list"))
        return Patient.objects.get(patient_id=self.kwargs['slug'])


@login_required
def patientDeleteView(request,slug):
    doctor =  get_object_or_404(Doctor, email=request.user.email)
    patient = get_object_or_404(Patient, patient_id=slug, doctor=doctor)
    Patient.objects.get(patient_id=patient.patient_id, doctor=doctor).delete()
    return HttpResponseRedirect(reverse("detector:patient_list"))


def cancerTypesView(request, name):
    return render(request,f'detector/cancer_types/{name}.html')

class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientReEditForm
    template_name = 'detector/patientreg2.html'
    def get_object(self, queryset=None):
        return Patient.objects.get(patient_id=self.kwargs['slug'])
    def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          slug = self.kwargs['slug']
          return reverse_lazy('detector:details', kwargs={'slug':slug})
        
class TrialView(TemplateView):
    template_name = 'detector/patientreg2.html'