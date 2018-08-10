from basic_app import views
from django.conf.urls import url

app_name='basic_app'

urlpatterns=[
    url(r'^register/$',views.register,name="register"),
    url(r'^user_login/$',views.user_login,name="user_login"),
    url(r'^git_user_search/$',views.git_user_search,name="git_user_search"),
    url(r'^git_user_search/user_info$',views.git_user_search,name="user_info"),
    url(r'^git_user_search/search_again$',views.git_user_search,name="search_again_user")

]
