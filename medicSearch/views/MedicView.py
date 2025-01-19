from django.http import HttpResponse

def list_medics_view(request):
    return HttpResponse('Listagem de 1 ou mais médicos')