from django.http import HttpResponse
from medicSearch.models import Profile

def list_medics_view(request):
    name = request.GET.get('name')
    speciality = request.GET.get('speciality')
    neighborhood = request.GET.get('neighborhood')
    city = request.GET.get('city')
    state = request.GET.get('state')
    medics = Profile.objects.filter(role=2)

    if name is not None and name != '':
        medics = medics.filter(user__first_name=name)
    print(medics.all())
    
    return HttpResponse('Listagem de 1 ou mais médicos')