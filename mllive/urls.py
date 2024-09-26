# urls.py
from django.conf.urls import handler400, handler404, handler500
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_model, name='upload_model'),
    path('add-input-field/', views.add_input_field, name='add_input_field'),
    path('models/', views.model_list, name='model_list'),
    path('predict/<int:model_id>/', views.predict, name='predict'),
    path('delete/<int:model_id>/', views.delete_model, name='delete_model'),
]


handler400 = 'mllive.views.bad_request'
handler404 = 'mllive.views.page_not_found'
handler500 = 'mllive.views.server_error'
