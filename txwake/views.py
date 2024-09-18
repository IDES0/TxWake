from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BoatPull, BoatPullSignup, EmailSubscription
from django.contrib import messages
from django.db import transaction
from django.db.models import F

def home(request):
    return render(request, 'txwake/home.html')

def email_subscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            EmailSubscription.objects.get_or_create(email=email)
            messages.success(request, 'Thank you for subscribing!')
        return redirect('home')
    return render(request, 'txwake/home.html')

@login_required
def boat_pull_list(request):
    # Get the active boat pulls ordered by date and time
    boat_pulls = BoatPull.objects.filter(is_active=True).order_by('date', 'time')
    pulls_with_members = []

    # Fetch members for each boat pull and check if the user is already registered
    for pull in boat_pulls:
        members = BoatPullSignup.objects.filter(boat_pull=pull).select_related('user')
        pulls_with_members.append({
            'boat_pull': pull,
            'members': members,
            'is_registered': BoatPullSignup.objects.filter(boat_pull=pull, user=request.user).exists()
        })

    if request.method == 'POST':
        pull_id = request.POST.get('pull_id')
        boat_pull = get_object_or_404(BoatPull, id=pull_id)
        action = request.POST.get('action')

        # Handle registration
        if action == 'register':
            # Check if the user is already registered for this pull
            if BoatPullSignup.objects.filter(user=request.user, boat_pull=boat_pull).exists():
                messages.error(request, 'You are already registered for this pull.')
                return redirect('boat_pull_list')

            # Atomic transaction to handle signup and spot decrement safely
            try:
                with transaction.atomic():
                    boat_pull = BoatPull.objects.select_for_update().get(id=pull_id)

                    # Check if there are available spots
                    if boat_pull.available_spots > 0:
                        # Decrease the available spots and save
                        boat_pull.available_spots = F('available_spots') - 1
                        boat_pull.save()

                        # Register the user for the pull
                        BoatPullSignup.objects.create(user=request.user, boat_pull=boat_pull)
                        messages.success(request, 'Successfully registered for the pull!')
                    else:
                        messages.error(request, 'Sorry, this pull is already full.')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again.')

        # Handle dropping from a pull
        elif action == 'drop':
            signup = BoatPullSignup.objects.filter(user=request.user, boat_pull=boat_pull)

            if signup.exists():
                try:
                    with transaction.atomic():
                        # Drop the user from the pull
                        signup.delete()

                        # Increase the available spots and save
                        boat_pull.available_spots = F('available_spots') + 1
                        boat_pull.save()

                        messages.success(request, 'Successfully dropped from the pull.')
                except Exception as e:
                    messages.error(request, 'An error occurred while dropping the pull. Please try again.')
            else:
                messages.error(request, 'You are not signed up for this pull.')

        return redirect('boat_pull_list')

    # Render the template with the list of boat pulls and members
    return render(request, 'txwake/boat_pull_list.html', {'pulls_with_members': pulls_with_members})