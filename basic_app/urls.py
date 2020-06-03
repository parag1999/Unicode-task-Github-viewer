from basic_app import views
from django.conf.urls import url
from django.urls import path

app_name='basic_app'

urlpatterns=[
    path('register/',views.register,name="register"),
    path('user_login/',views.user_login,name="user_login"),
    path('git_user_search/',views.git_user_search,name="git_user_search"),
    path('about_me/',views.contact_msg_store,name="about_me"),
    path('git_user_search/<str:user>/',views.git_user_info,name="user_profile"),
    path('git_user_search/<str:user>/<str:repo_name>/',views.commit_info,name="commit_history"),
    path('git_user_search/search_again',views.git_user_search,name="search_again_user")

]
