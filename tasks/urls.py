from django.conf.urls import url
from django.urls import path
from tasks import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('login/', views.login_view, name="login"),
    path('signin/', views.signin,name="signin"),
    path('register/', views.register, name="register"),
    path('logout/', views.signout, name="logout"),
    path('add_task/', views.addtask, name="add_task"),
    path('task_edit/<int:id>', views.task_edit,name="task_edit"),
    path('task_delete/<int:id>',views.task_delete,name="task_delete"),
    path('task_details/<int:id>', views.task_details, name="task_details"),
    path('model_form_upload/', views.model_form_upload, name='model_form_upload'),
    path('get_recordings/', views.get_recordings, name='get_recordings'),
    path('add_voice_note/<int:task_id>', views.add_voice_note, name="add_voice_note"),
    path('delete_voice_note/<int:note_id>', views.delete_voice_note, name="delete_voice_note"),
    path('task_voice_notes/<int:task_id>', views.task_voice_notes, name="task_voice_notes")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)