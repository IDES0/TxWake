from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BoatPull, Signup
from django.contrib import messages

def home(request):
    return render(request, 'txwake/home.html')

@login_required
def boat_pull_list(request):
    boat_pulls = BoatPull.objects.filter(is_active=True).order_by('date', 'time')
    pulls_with_members = []

    for pull in boat_pulls:
        members = Signup.objects.filter(boat_pull=pull).select_related('user')
        pulls_with_members.append({
            'boat_pull': pull,
            'members': members,
            'is_registered': Signup.objects.filter(boat_pull=pull, user=request.user).exists()
        })

    if request.method == 'POST':
        pull_id = request.POST.get('pull_id')
        boat_pull = get_object_or_404(BoatPull, id=pull_id)

        if Signup.objects.filter(user=request.user, boat_pull=boat_pull).exists():
            messages.error(request, 'You have already registered for this pull.')
            return redirect('boat_pull_list')

        if boat_pull.available_spots > 0:
            Signup.objects.create(user=request.user, boat_pull=boat_pull)
            boat_pull.available_spots -= 1
            boat_pull.save()
            messages.success(request, 'Successfully registered for the pull!')
            return redirect('boat_pull_list')
        else:
            messages.error(request, 'Sorry, this pull is already full.')

    return render(request, 'txwake/boat_pull_list.html', {'pulls_with_members': pulls_with_members})

@login_required
def boat_pull_signup(request, pull_id):
    boat_pull = get_object_or_404(BoatPull, id=pull_id)

    if Signup.objects.filter(user=request.user, boat_pull__date=boat_pull.date).count() >= 1:
        return render(request, 'txwake/boat_pull_signup.html', {
            'error': 'You have already signed up for a boat pull on this day.',
            'boat_pull': boat_pull
        })

    if boat_pull.available_spots <= 0:
        return render(request, 'txwake/boat_pull_signup.html', {
            'error': 'This boat pull is already full.',
            'boat_pull': boat_pull
        })

    if request.method == 'POST':
        Signup.objects.create(user=request.user, boat_pull=boat_pull)
        boat_pull.available_spots -= 1
        boat_pull.save()
        return redirect('boat_pull_list')
    
    return render(request, 'txwake/boat_pull_signup.html', {'boat_pull': boat_pull})