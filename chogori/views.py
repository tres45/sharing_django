from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from django.http import JsonResponse

from .models import Hike, Guide, Category
from .forms import ReviewForm


class CategoryRegion:
    """Categories and regions for hikes"""
    def get_categories(self):
        return Category.objects.all()

    def get_regions(self):
        return Hike.objects.filter(draft=False).values('region')


class HikesView(CategoryRegion, ListView):
    """List of hikes"""
    model = Hike
    queryset = Hike.objects.filter(draft=False)


class HikeDetailView(CategoryRegion, DetailView):
    """Full description for hike"""
    model = Hike
    queryset = Hike.objects.filter(draft=False)
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context


class AddReview(View):
    """Reviews for hike"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        hike = Hike.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.hike = hike
            form.save()
        return redirect(hike.get_absolute_url())


class GuideView(View):
    """Guide's information"""
    def get(self, request, slug):
        guide = Guide.objects.get(name=slug)
        return render(request, 'chogori/guide.html', {'guide': guide})


class FilterHikesView(CategoryRegion, ListView):
    """Filter for hikes"""
    def get_queryset(self):
        regions = self.request.GET.getlist('region')
        categories = self.request.GET.getlist('category')
        if len(regions) and len(categories):
            queryset = Hike.objects.filter(region__in=regions, category__in=categories)
        elif len(regions) or len(categories):
            queryset = Hike.objects.filter(Q(region__in=regions) | Q(category__in=categories))
        else:
            queryset = Hike.objects.all()

        if (len(queryset)):
            queryset = queryset.filter(draft=False)
        return queryset


class JsonFilterHikesView(CategoryRegion, ListView):
    """Filter for hikes in JSON format"""
    def get_queryset(self):
        regions = self.request.GET.getlist('region')
        categories = self.request.GET.getlist('category')
        if len(regions) and len(categories):
            queryset = Hike.objects.filter(region__in=regions, category__in=categories)
        elif len(regions) or len(categories):
            queryset = Hike.objects.filter(Q(region__in=regions) | Q(category__in=categories))
        else:
            queryset = Hike.objects.all()

        if (len(queryset)):
            queryset = queryset.filter(draft=False)
        return queryset.values('title', 'tagline', 'url', 'image')

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'hikes': queryset}, safe=False)


class Search(CategoryRegion, ListView):
    """Search for hikes"""
    def get_queryset(self):
        queryset = Hike.objects.filter(title__icontains=self.request.GET.get("search"), draft=False)
        return queryset.values('title', 'tagline', 'url', 'image')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search"] = f'search={self.request.GET.get("search")}&'
        return context


class JsonSearch(CategoryRegion, ListView):
    """Search for hikes"""
    def get_queryset(self):
        queryset = Hike.objects.filter(title__icontains=self.request.GET.get("search"), draft=False)
        return queryset.values('title', 'tagline', 'url', 'image')

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'hikes': queryset}, safe=False)
