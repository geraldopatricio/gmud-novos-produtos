from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .jobs.processar_arquivo_async import handle_uploaded_csv
from celery.result import AsyncResult
# Create your views here.
def home(request):
    if request.method == 'POST':
        form_details = UploadFileForm(request.POST, request.FILES)
        if form_details.is_valid():
            csv_file = request.FILES['file']
            try:               
                task = handle_uploaded_csv.delay(csv_file)
                messages.success(request, "Processamento Iniciado")
            except ValueError as e:
                messages.error(request, e)
            return render(request, 'home.html', context={'task_id': task.id})
        else:
            return render(request, 'home.html', {'form': form_details})
    return render(request, 'home.html')