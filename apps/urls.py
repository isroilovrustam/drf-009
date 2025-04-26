from django.urls import path, include

urlpatterns = [
    path("users/", include('user.urls')),
    # path("about/", include('about.urls')),
    path("contact/", include('contact.urls')),
    # path("blog/", include('blog.urls')),
]
