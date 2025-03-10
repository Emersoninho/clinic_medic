from django.shortcuts import render, redirect, get_object_or_404
from medicSearch.models import Profile
from django.core.paginator import Paginator
from medicSearch.forms.UserProfileForm import UserProfileForm, UserForm

def list_profile_view(request, id=None):
    profile = None
    if id is None:
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user).first()
        else:
            return redirect(to='/login/')
    else:
        profile = Profile.objects.filter(user__id=id).first()
    
    if not profile:
        return redirect(to='/')  # Ou mostre uma mensagem de erro personalizada
    
    favorites = profile.show_favorites() if profile else []

    paginator = Paginator(favorites, 8)
    page = request.GET.get('page')
    favorites = paginator.get_page(page)

    ratings = profile.show_ratings()
    if len(ratings) > 0:
        paginator = Paginator(ratings, 8)
        page = request.GET.get('page')
        ratings = paginator.get_page(page)

    context = {
        'profile': profile,
        'favorites': favorites,
        'ratings': ratings
    }

    return render(request, 'profile/profile.html', context, status=200)

def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    emailunused = True
    message = None

    if request.method == 'POST':
        profileform = UserProfileForm(request.POST, request.FILES, instance=profile)
        userform = UserForm(request.POST, instance=request.user)
        verifyemail = Profile.objects.filter(user__email=request.POST['email']).exclude(user__id=request.user.id).first()
        emailunused = verifyemail is None
    else:
        profileform = UserProfileForm(instance=profile)
        userform = UserForm(instance=request.user)

    if profileform.is_valid() and userform.is_valid() and emailunused:
        profileform.save()
        userform.save()
        message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}
    else:
        if request.method == 'POST':
            if emailunused:
                message = {'type': 'danger', 'text': 'Dados inválidos'}
            else:
                message = {'type': 'warning', 'text': 'E-mail já utilizado por outro usuário'}

    context = {
        'profileform': profileform,
        'userform': userform,
        'message': message,
    }

    return render(request, template_name='user/profile.html', context=context, status=200)
