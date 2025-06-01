from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import logging

logger = logging.getLogger(__name__)

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display a blank registration form.
        form = UserCreationForm()
        logger.debug("Displaying blank registration form")
    else:
        # Process the completed form.
        logger.debug(f"Processing registration form with data: {request.POST}")
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            logger.debug("Form is valid, creating user")
            new_user = form.save()
            logger.info(f"New user created: {new_user.username}")
            # Log the user in and then redirect to the home page.
            login(request, new_user)
            logger.debug(f"User {new_user.username} logged in successfully")
            return redirect('learning_logs:index')
        else:
            logger.error(f"Form validation failed: {form.errors}")

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)
