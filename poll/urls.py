from django.urls import path
from . import views
urlpatterns = [
     path('', views.HomepageView.as_view(), name="homepage"),
     path('results/lga', views.ResultLGAView.as_view(), name="lga-results"),
     path('create', views.PollingUnitView.as_view(), name="create-polling-unit"),
]
