from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, Resume

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']

        if not username or not email or not password:
            flash('All fields are required.')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken. Please choose another.')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.')
            return redirect(url_for('register'))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Invalid username or password.')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    resumes = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.upload_date.desc()).all()
    return render_template('dashboard.html', resumes=resumes)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'resume' not in request.files or request.files['resume'].filename == '':
            flash('Please select a PDF file to upload.')
            return redirect(url_for('upload'))

        file = request.files['resume']

        if not file.filename.lower().endswith('.pdf'):
            flash('Only PDF files are supported.')
            return redirect(url_for('upload'))

        original_filename = file.filename
        safe_name = secure_filename(file.filename)
        base, ext = os.path.splitext(safe_name)
        unique_name = f"{base}_{current_user.id}_{int(__import__('time').time())}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(filepath)

        from resume_parser import extract_text
        from ai_analyzer import analyze_resume

        text = extract_text(filepath)
        result = analyze_resume(text)

        resume = Resume(
            user_id=current_user.id,
            original_filename=original_filename,
            file_path=filepath,
            resume_text=text,
            analysis_result=result['report'],
            score=result['score']
        )
        db.session.add(resume)
        db.session.commit()

        return redirect(url_for('view_resume', resume_id=resume.id))

    return render_template('upload.html')


@app.route('/resume/<int:resume_id>')
@login_required
def view_resume(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    return render_template('analysis.html', resume=resume)


@app.route('/resume/<int:resume_id>/download')
@login_required
def download_resume(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    if not os.path.exists(resume.file_path):
        flash('File not found on disk.')
        return redirect(url_for('dashboard'))
    return send_file(resume.file_path, as_attachment=True, download_name=resume.original_filename)


@app.route('/resume/<int:resume_id>/delete', methods=['POST'])
@login_required
def delete_resume(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    db.session.delete(resume)
    db.session.commit()
    flash('Resume deleted successfully.')
    return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
