from django.shortcuts import redirect

class SessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not hasattr(request.user, 'profile'):
            return redirect('login')
        return self.get_response(request)