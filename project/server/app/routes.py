from flask import render_template, jsonify, request, Blueprint, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from app.models import User, SystemStats
import platform

bp = Blueprint('main', __name__)

# API endpoint for clients to submit stats
@bp.route('/api/submit_stats', methods=['POST'])
def submit_stats():
    try:
        data = request.get_json()
        
        # Create new system stats record
        stats = SystemStats(
            client_id=data.get('client_id', 'unknown'),
            hostname=data.get('hostname', platform.node()),
            cpu=data.get('cpu'),
            ram=data.get('ram'),
            disk=data.get('disk'),
            processes=data.get('processes'),
            upload=data.get('upload'),
            download=data.get('download'),
            boot_time=data.get('boot_time'),
            num_cpu_physical_core=data.get('num_cpu_physical_core'),
            uptime=data.get('uptime'),
            cpu_info=data.get('cpu_info'),
            cpu_current_freq=data.get('cpu_current_freq'),
            total_RAM=data.get('total_RAM'),
            ava_RAM=data.get('ava_RAM'),
            packetloss=data.get('packetloss'),
            battery_percent=data.get('battery_percent'),
            plugged_state=data.get('plugged_state')
        )
        
        db.session.add(stats)
        db.session.commit()
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Admin dashboard
@bp.route('/')
@login_required
def dashboard():
    # Get latest stats from all clients
    subquery = db.session.query(
        SystemStats.client_id,
        db.func.max(SystemStats.timestamp).label('max_timestamp')
    ).group_by(SystemStats.client_id).subquery()
    
    latest_stats = SystemStats.query.join(
        subquery,
        db.and_(
            SystemStats.client_id == subquery.c.client_id,
            SystemStats.timestamp == subquery.c.max_timestamp
        )
    ).all()
    
    return render_template('dashboard.html', systems=latest_stats)

# Login page
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))