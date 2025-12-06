from django.http import HttpResponseForbidden
from beneficiary.models import Profile  

def role_required(required_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            try:
                if request.user.profile.role != required_role:
                    return HttpResponseForbidden("Not allowed")
            except Profile.DoesNotExist:
                return HttpResponseForbidden("Profile not found")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator