from django.urls import path

from . import views


urlpatterns = [
    path('', views.HikesView.as_view()),
    path('filter/', views.FilterHikesView.as_view(), name='filter'),
    path('json-filter/', views.JsonFilterHikesView.as_view(), name='json_filter'),
    path('search/', views.Search.as_view(), name='search'),
    path('json-search/', views.JsonSearch.as_view(), name='search_filter'),
    path('<slug:slug>/', views.HikeDetailView.as_view(), name='hike_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('guide/<str:slug>/', views.GuideView.as_view(), name='guide_detail')
]
