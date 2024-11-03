
from .models import UserProfile

def user_profile(request):
    user_profile_pic = None
    if request.user.is_authenticated:
        try:
            user_profile_pic = request.user.userprofile.photo.url
        except UserProfile.DoesNotExist:
            pass  # Handle case where user has no profile
    return {'user_profile_pic': user_profile_pic}
