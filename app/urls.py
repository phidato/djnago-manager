from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from app import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^signup', views.SignupView.as_view(), name='signup'),
    
    url(r'^login/$', views.user_login, name='login'),
    url(r'^users/$', views.UserView.as_view(), name='allusers'),
    url(r'^users-delete/(?P<username>[\w|\W.-]+)/$', views.UserDelete, name='deleteusers'),

    url(r'^users-update/$', views.UserUpdate, name='updateusers'),

    url(r'^post-add/$', views.post_add, name='postadd'),
    url(r'^users-post/$', views.post_index, name='userspost'),
    url(r'^post-delete/$', views.user_post_delete_view, name='postdelete'),
    url(r'^post-update/$', views.post_save, name='postupdate'),

    url(r'^emp-add/$', views.emp_add, name='empadd'),
    url(r'^emp-data/$', views.emp_index, name='empdata'),
    url(r'^emp-delete/$', views.emp_delete, name='empdelete'),
    url(r'^emp-save/$', views.emp_save, name='empsave'),

    url(r'^projects/$', views.project_index, name='allprojects'),
    url(r'^add-project/$', views.project_add, name='projectadd'),
    url(r'^project-save/$', views.project_save, name='projectsave'),
    url(r'^project-delete/$', views.project_delete, name='projectdelete'),

    url(r'^departments/$', views.dept_index, name='alldepartments'),
    url(r'^add-department/$', views.dept_add, name='departmentadd'),
    url(r'^department-save/$', views.dept_save, name='deptsave'),
    url(r'^department-delete/$', views.dept_delete, name='deptdelete'),

    url(r'^designations/$', views.desg_index, name='alldesignations'),
    url(r'^add-designation/$', views.desg_add, name='designationadd'),
    url(r'^designation-save/$', views.desg_save, name='designationsave'),
    url(r'^designation-delete/$', views.desg_delete, name='desgdelete'),

    url(r'^save-user/', views.save_user, name='save-user'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^fb-data/$', views.fb_data, name='fbdata'),


)