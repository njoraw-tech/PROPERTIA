from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.http import JsonResponse



def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            # Capture the role from the form and save to profile
            user_role = form.cleaned_data.get('role')
            user.profile.role = user_role
            user.profile.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "redirect_url": "/accounts/login/"})
            else:
                return redirect('accounts:login')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Send back the form HTML with errors
                from django.template.loader import render_to_string
                form_html = render_to_string('accounts/register_form.html', {'form': form}, request=request)
                return JsonResponse({"success": False, "form_html": form_html}, status=400)
            
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_settings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('accounts:profile_settings')
    else:
        # Applying placeholders directly to the form instances if they aren't in forms.py
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form, 
        'p_form': p_form,
        'title': 'Account Settings'
    }
    return render(request, 'accounts/accounts_view.html', context)

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request) # Log out before deleting to clear session
        user.delete()
        messages.warning(request, 'Your account has been permanently deleted.')
        return redirect('accounts:login') # Redirect to login as profile no longer exists
    return render(request, 'accounts/delete_confirm.html')

def support_view(request):
    return render(request, 'accounts/support.html', {'title': 'Support'})

def password_change_done(request):
    return render(request, 'accounts/password_change_done.html', {'title': 'Password Changed'})