from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TodoForm
from .models import Todo, UserProfile

def index(request):
    return render(request, 'todo/index.html')

class Checklist(LoginRequiredMixin, View):

    def get(self, request):
        items = Todo.objects.filter(user=request.user)
        form = TodoForm()
        user_profile = UserProfile.objects.filter(user=request.user).first()
        total_spoons_required = sum(item.spoons_required for item in items)
        remaining_spoons = user_profile.max_spoons - total_spoons_required if user_profile else 0

        return render(request, "todo/checklist.html", {
            "items": items,
            "form": form,
            "remaining_spoons": remaining_spoons
        })

    def post(self, request):
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('checklist')
        else:
            items = Todo.objects.filter(user=request.user)
            user_profile = UserProfile.objects.filter(user=request.user).first()
            total_spoons_required = sum(item.spoons_required for item in items)
            remaining_spoons = user_profile.max_spoons - total_spoons_required if user_profile else 0

            return render(request, "todo/checklist.html", {
                "items": items,
                "form": form,
                "remaining_spoons": remaining_spoons
            })

def remove(request, item_id):
    item = Todo.objects.filter(id=item_id, user=request.user).first()
    if item:
        item.delete()
        messages.info(request, "Item removed!")
    else:
        messages.error(request, "Item not found or you don't have permission to remove it.")
    return redirect('checklist')
