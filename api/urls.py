from django.urls import path
from api.controllers.auth_controller import RegisterController, LoginController
from api.controllers.spam_controller import SpamController
from api.controllers.search_controller import SearchController
from api.controllers.detail_controller import ContactDetailController

urlpatterns = [
    path("register/", RegisterController.as_view(), name="register"),
    path("login/", LoginController.as_view(), name="login"), 
    path("spam/", SpamController.as_view(), name="spam_report"),
    path("search/", SearchController.as_view(), name="search"),
    path("contact/<int:contact_id>/", ContactDetailController.as_view(), name="person_detail"),

]
