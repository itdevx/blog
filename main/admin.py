from django.contrib import admin
from main.models import Post, Category, IPAdress, PostHit
from django.utils.html import format_html


# Actions
@admin.action(description='تنظیم وضعیت به حالت False')
def ChangeToFalse(Post,request,queryset):
    return queryset.update(status='F')

@admin.action(description='تنظیم وضعیت به حالت True')
def ChangeToTrue(Blog,request,queryset):
    return queryset.update(status='T')



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def image_format(self,obj):
        return format_html('<img width=50 src={}/>'.format(obj.intro_image.url))
    
    list_display = ['title','author','created','status','image_format']
    list_filter = ['title','author','status']
    list_search = ['title','description','author']
    prepopulated_fields = {
        'slug':('title',)
    }
    actions = [ChangeToFalse,ChangeToTrue]

    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'category_slug':('category_name',)
    }


admin.site.register(IPAdress)
admin.site.register(PostHit)
