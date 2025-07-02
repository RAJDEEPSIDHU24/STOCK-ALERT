from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
import os
import sys
import io
import json
from functools import wraps
# Firebase
import firebase_admin
from firebase_admin import credentials, auth, firestore
# Load .env 
from dotenv import load_dotenv
#  modules
from stocks import StockChangeRecognizer
from sendmail import SendEmail
# Load environment variables
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'super_secret_dev_key')
# Firebase Admin SDK init
FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
if not FIREBASE_SERVICE_ACCOUNT_PATH or not os.path.exists(FIREBASE_SERVICE_ACCOUNT_PATH):
    print("Error: FIREBASE_SERVICE_ACCOUNT_PATH not set or invalid.")
    sys.exit(1)
try:
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized.")
except Exception as e:
    print(f"❌ Firebase init error: {e}")
    sys.exit(1)
# Canvas vars
app_id = os.environ.get('__app_id', 'default-stock-app')
# Auth Decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
# Companies 
COMPANIES = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "WIPRO.NS", "ITC.NS",
    "HCLTECH.NS", "AXISBANK.NS", "KOTAKBANK.NS", "TATAMOTORS.NS", "MARUTI.NS"
]

COMPANY_NAMES = [
    "Reliance Industries", "TCS", "Infosys", "HDFC Bank", "ICICI Bank",
    "Hindustan Unilever", "SBI", "Bharti Airtel", "Wipro", "ITC",
    "HCL Technologies", "Axis Bank", "Kotak Mahindra Bank", "Tata Motors", "Maruti Suzuki"
]

# --- Routes ------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('register'))
        try:
            user = auth.create_user(email=email, password=password)
            db.collection(f'artifacts/{app_id}/users/{user.uid}/preferences').document('settings').set({
                'email_alerts_enabled': False,
                'alert_email': '',
                'email_password': '',
                'theme': 'dark'
            })
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error registering: {e}', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('login'))
        try:
            user = auth.get_user_by_email(email)
            session['user_id'] = user.uid
            session['user_email'] = user.email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Invalid credentials: {e}', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    user_email = session['user_email']
    user_settings = {}
    try:
        doc = db.collection(f'artifacts/{app_id}/users/{user_id}/preferences').document('settings').get()
        if doc.exists:
            user_settings = doc.to_dict()
    except Exception as e:
        flash('Could not load user settings.', 'danger')
        print(f"Settings error: {e}")
    from_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    to_date = datetime.today().strftime('%Y-%m-%d')

    #  logo URLs 
    company_logos = {
        symbol: url_for('static', filename=f'logos/{symbol}.png') for symbol in COMPANIES
    }
    return render_template('index.html',
                           companies=zip(COMPANIES, COMPANY_NAMES),
                           company_logos=company_logos,
                           from_date=from_date,
                           to_date=to_date,
                           user_settings=user_settings,
                           user_email=user_email)


@app.route('/analyze_stock', methods=['POST'])
@login_required
def analyze_stock():
    user_id = session['user_id']
    selected_symbol = request.form.get('stock_symbol')
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    try:
        index = COMPANIES.index(selected_symbol)
        stock_name = COMPANY_NAMES[index]
    except ValueError:
        return jsonify(message="❗ Invalid stock selected.", chart_data=None)
    try:
        recognizer = StockChangeRecognizer(stock_name, selected_symbol, from_date, to_date)
        recognizer.get_data_and_analyze()
        stock_message = recognizer.get_message()
        chart_data = recognizer.chart_data
        #  Email Alerts
        settings = {}
        try:
            doc = db.collection(f'artifacts/{app_id}/users/{user_id}/preferences').document('settings').get()
            if doc.exists:
                settings = doc.to_dict()
        except Exception as e:
            print(f"Email settings error: {e}")
        if settings.get('email_alerts_enabled') and recognizer.big_delta:
            try:
                alert_email = settings.get('alert_email', '')
                password = settings.get('email_password', '')
                SendEmail({selected_symbol: stock_message}).send_mails(alert_email, alert_email, password)
                stock_message += "\n📧 Email alert sent!"
            except Exception as e:
                stock_message += f"\n❌ Email error: {e}"
    except Exception as e:
        return jsonify(message=f"❌ Analysis failed: {e}", chart_data=None)
    return jsonify(message=stock_message, chart_data=chart_data, stock_name=stock_name, symbol=selected_symbol)


@app.route('/update_preferences', methods=['POST'])
@login_required
def update_preferences():
    user_id = session['user_id']
    theme = request.form.get('theme')
    email_alerts_enabled = request.form.get('email_alerts_enabled') == 'on'
    alert_email = request.form.get('alert_email')
    email_password = request.form.get('email_password')
    try:
        update_data = {
            'theme': theme,
            'email_alerts_enabled': email_alerts_enabled,
            'alert_email': alert_email,
        }
        if email_password:
            update_data['email_password'] = email_password
        db.collection(f'artifacts/{app_id}/users/{user_id}/preferences').document('settings').set(update_data, merge=True)
        flash('Preferences updated.', 'success')
    except Exception as e:
        flash(f"Update error: {e}", 'danger')
    return redirect(url_for('index'))


@app.route('/cli_run')
def cli_run():
    output = []
    output.append("📊 Top 15 Indian Companies")
    for i, name in enumerate(COMPANY_NAMES, 1):
        output.append(f"{i}. {name}")
    output.append("\n--- CLI Demo: Reliance Industries ---")
    symbol = COMPANIES[0]
    name = COMPANY_NAMES[0]
    from_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    to_date = datetime.today().strftime('%Y-%m-%d')
    try:
        recognizer = StockChangeRecognizer(name, symbol, from_date, to_date)
        recognizer.get_data_and_analyze()
        output.append(recognizer.get_message())
        output.append("\n✅ CLI demo complete.")
    except Exception as e:
        output.append(f"❌ CLI error: {e}")
    return render_template('cli_output.html', cli_output="\n".join(output))
if __name__ == '__main__':
    app.run(debug=True)

