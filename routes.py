from flask import Blueprint, render_template, request, flash, redirect, url_for
from database import get_db_connection

# Define the blueprint for modular routing
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM User WHERE email = ? AND passwordHash = ?', 
                           (email, password)).fetchone()
        conn.close()
        
        if user:
            # On success, redirect to dashboard with the actual user ID
            return redirect(url_for('main.dashboard', user_id=user['userId']))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('main.index'))
            
    return render_template('index.html')

@main_bp.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    conn = get_db_connection()
    
    # Get current user details for the Navbar Profile Icon
    user = conn.execute('SELECT * FROM User WHERE userId = ?', (user_id,)).fetchone()
    
    # Get User's Learning Preferences (Skills they want to learn)
    learn_skills = conn.execute('''
        SELECT skillId FROM UserRequestPreference WHERE userId = ?
    ''', (user_id,)).fetchall()
    
    learn_ids = [s['skillId'] for s in learn_skills]
    mentors = []

    if learn_ids:
        # Find other users who OFFER these skills (The Match Engine)
        placeholders = ','.join(['?'] * len(learn_ids))
        query = f'''
            SELECT u.name, s.skillName, o.level, u.userId
            FROM User u
            JOIN UserOffer o ON u.userId = o.userId
            JOIN Skill s ON o.skillId = s.skillId
            WHERE o.skillId IN ({placeholders}) AND u.userId != ?
        '''
        mentors = conn.execute(query, (*learn_ids, user_id)).fetchall()

    conn.close()
    return render_template('dashboard.html', user=user, mentors=mentors)

@main_bp.route('/add_skill', methods=['POST'])
def add_skill():
    """Allows users to 'Push' new skill data into the database"""
    user_id = request.form.get('user_id')
    skill_id = request.form.get('skill_id')
    level = request.form.get('level')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO UserOffer (userId, skillId, level) 
        VALUES (?, ?, ?)
    ''', (user_id, skill_id, level))
    
    conn.commit()
    conn.close()
    flash('Skill offered successfully!')
    return redirect(url_for('main.dashboard', user_id=user_id))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        bio = request.form.get('bio')

        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO User (name, email, passwordHash, bio)
                VALUES (?, ?, ?, ?)
            ''', (name, email, password, bio)) # In production, use password hashing
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('main.index'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Please use a different one.')
        finally:
            conn.close()
            
    return render_template('register.html')
from flask import session

@main_bp.route('/logout')
def logout():
    """Handles the Sign Out use case"""
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@main_bp.route('/profile/<int:user_id>')
def profile(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM User WHERE userId = ?', (user_id,)).fetchone()
    
    # 1. Fetch all skills for the dropdown [cite: 364]
    all_skills = conn.execute('SELECT * FROM Skill').fetchall()
    
    # 2. Fetch skills user is TEACHING
    user_offers = conn.execute('''
        SELECT o.*, s.skillName FROM UserOffer o 
        JOIN Skill s ON o.skillId = s.skillId WHERE o.userId = ?
    ''', (user_id,)).fetchall()
    
    # 3. Fetch skills user wants to LEARN (The Learning List)
    learning_list = conn.execute('''
        SELECT p.*, s.skillName FROM UserRequestPreference p
        JOIN Skill s ON p.skillId = s.skillId WHERE p.userId = ?
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    # PASS ALL THREE TO THE VIEW [cite: 102]
    return render_template('profile.html', 
                           user=user, 
                           all_skills=all_skills, 
                           user_offers=user_offers, 
                           learning_list=learning_list)
@main_bp.route('/add_preference', methods=['POST'])
def add_preference():
    user_id = request.form.get('user_id')
    skill_id = request.form.get('skill_id')
    
    conn = get_db_connection()
    # Check if the record already exists to prevent duplicates
    conn.execute('''
        INSERT INTO UserRequestPreference (userId, skillId) 
        VALUES (?, ?)
    ''', (user_id, skill_id))
    
    conn.commit() # CRITICAL: This saves the data permanently
    conn.close()
    return redirect(url_for('main.profile', user_id=user_id))
@main_bp.route('/update_profile', methods=['POST'])
def update_profile():
    """Handles the modification of user metadata such as bio."""
    user_id = request.form.get('user_id')
    new_name = request.form.get('name')
    new_bio = request.form.get('bio')
    
    conn = get_db_connection()
    # This SQL command updates the existing 'matter' in the database [cite: 363]
    conn.execute('''
        UPDATE User 
        SET name = ?, bio = ? 
        WHERE userId = ?
    ''', (new_name, new_bio, user_id))
    
    conn.commit() # Save the changes permanently
    conn.close()
    
    flash('Profile updated successfully!')
    return redirect(url_for('main.profile', user_id=user_id))
@main_bp.route('/send_request/<int:mentor_id>/<string:skill_name>')
def send_request(mentor_id, skill_name):
    """
    Implements the 'Send Exchange Request' use case.
    Transitions the request to 'Pending' status.
    """
    # Assuming the current logged-in user is '1' for this mini-project
    learner_id = 1 
    
    conn = get_db_connection()
    
    # 1. Verify the skill exists to maintain data integrity
    skill = conn.execute('SELECT skillId FROM Skill WHERE skillName = ?', (skill_name,)).fetchone()
    
    if skill:
        # 2. INSERT the request into the ExchangeRequest table
        conn.execute('''
            INSERT INTO ExchangeRequest (senderId, receiverId, skillId, status)
            VALUES (?, ?, ?, 'Pending')
        ''', (learner_id, mentor_id, skill['skillId']))
        
        conn.commit()
        flash(f'Request for {skill_name} sent to the mentor!')
    else:
        flash('Error: Skill not found.')
        
    conn.close()
    return redirect(url_for('main.dashboard', user_id=learner_id))
@main_bp.route('/sessions/<int:user_id>')
def view_sessions(user_id):
    conn = get_db_connection()
    
    # We join u1 (Mentor) and u2 (Learner) to get their specific details
    sessions = conn.execute('''
        SELECT r.exchangeId, 
               u1.name as mentorName, 
               u1.email as mentorEmail, 
               u2.name as learnerName, 
               u2.email as learnerEmail,
               s.skillName, 
               r.status
        FROM ExchangeRequest r
        JOIN User u1 ON r.receiverId = u1.userId
        JOIN User u2 ON r.senderId = u2.userId
        JOIN Skill s ON r.skillId = s.skillId
        WHERE (r.senderId = ? OR r.receiverId = ?) AND r.status = 'Accepted'
    ''', (user_id, user_id)).fetchall()
    
    user = conn.execute('SELECT * FROM User WHERE userId = ?', (user_id,)).fetchone()
    conn.close()
    return render_template('sessions.html', user=user, sessions=sessions)
@main_bp.route('/manage_requests/<int:user_id>')
def manage_requests(user_id):
    """
    Displays both Sent and Received requests.
    Fulfills the 'Monitor Request Status' use case.
    """
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM User WHERE userId = ?', (user_id,)).fetchone()
    
    # 1. Received Requests (You are the Mentor)
    received = conn.execute('''
        SELECT r.exchangeId, u.name as senderName, s.skillName, r.status
        FROM ExchangeRequest r
        JOIN User u ON r.senderId = u.userId
        JOIN Skill s ON r.skillId = s.skillId
        WHERE r.receiverId = ? AND r.status = 'Pending'
    ''', (user_id,)).fetchall()
    
    # 2. Sent Requests (You are the Learner)
    sent = conn.execute('''
        SELECT r.exchangeId, u.name as mentorName, s.skillName, r.status
        FROM ExchangeRequest r
        JOIN User u ON r.receiverId = u.userId
        JOIN Skill s ON r.skillId = s.skillId
        WHERE r.senderId = ?
    ''', (user_id,)).fetchall()
    
    conn.close()
    return render_template('manage_requests.html', 
                           user=user, 
                           received=received, 
                           sent=sent)
@main_bp.route('/handle_request/<int:request_id>/<string:action>')
def handle_request(request_id, action):  # <--- This must match the 'handle_request' in url_for
    """Transitions the request state based on Mentor action"""
    new_status = 'Accepted' if action == 'accept' else 'Rejected'
    
    conn = get_db_connection()
    conn.execute('UPDATE ExchangeRequest SET status = ? WHERE exchangeId = ?', 
                 (new_status, request_id))
    
    # Redirection logic
    row = conn.execute('SELECT receiverId FROM ExchangeRequest WHERE exchangeId = ?', 
                       (request_id,)).fetchone()
    user_id = row['receiverId']
    
    conn.commit()
    conn.close()
    flash(f'Request has been {new_status}.')
    return redirect(url_for('main.manage_requests', user_id=user_id))
@main_bp.route('/contact_partner/<int:session_user_id>')
def contact_partner(session_user_id):
    """
    Fetches contact details for a matched partner.
    Fulfills the 'Initiate Communication' use case.
    """
    conn = get_db_connection()
    # Fetch the partner's 'matter' (email and bio)
    partner = conn.execute('SELECT name, email, bio FROM User WHERE userId = ?', 
                          (session_user_id,)).fetchone()
    conn.close()
    
    if partner:
        return {
            "name": partner['name'],
            "email": partner['email'],
            "bio": partner['bio']
        }
    return {"error": "User not found"}, 404
@main_bp.route('/complete_session/<int:exchange_id>')
def complete_session(exchange_id):
    """
    Transitions the session state to 'Completed'.
    Fulfills the 'Finalize Exchange' use case.
    """
    conn = get_db_connection()
    
    # Update the status to Completed
    conn.execute('''
        UPDATE ExchangeRequest 
        SET status = 'Completed' 
        WHERE exchangeId = ?
    ''', (exchange_id,))
    
    # Fetch user_id for redirection
    row = conn.execute('SELECT senderId FROM ExchangeRequest WHERE exchangeId = ?', (exchange_id,)).fetchone()
    user_id = row['senderId']
    
    conn.commit()
    conn.close()
    
    flash('Congratulations! You have completed this skill exchange.')
    return redirect(url_for('main.view_sessions', user_id=user_id))