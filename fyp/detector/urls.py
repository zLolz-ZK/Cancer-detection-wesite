from django.urls import path,include 
from . import views

app_name = 'detector'
urlpatterns = [
    path('',views.home_view, name='home'),
    path('welcome/',views.welcome_view, name='welcome'),
    #path('about/',views.about, name='about'),
    #path('detection/',views.detection, name='detection'),
    path('registration/', views.registration, name="registration"),
    path('login/', views.login_view, name='login'),
    path('new_patient', views.new_patient, name='new_patient'),
    path('logout/', views.logout_view, name='logout'),
    #path('detect/', views.crop_view, name = 'detect'),

    path('result/<slug:slug>/', views.result, name='result'),
    path('details/<slug:slug>/', views.PatientView.as_view(), name='details'),

    path('patient_list/', views.OldPatientsList.as_view(), name = 'patient_list'),
    path('delete/<slug:slug>/', views.patientDeleteView, name = 'delete'),
    path('cancer_types/<str:name>/', views.cancerTypesView, name = 'cancer_types'),
    path('trial/',views.TrialView.as_view(), name = 'trial'),
    path('edit/<slug:slug>/', views.PatientUpdateView.as_view(), name = 'patient_edit'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)