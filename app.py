from flask import Flask, render_template, request, redirect, url_for, flash, session, Response, send_from_directory, send_file, make_response
from extensions import db
from flask_migrate import Migrate
from flask_login import LoginManager
import io
import csv
import matplotlib
matplotlib.use('Agg')
from datetime import datetime, timedelta
from decorators import login_required, role_required
from generate_report import generate_guest_statistics, generate_pdf_report
import logging
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
import os
from datetime import datetime
# Load environment variables from .env
load_dotenv()




# Initialize Flask app
app = Flask(__name__)

# Configuration for PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_DELETE_PASSWORD = os.getenv('SECRET_DELETE_PASSWORD')

# Initialize the SQLAlchemy instance with the Flask app
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# Define the Guest model
from models import Guest, GuestType, User

# Create database tables explicitly using app context
with app.app_context():
    db.create_all()

def generate_csv(guests, filename):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Email', 'Phone', 'Timestamp'])  # Header row

    for guest in guests:
        writer.writerow([guest.name, guest.email, guest.phone, guest.timestamp.strftime('%Y-%m-%d')])

    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/rsvp/static/<path:filename>')
def rsvp_static(filename):
    return send_from_directory('static', filename)

# Default static route (optional fallback)
@app.route('/static/<path:filename>')
def default_static(filename):
    return send_from_directory('static', filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    """
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # Validate input
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('login'))

        # Find the user by username
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

        # Log the user in
        session['user_id'] = user.id
        session['role'] = user.role
        flash('You have been logged in successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route to display the Regular Guest RSVP form
@app.route('/')
def index():
    return render_template('index.html')

# Route to display the VIP Guest RSVP form
@app.route('/vip')
def vip():
    return render_template('vip.html')

# Route to handle regular guest form submissions
@app.route('/register/regular', methods=['POST'])
def register_regular():
    return register_guest('regular')

# Route to handle VIP guest form submissions
@app.route('/vip_register', methods=['POST'])
def vip_register():
    return register_guest('vip')

# Helper function to handle guest registration
def register_guest(guest_type):
    # Extract form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # Validate data (basic validation)
    if not name or not email or not phone:
        flash('Invalid form data. Please try again.', 'danger')
        return redirect(url_for('index') if guest_type == 'regular' else url_for('vip'))

    # Check if the email already exists in the database
    existing_guest = Guest.query.filter_by(email=email).first()
    if existing_guest:
        flash('This email has already been used. Please use a different email.', 'danger')
        return redirect(url_for('index') if guest_type == 'regular' else url_for('vip'))

    # Create a new Guest object
    new_guest = Guest(name=name, email=email, phone=phone, guest_type=guest_type)

    try:
        # Add the guest to the database
        db.session.add(new_guest)
        db.session.commit()
        flash('Thank you for your RSVP', 'success')
    except Exception as e:
        # Handle any unexpected errors
        db.session.rollback()
        flash('An error occurred while processing your RSVP. Please try again later.', 'danger')
        app.logger.error(f"Error during guest registration: {str(e)}")  # Log the error for debugging

    return redirect(url_for('index') if guest_type == 'regular' else url_for('vip'))


# Admin Route: Create Moderator
@app.route('/create_moderator', methods=['GET', 'POST'])
@login_required
@role_required('Admin')  # Only Admins can create moderators
def create_moderator():
    """
    Allow Admins to create new moderators.
    """
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # Validate input
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('create_moderator'))
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('create_moderator'))

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('create_moderator'))

        try:
            # Create the moderator
            moderator = User(username=username, role='Moderator')  # No email required
            moderator.set_password(password)
            db.session.add(moderator)
            db.session.commit()

            flash('Moderator created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the moderator. Please try again.', 'danger')
            app.logger.error(f"Error creating moderator: {e}")

    return render_template('create_moderator.html')

# Route to export RSVP data to CSV (Restricted to Admins)
@app.route('/export/<type_name>')
@login_required
def export_guest_list(type_name):
    """
    Export the guest list for a specific guest type as a CSV file.
    """
    logging.info(f"Exporting guest list for type: {type_name}")

    # Find the guest type by name (case-insensitive)
    guest_type = GuestType.query.filter(
        db.func.lower(GuestType.name) == type_name.lower()
    ).first()

    if not guest_type:
        logging.warning(f"Guest type '{type_name}' does not exist.")
        flash(f'Guest type "{type_name}" does not exist.', 'danger')
        return redirect(url_for('dashboard'))

    logging.info(f"Found guest type: {guest_type.name} (ID: {guest_type.id})")

    # Fetch all guests associated with this guest type
    guests_list = Guest.query.filter_by(guest_type_id=guest_type.id).all()

    if not guests_list:
        logging.warning(f"No guests found for type '{type_name}'.")
        flash(f'No guests found for type "{type_name}".', 'warning')
        return redirect(url_for('dashboard'))

    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the header row
    writer.writerow(['Name', 'Email', 'Phone', 'Registered On'])

    # Write the guest data rows
    for guest in guests_list:
        writer.writerow([
            guest.name,
            guest.email,
            guest.phone,
            guest.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])

    # Prepare the response
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={guest_type.name}_guest_list.csv"
    response.headers["Content-Type"] = "text/csv"

    return response

@app.route('/guests/<type_name>')
@login_required
def view_guests_by_type(type_name):
    """
    Fetch and display the list of guests for a specific guest type.
    Handles case-insensitive matching for guest types.
    """
    logging.info(f"Fetching guest list for type: {type_name}")

    # Find the guest type by name (case-insensitive)
    guest_type = GuestType.query.filter(
        db.func.lower(GuestType.name) == type_name.lower()
    ).first()

    if not guest_type:
        logging.warning(f"Guest type '{type_name}' does not exist.")
        flash(f'Guest type "{type_name}" does not exist.', 'danger')
        return redirect(url_for('dashboard'))

    logging.info(f"Found guest type: {guest_type.name} (ID: {guest_type.id})")

    # Fetch all guests associated with this guest type
    guests_list = Guest.query.filter_by(guest_type_id=guest_type.id).all()

    if not guests_list:
        logging.warning(f"No guests found for type '{type_name}'.")
        flash(f'No guests found for type "{type_name}".', 'warning')

    # Render the guest list template
    return render_template(
        'guest_list.html',
        guests=guests_list,
        guest_type=guest_type.name
    )

# Route to view the list of regular guests (Restricted to logged-in users)
@app.route('/guests/regular')
@login_required  # Requires login, but no role restriction (Admin/Moderator can access)
def regular_guests():
    regular_guests_list = Guest.query.filter_by(guest_type='regular').all()
    return render_template('guest_list.html', guests=regular_guests_list, guest_type='Regular')

# Route to view the list of VIP guests (Restricted to logged-in users)
@app.route('/guests/vip')
@login_required  # Requires login, but no role restriction (Admin/Moderator can access)
def vip_guests():
    vip_guests_list = Guest.query.filter_by(guest_type='vip').all()
    return render_template('guest_list.html', guests=vip_guests_list, guest_type='VIP')

# Route to export regular guest list as CSV (Restricted to Admins)
@app.route('/export/regular')
@login_required
@role_required('Admin')  # Only Admins can export
def export_regular():
    regular_guests_list = Guest.query.filter_by(guest_type='regular').all()
    return generate_csv(regular_guests_list, 'regular_guests.csv')

# Route to export VIP guest list as CSV (Restricted to Admins)
@app.route('/export/vip')
@login_required
@role_required('Admin')  # Only Admins can export
def export_vip():
    vip_guests_list = Guest.query.filter_by(guest_type='vip').all()
    return generate_csv(vip_guests_list, 'vip_guests.csv')

# Route to search for guests (Restricted to logged-in users)
@app.route('/search_guests', methods=['GET'])
@login_required
def search_guests():
    query = request.args.get('query', '').strip()
    if not query:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('dashboard'))

    # Search by name or email
    guests = Guest.query.filter(
        (Guest.name.ilike(f'%{query}%')) | (Guest.email.ilike(f'%{query}%'))
    ).all()

    if not guests:
        flash(f'No results found for "{query}".', 'warning')

    # Pass the results to the guest list template
    guest_types = GuestType.query.all()  # Pass all guest types for tagging
    return render_template('guest_list.html', guests=guests, guest_type=f'Search Results for "{query}"', guest_types=guest_types)




@app.route('/guests/<type_name>')
@login_required
def guest_list(type_name):
    """
    Fetch and display the list of guests for a specific guest type.
    Handles case-insensitive matching for guest types.
    """
    logging.info(f"Fetching guest list for type: {type_name}")

    # Find the guest type by name (case-insensitive)
    guest_type = GuestType.query.filter(
        db.func.lower(GuestType.name) == type_name.lower()
    ).first()

    if not guest_type:
        logging.warning(f"Guest type '{type_name}' does not exist.")
        flash(f'Guest type "{type_name}" does not exist.', 'danger')
        return redirect(url_for('dashboard'))

    logging.info(f"Found guest type: {guest_type.name} (ID: {guest_type.id})")

    # Fetch all guests associated with this guest type
    guests_list = Guest.query.filter_by(guest_type_id=guest_type.id).all()

    if not guests_list:
        logging.warning(f"No guests found for type '{type_name}'.")
        flash(f'No guests found for type "{type_name}".', 'warning')

    # Render the guest list template
    return render_template(
        'guest_list.html',
        guests=guests_list,
        guest_type=guest_type.name
    )





@app.route('/dashboard')
@login_required  # Requires login
def dashboard():
    now = datetime.utcnow()

    # Fetch all guest types
    guest_types = GuestType.query.all()
    stats = {}
    for gt in guest_types:
        stats[gt.name] = gt.guests.count()  # Count guests for each type

    # Guests registered today
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    guests_today = Guest.query.filter(Guest.timestamp >= start_of_day).count()

    # Guests registered this week
    start_of_week = now - timedelta(days=now.weekday())  # Start of the week (Monday)
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    guests_this_week = Guest.query.filter(Guest.timestamp >= start_of_week).count()

    # Guests registered this month
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    guests_this_month = Guest.query.filter(Guest.timestamp >= start_of_month).count()

    # Registration trends (last 7 days)
    registration_trends = []
    labels = []
    for i in range(7):  # Last 7 days
        day = now - timedelta(days=i)
        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        count = Guest.query.filter(Guest.timestamp.between(start_of_day, end_of_day)).count()
        registration_trends.append(count)
        labels.append(day.strftime('%Y-%m-%d'))
    registration_trends.reverse()
    labels.reverse()

    # Guest type counts for the chart
    guest_type_counts = [stats[gt.name] for gt in guest_types]

    # Predefined color palette
    COLOR_PALETTE = [
        "#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33F3",
        "#33FFF6", "#FF8C33", "#33FF8C", "#8C33FF", "#FF3333"
    ]

    # Assign colors to guest types
    guest_type_colors = [COLOR_PALETTE[i % len(COLOR_PALETTE)] for i in range(len(guest_types))]

    # Convert guest type names into a list for JSON serialization
    guest_type_labels = [gt.name for gt in guest_types]

    return render_template(
        'dashboard.html',
        guest_types=guest_types,
        stats=stats,
        guests_today=guests_today,
        guests_this_week=guests_this_week,
        guests_this_month=guests_this_month,
        registration_trends=registration_trends,
        registration_labels=labels,
        guest_type_counts=guest_type_counts,  # Pass guest type counts to the template
        guest_type_colors=guest_type_colors,  # Pass guest type colors to the template
        guest_type_labels=guest_type_labels,  # Pass guest type labels to the template
        role=session['role']
    )

@app.route('/tag_guest/<int:guest_id>', methods=['POST'])
@login_required
@role_required('Moderator')
def tag_guest(guest_id):
    guest = Guest.query.get_or_404(guest_id)
    new_type_name = request.form.get('new_type').strip().capitalize()

    # Find the target guest type
    new_type = GuestType.query.filter_by(name=new_type_name).first()
    if not new_type:
        flash(f'Guest type "{new_type_name}" does not exist.', 'danger')
        return redirect(url_for('guest_list', type_name=guest.type.name))

    # Update the guest's type
    guest.guest_type_id = new_type.id
    db.session.commit()
    flash(f'{guest.name} has been tagged as {new_type.name}.', 'success')
    return redirect(url_for('guest_list', type_name=new_type.name))


@app.route('/generate_report')
@login_required
@role_required('Admin')  # Only Admins can generate reports
def generate_report():
    statistics = generate_guest_statistics()
    pdf_buffer = generate_pdf_report(statistics)
    return Response(
        pdf_buffer,
        mimetype='application/pdf',
        headers={"Content-Disposition": "attachment;filename=guest_statistics_report.pdf"}
    )


@app.route('/create_guest_type', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def create_guest_type():
    if request.method == 'POST':
        type_name = request.form.get('type_name').strip().capitalize()
        if not type_name:
            flash('Guest type name is required.', 'danger')
            return redirect(url_for('create_guest_type'))

        # Check if the type already exists
        existing_type = GuestType.query.filter_by(name=type_name).first()
        if existing_type:
            flash(f'Guest type "{type_name}" already exists.', 'warning')
            return redirect(url_for('create_guest_type'))

        # Create the new type
        new_type = GuestType(name=type_name)
        db.session.add(new_type)
        db.session.commit()
        flash(f'New guest type "{type_name}" created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_guest_type.html')

@app.route('/delete_guest_type/<int:type_id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_guest_type(type_id):
    guest_type = GuestType.query.get_or_404(type_id)
    db.session.delete(guest_type)
    db.session.commit()
    flash(f'Guest type "{guest_type.name}" deleted.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/rsvp/<type_name>', methods=['GET'])
def rsvp_form(type_name):
    guest_type = GuestType.query.filter_by(name=type_name).first_or_404()
    return render_template('index.html', guest_type=guest_type)


@app.route('/register/<type_name>', methods=['POST'])
def register_guest(type_name):
    guest_type = GuestType.query.filter_by(name=type_name).first_or_404()

    # Extract form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # Validate data
    if not name or not email or not phone:
        flash('All fields are required.', 'danger')
        return redirect(url_for('rsvp_form', type_name=type_name))

    # Check if email already exists
    existing_guest = Guest.query.filter_by(email=email).first()
    if existing_guest:
        flash('This email has already been used. Please use a different email.', 'danger')
        return redirect(url_for('rsvp_form', type_name=type_name))

    # Create guest
    new_guest = Guest(
        name=name,
        email=email,
        phone=phone,
        guest_type_id=guest_type.id  # Link to the appropriate guest type
    )
    db.session.add(new_guest)
    db.session.commit()
    flash('Thank you for your RSVP!', 'success')
    return redirect(url_for('rsvp_form', type_name=type_name))


@app.route('/clear_all_guests', methods=['POST'])
@login_required
def clear_all_guests():
    """
    Clear all guest types and their associated guests.
    This action requires a secret password for authorization.
    """
    if session['role'] != 'Admin':
        flash("You do not have permission to perform this action.", "danger")
        return redirect(url_for('dashboard'))

    # Retrieve the submitted password from the form
    submitted_password = request.form.get('delete_password')

    # Load the hashed password from the environment variable
    hashed_password = os.getenv('SECRET_DELETE_PASSWORD_HASH')

    # Verify the password using check_password_hash
    if not check_password_hash(hashed_password, submitted_password):
        flash("Incorrect password. Deletion aborted.", "danger")
        return redirect(url_for('dashboard'))

    # Delete all guests
    Guest.query.delete()

    # Delete all guest types
    GuestType.query.delete()

    # Commit changes to the database
    db.session.commit()

    logging.info("All guest types and guests have been deleted.")
    flash("All guest types and guests have been successfully deleted.", "success")

    return redirect(url_for('dashboard'))


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
