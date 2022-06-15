from django.http import Http404
from main.models import Post
from account.models import User
from django.shortcuts import get_object_or_404



class FormValidMixins():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = False
        return super().form_valid(form)



class FieldsMixins():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = '__all__'
        else:
            self.fields = [
                'title',
                'slug',
                'description',
                'intro_image',
                'categories',
                'tags'
            ]
        # else:
            # raise Http404('شما نمیتوانید این صفحه را مشاهده کنید')
        return super().dispatch(request, *args, **kwargs)
        


class SuperuserAccessMixins():
    def dispatch(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('صفحه مورد نظر یافت نشد')



class SuperuserAccessDeleteUserMixins():
    def dispatch(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('صفحه مورد نظر یافت نشد')



class SuperAccessUpdateUsers():
    def dispatch(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('صفحه مورد نظر یافت نشد')
