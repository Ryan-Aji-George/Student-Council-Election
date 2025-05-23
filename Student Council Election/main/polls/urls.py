from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('select/', views.select, name='select'),
    path('select/all/', views.select_all, name='select_all'),
    path('<int:post_id>/', views.detail, name='detail'),
    #path('<int:post_id>/results', views.results, name='results'),
    path('<int:post_id>/vote', views.vote, name='vote'),
    path('vote_all/', views.vote_all, name='vote_all'),
    path('general_vote/', views.general_vote, name='general_vote'),
    path('success/', views.success, name='success'),
    path('al_success/', views.al_success, name='al_success'),
    path('al_success-2/', views.al_success2, name='al_success-2'),
    path('success/vote_all', views.success_vote_all, name='success_vote_all'),
    path('results/', views.results, name='results'),
    path('download_results/', views.download_results, name='download_results'),
    path('house/<str:house_name>/', views.house_vote, name='house_vote'),
    path('download_voters_page/', views.download_voters_page, name='download_voters_page'),

    path('download_results/excel/', views.download_results_excel, name='download_results_excel'),
]
