from django.shortcuts import render, redirect, get_object_or_404
from medicSearch.models import Profile
from django.core.paginator import Paginator
from medicSearch.forms.UserProfileForm import UserProfileForm

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
    profileform = UserProfileForm(instance=profile)

    context = {
        'profileform': profileform,
    }

    return render(request, template_name='user/profile.html', context=context, status=200)
