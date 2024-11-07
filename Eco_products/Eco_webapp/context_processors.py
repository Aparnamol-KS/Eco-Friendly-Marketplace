
from .models import UserProfile

def user_profile(request):
    user_profile_pic = None
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile  # Get the user's profile
            if user_profile.photo and hasattr(user_profile.photo, 'url'):
                user_profile_pic = user_profile.photo.url  # Only access .url if photo exists
        except UserProfile.DoesNotExist:
            pass  # Handle case where user has no profile

    return {'user_profile_pic': user_profile_pic}