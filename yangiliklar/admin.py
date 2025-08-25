from django.contrib import admin
from .models import Users_info,Tag,Category,New,News_Tag,Comments,Contact,Advertisement

# admin.site.register(Users_info)
# admin.site.register(Tag)
# admin.site.register(Category)
# admin.site.register(New)
# admin.site.register(News_Tag)
# admin.site.register(Comments)
# admin.site.register(Contact)






@admin.register(Users_info)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ["title","status"]

@admin.register(Advertisement)
class AdsAdmin(admin.ModelAdmin):
    list_display = ["title"]



