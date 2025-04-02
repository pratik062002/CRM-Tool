from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Lead
from django.contrib.auth.hashers import make_password, check_password

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        if not all([full_name, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "You already have an account. Please login.")
            return redirect('login')
        else:
            # Save user
            user = User(
                full_name=full_name,
                email=email,
                password=make_password(password)
            )
            user.save()
            # Store user in session (consistent with login view)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.full_name
            messages.success(request, "Sign up successful!")
            return redirect('dashboard')
    
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validation
        if not all([email, password]):
            messages.error(request, "All fields are required.")
        else:
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    # Store user in session
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.full_name
                    messages.success(request, "Login successful!")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid email or password.")
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
    
    return render(request, 'login.html')

def logout(request):
    # Clear session
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('login')

def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to access the dashboard.")
        return redirect('login')
    user_name = request.session.get('user_name', 'User')
    return render(request, 'dashboard.html', {'user_name': user_name})

def new_lead(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to create a lead.")
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])
    lead_id = request.GET.get('lead_id')  # Check if we're editing a lead
    lead = None
    if lead_id:
        lead = get_object_or_404(Lead, id=lead_id, user=user)

    if request.method == 'POST':
        series = request.POST.get('series')
        job_title = request.POST.get('job_title')
        lead_owner = request.POST.get('lead_owner')
        salutation = request.POST.get('salutation')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        status = request.POST.get('status')

        # Validation
        if not all([series, job_title, lead_owner, salutation, first_name, last_name, gender, status]):
            messages.error(request, "All required fields must be filled.")
            return redirect('new_lead')

        # Validate salutation, gender, and status against model choices
        valid_salutations = [choice[0] for choice in Lead._meta.get_field('salutation').choices]
        valid_genders = [choice[0] for choice in Lead._meta.get_field('gender').choices]
        valid_statuses = [choice[0] for choice in Lead._meta.get_field('status').choices]

        if salutation not in valid_salutations:
            messages.error(request, "Invalid salutation selected.")
            return redirect('new_lead')
        if gender not in valid_genders:
            messages.error(request, "Invalid gender selected.")
            return redirect('new_lead')
        if status not in valid_statuses:
            messages.error(request, "Invalid status selected.")
            return redirect('new_lead')

        # Save or update the lead
        try:
            if lead:  # Update existing lead
                lead.series = series
                lead.job_title = job_title
                lead.lead_owner = lead_owner
                lead.salutation = salutation
                lead.first_name = first_name
                lead.middle_name = middle_name if middle_name else ''
                lead.last_name = last_name
                lead.gender = gender
                lead.status = status
                lead.save()
                messages.success(request, "Lead updated successfully!")
            else:  # Create new lead
                lead = Lead(
                    user=user,
                    series=series,
                    job_title=job_title,
                    lead_owner=lead_owner,
                    salutation=salutation,
                    first_name=first_name,
                    middle_name=middle_name if middle_name else '',
                    last_name=last_name,
                    gender=gender,
                    status=status,
                )
                lead.save()
                messages.success(request, "Lead created successfully!")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error saving lead: {str(e)}")
            return redirect('new_lead')
    
    return render(request, 'new_lead.html', {'lead': lead})

def previous_leads(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to view leads.")
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])
    leads = Lead.objects.filter(user=user)
    return render(request, 'previous_leads.html', {'leads': leads})

def landing(request):
    return render(request, 'landing.html')