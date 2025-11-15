from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

class SystemStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(100), nullable=False)
    hostname = db.Column(db.String(100))
    cpu = db.Column(db.Float)
    ram = db.Column(db.Float)
    disk = db.Column(db.Float)
    processes = db.Column(db.Integer)
    upload = db.Column(db.Float)
    download = db.Column(db.Float)
    boot_time = db.Column(db.String(50))
    num_cpu_physical_core = db.Column(db.Integer)
    uptime = db.Column(db.String(50))
    cpu_info = db.Column(db.String(100))
    cpu_current_freq = db.Column(db.Float)
    total_RAM = db.Column(db.Float)
    ava_RAM = db.Column(db.Float)
    packetloss = db.Column(db.String(50))
    battery_percent = db.Column(db.Float)
    plugged_state = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))