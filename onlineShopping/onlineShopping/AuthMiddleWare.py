from django.shortcuts import redirect


class AuthMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print("custom middleware before next middleware/view")
        # print(request.path)
        # print(request)
        if not request.user.is_authenticated and not (request.path == '/login/' or request.path == "/login/signup" or request.path == "/login/changePassword"):
            return redirect("authentication:login")
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # patch_cache_control(response=response, no_store=True)
        # Code to be executed for each response after the view is called
        # print("custom middleware after response or previous middleware")
        return response
