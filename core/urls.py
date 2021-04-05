from django.urls import path, include

from .views import get_records, download_csv

app_name = "core"

urlpatterns = [
	path('get-records/', get_records, name="get_records"),
	path('download-csv/', download_csv, name="download_csv"),
    
]