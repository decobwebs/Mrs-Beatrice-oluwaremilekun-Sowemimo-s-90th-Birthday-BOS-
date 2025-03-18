from functools import wraps
from flask import flash, redirect, url_for, session

def login_required(f):
    """
    A decorator to ensure the user is logged in before accessing a route.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """
    A decorator to restrict access to routes based on user roles.
    Admins are allowed to bypass role restrictions.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('You must be logged in to access this page.', 'danger')
                return redirect(url_for('login'))

            user_role = session.get('role')
            if not user_role:
                flash('Your role could not be determined. Please log in again.', 'danger')
                return redirect(url_for('login'))

            if user_role != required_role and user_role != 'Admin':
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))

            return func(*args, **kwargs)
        return wrapper
    return decorator