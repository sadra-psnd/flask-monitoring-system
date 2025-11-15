from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

def setup_admin():
    with app.app_context():
        # Create admin user if doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin', 
                password_hash=generate_password_hash('admin123', method='pbkdf2:sha256')
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin/admin123")

if __name__ == '__main__':
    setup_admin()
    app.run(host='0.0.0.0', port=5000, debug=True)