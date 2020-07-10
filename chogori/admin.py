from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Guide, Hike, HikePhotos, Reviews


class HikeAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Hike
        fields = '__all__'


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 0
    readonly_fields = ("name", "email")


class HikeShotsInline(admin.TabularInline):
    model = HikePhotos
    extra = 0
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100"')

    get_image.short_description = "Фотография"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    list_display_links = ("name",)


@admin.register(Hike)
class HikeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_date", "duration", "url", "draft")
    list_filter = ("category", "duration")
    search_fields = ("title",)
    inlines = [HikeShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = HikeAdminForm
    actions = ["publish", "unpublish"]
    readonly_fields = ("get_image",)
    fieldsets = (
        ("Поход", {
            "fields": ("title", "tagline", ("price", "category"))
        }),
        ("Локация", {
            "fields": (("country", "region"),)
        }),
        ("Детали", {
            "fields": ("description", ("image", "get_image"))
        }),
        ("Организаторы", {
            "fields": (("manager", "guide"),)
        }),
        ("Даты", {
            "fields": (("start_date", "finish_date", "duration"),)
        }),
        ("Опции", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="150"')

    get_image.short_description = "Фотография"

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "hike", "id")
    readonly_fields = ("name", "email")
    list_filter = ("hike",)


@admin.register(HikePhotos)
class HikePhotosAdmin(admin.ModelAdmin):
    list_display = ("title", "hike", "get_image")
    readonly_fields = ("get_image",)
    list_filter = ("hike",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100">')

    get_image.short_description = "Фотография"


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("name", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100">')

    get_image.short_description = "Фотография"


admin.site.site_title = "Турклуб Чогори"
admin.site.site_header = "Турклуб Чогори"
