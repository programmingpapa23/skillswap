from datetime import datetime

class User:
    """
    Represents the central User entity.
    This class serves as the base for both learners and mentors.
    """
    def __init__(self, user_id, name, email, bio=None, password_hash=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.bio = bio
        self.created_at = datetime.now()

class Skill:
    """
    Defines the available skills within the decentralized 'knowledge economy'.
    """
    def __init__(self, skill_id, skill_name, category, description=None):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.category = category
        self.description = description

class UserOffer:
    """
    Association entity representing skills a user is prepared to 'Teach'.
    """
    def __init__(self, offer_id, user_id, skill_id, level, available=1):
        self.offer_id = offer_id
        self.user_id = user_id
        self.skill_id = skill_id
        self.level = level # e.g., Beginner, Intermediate, Expert
        self.available = available # 1 for True, 0 for False

class UserRequestPreference:
    """
    Association entity representing skills a user wants to 'Learn'.
    """
    def __init__(self, request_pref_id, user_id, skill_id, level_needed):
        self.request_pref_id = request_pref_id
        self.user_id = user_id
        self.skill_id = skill_id
        self.level_needed = level_needed

class ExchangeRequest:
    """
    Tracks the lifecycle of a skill exchange as per the State Machine Diagram.
    """
    def __init__(self, exchange_id, sender_id, receiver_id, skill_id, message=None, status='Pending'):
        self.exchange_id = exchange_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.skill_id = skill_id
        self.message = message
        self.status = status # States: Pending, Accepted, Rejected, Cancelled, Completed
        self.created_at = datetime.now()

class Session:
    """
    Represents a scheduled learning interaction between a mentor and a learner.
    """
    def __init__(self, session_id, exchange_id, scheduled_date, scheduled_time, mode, location_link=None):
        self.session_id = session_id
        self.exchange_id = exchange_id
        self.scheduled_date = scheduled_date
        self.scheduled_time = scheduled_time
        self.mode = mode # e.g., Online, Offline
        self.location_link = location_link
        self.status = 'Scheduled'