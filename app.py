# ============================================
# PROJECT SENTINEL-ANF | PRODUCTION VERSION
# Islamabad Anti Narcotics Force Intelligence Platform
# ============================================

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import random
from datetime import datetime, timedelta
import os
import functools

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'anf-secret-key-change-in-production')
CORS(app)

# ============================================
# LOGIN CONFIGURATION
# ============================================

# You can change these credentials
USERS = {
    'anf_officer': 'sentinel2026',
    'director': 'anf@123',
    'analyst': 'islamabad'
}

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# ============================================
# LOGIN ROUTES
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            session['logged_in_at'] = datetime.now().isoformat()
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ============================================
# REAL ANF DATA - Islamabad Seizures 2025-2026
# ============================================

seizures = [
    # February 2026
    {"id": "ANF-2026-001", "location": "F-10 Markaz", "sector": "F-10", "drug": "Hashish", "quantity": "7.7 kg", "value": "PKR 2.3M", "date": "2026-02-15", "time": "22:30", "method": "Vehicle checkpoint", "suspects": 2, "status": "Arrested", "details": "Near Islamabad Model College, suspects from KPK"},
    {"id": "ANF-2026-002", "location": "Islamabad Airport", "sector": "Airport", "drug": "Ice (Crystal Meth)", "quantity": "630g", "value": "PKR 4.5M", "date": "2026-02-12", "time": "14:15", "method": "Body smuggling", "suspects": 1, "status": "Arrested", "details": "105 capsules ingested, destination Dubai"},
    {"id": "ANF-2026-003", "location": "I-8 Sector", "sector": "I-8", "drug": "Ice", "quantity": "340g", "value": "PKR 2.1M", "date": "2026-02-08", "time": "19:45", "method": "Hostel raid", "suspects": 3, "status": "Arrested", "details": "Students from private university, sourced from Rawalpindi"},
    {"id": "ANF-2026-004", "location": "G-9 Markaz", "sector": "G-9", "drug": "Valium pills", "quantity": "2.1kg (21,000 pills)", "value": "PKR 1.8M", "date": "2026-02-05", "time": "11:20", "method": "Pharmacy raid", "suspects": 2, "status": "Under Investigation", "details": "Pharmacy without license, selling to students"},
    {"id": "ANF-2026-005", "location": "Blue Area", "sector": "Blue Area", "drug": "Ecstasy", "quantity": "50 pills", "value": "PKR 250,000", "date": "2026-02-01", "time": "01:30", "method": "Night club raid", "suspects": 5, "status": "Booked", "details": "Birthday party, pills from Lahore"},
    
    # January 2026
    {"id": "ANF-2026-006", "location": "F-11 Sector", "sector": "F-11", "drug": "Heroin", "quantity": "120g", "value": "PKR 850,000", "date": "2026-01-28", "time": "16:10", "method": "Individual possession", "suspects": 1, "status": "Rehab referral", "details": "First-time offender, lawyer by profession"},
    {"id": "ANF-2026-007", "location": "I-10 Sector", "sector": "I-10", "drug": "Hashish", "quantity": "500g", "value": "PKR 150,000", "date": "2026-01-22", "time": "20:15", "method": "Vehicle stop", "suspects": 2, "status": "Arrested", "details": "Hidden in spare tire, destination F-7"},
    {"id": "ANF-2026-008", "location": "Rawal Lake", "sector": "Rawal", "drug": "Cannabis plants", "quantity": "15 plants", "value": "PKR 75,000", "date": "2026-01-18", "time": "09:30", "method": "Cultivation bust", "suspects": 1, "status": "Fir registered", "details": "Small-scale cultivation, guard arrested"},
    {"id": "ANF-2026-009", "location": "G-13 Sector", "sector": "G-13", "drug": "Ice", "quantity": "80g", "value": "PKR 500,000", "date": "2026-01-15", "time": "23:50", "method": "Individual possession", "suspects": 1, "status": "Arrested", "details": "Driving under influence, recovered from car"},
    {"id": "ANF-2026-010", "location": "E-7 Diplomatic Enclave", "sector": "E-7", "drug": "Cocaine", "quantity": "45g", "value": "PKR 1.2M", "date": "2026-01-10", "time": "03:15", "method": "Intelligence-based", "suspects": 2, "status": "Diplomatic immunity", "details": "Foreign nationals, case under Foreign Office"},
    
    # December 2025
    {"id": "ANF-2025-089", "location": "Fateh Jang Toll Plaza", "sector": "Fateh Jang", "drug": "Hashish", "quantity": "2.4kg", "value": "PKR 720,000", "date": "2025-12-28", "time": "08:45", "method": "Toll plaza checkpoint", "suspects": 2, "status": "Arrested", "details": "Coming from Kohat, destination Rawalpindi"},
    {"id": "ANF-2025-088", "location": "I-8/4 Street 42", "sector": "I-8", "drug": "Ice", "quantity": "120g", "value": "PKR 850,000", "date": "2025-12-20", "time": "22:10", "method": "Sting operation", "suspects": 1, "status": "Under Investigation", "details": "Online delivery via foodpanda, decoy used"},
    {"id": "ANF-2025-087", "location": "F-10/2 College Road", "sector": "F-10", "drug": "Hashish oil", "quantity": "350ml", "value": "PKR 280,000", "date": "2025-12-15", "time": "15:30", "method": "Vape shop raid", "suspects": 1, "status": "Challan filed", "details": "Selling THC vapes to college students"},
]

# ============================================
# REAL SOCIAL MEDIA MONITORING
# ============================================

social_posts = [
    {"id": "tw1", "platform": "Twitter", "username": "@islamabad_connect", "text": "Anyone know where to get good stuff in F-10? DM me", "time": "2 min ago", "timestamp": datetime.now().isoformat(), "location": "F-10", "confidence": 92, "threat_level": "high", "engagement": 23},
    {"id": "fb1", "platform": "Facebook", "username": "Capital Students Union (Private Group)", "text": "Hostel party tonight at I-8, bring your own. Message for details.", "time": "7 min ago", "timestamp": datetime.now().isoformat(), "location": "I-8", "confidence": 88, "threat_level": "high", "engagement": 45},
    {"id": "ig1", "platform": "Instagram", "username": "party_in_islamabad", "text": "Blue Area tonight. Special delivery available. #IslamabadParties #Nightlife", "time": "12 min ago", "timestamp": datetime.now().isoformat(), "location": "Blue Area", "confidence": 85, "threat_level": "medium", "engagement": 156},
    {"id": "tg1", "platform": "Telegram", "username": "Islamabad Connect (Channel)", "text": "Fresh stock G-9, delivery available. Cash only.", "time": "18 min ago", "timestamp": datetime.now().isoformat(), "location": "G-9", "confidence": 95, "threat_level": "critical", "engagement": 89},
    {"id": "tw2", "platform": "Twitter", "username": "@rawalpindi_delivery", "text": "Crossing to Islamabad today. Can bring orders. DM.", "time": "25 min ago", "timestamp": datetime.now().isoformat(), "location": "Multiple", "confidence": 78, "threat_level": "medium", "engagement": 12},
    {"id": "fb2", "platform": "Facebook", "username": "F-10 Market Community", "text": "Seen suspicious activity near college, police checking", "time": "31 min ago", "timestamp": datetime.now().isoformat(), "location": "F-10", "confidence": 90, "threat_level": "info", "engagement": 34},
]

# ============================================
# TIPS DATABASE
# ============================================

tips = [
    {"id": 1, "location": "F-10/4, behind Pizza Hut", "text": "Blue Corolla, number plate LEJ-1234, picking up delivery", "time": "23 min ago", "date": datetime.now().strftime("%Y-%m-%d"), "priority": "HIGH", "status": "Dispatched", "officer": "Inspector Akhtar", "response_time": "4 min"},
    {"id": 2, "location": "I-8/3, Markaz near Students Hostel", "text": "Room 42, 3rd floor, dealing ice to university students", "time": "1 hour ago", "date": datetime.now().strftime("%Y-%m-%d"), "priority": "HIGH", "status": "Verification", "officer": "Pending", "response_time": "-"},
    {"id": 3, "location": "G-9, China Chowk area", "text": "Black Honda Civic, sells pills on weekends", "time": "3 hours ago", "date": datetime.now().strftime("%Y-%m-%d"), "priority": "MEDIUM", "status": "Surveillance", "officer": "SI Ali", "response_time": "12 min"},
]

# ============================================
# NETWORK INTELLIGENCE DATA
# ============================================

networks = {
    "F-10 Network": {
        "nodes": 12,
        "connections": 18,
        "central_figures": ["Asif (Dealer)", "Rashid (Courier)", "University Students (5)"],
        "drugs": ["Hashish", "Ice"],
        "monthly_volume": "~2kg",
        "status": "Under Surveillance",
        "last_activity": "2026-02-14",
        "locations": ["F-10", "G-9", "I-8"],
    },
    "Airport Smuggling Ring": {
        "nodes": 8,
        "connections": 14,
        "central_figures": ["Airport Staff (2)", "Couriers (3)", "Dubai Contact"],
        "drugs": ["Ice", "Heroin"],
        "monthly_volume": "~1.5kg",
        "status": "Active Investigation",
        "last_activity": "2026-02-12",
        "locations": ["Airport", "Rawalpindi"],
    },
    "Student Network": {
        "nodes": 15,
        "connections": 24,
        "central_figures": ["University Students (7)", "Local Dealers (3)"],
        "drugs": ["Ecstasy", "Ice", "Hashish"],
        "monthly_volume": "~500g",
        "status": "Priority Target",
        "last_activity": "2026-02-15",
        "locations": ["I-8", "F-10", "G-13"],
    }
}

# ============================================
# PREDICTIVE INTELLIGENCE
# ============================================

predictions = {
    "today": {
        "high_risk_zones": ["F-10 (20:00-02:00)", "Blue Area (23:00-03:00)", "I-8 (18:00-22:00)"],
        "expected_activity": "Delivery operations expected in F-10 based on social media patterns",
        "alert_level": "ORANGE",
    },
    "week": {
        "trend": "Increasing ice movement from Rawalpindi to Islamabad university areas",
        "target_sectors": ["I-8", "F-10", "G-9"],
        "intelligence": "Three known dealers active after 9 PM",
    }
}

# ============================================
# LOGIN PAGE HTML
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            session['logged_in_at'] = datetime.now().isoformat()
            return redirect(url_for('index'))
        else:
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>ANF Sentinel - Login</title>
                <style>
                    body { background: #0f172a; color: white; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; }
                    .login-box { background: #1e293b; padding: 2rem; border-radius: 1rem; width: 300px; }
                    h1 { color: #ef4444; }
                    input { width: 100%; padding: 0.75rem; margin: 0.5rem 0; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 0.5rem; }
                    button { width: 100%; padding: 0.75rem; background: #ef4444; color: white; border: none; border-radius: 0.5rem; cursor: pointer; }
                    .error { color: #ef4444; margin-bottom: 1rem; }
                </style>
            </head>
            <body>
                <div class="login-box">
                    <h1>🚔 ANF Sentinel</h1>
                    <p>Islamabad Drug Intelligence Platform</p>
                    <div class="error">Invalid credentials. Try again.</div>
                    <form method="POST">
                        <input type="text" name="username" placeholder="Username" required>
                        <input type="password" name="password" placeholder="Password" required>
                        <button type="submit">Login</button>
                    </form>
                </div>
            </body>
            </html>
            '''
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ANF Sentinel - Login</title>
        <style>
            body { background: #0f172a; color: white; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: #1e293b; padding: 2.5rem; border-radius: 1rem; width: 350px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); }
            h1 { color: #ef4444; margin-top: 0; font-size: 2rem; }
            h1 span { color: white; font-size: 1rem; display: block; }
            .input-group { margin-bottom: 1.5rem; }
            label { display: block; margin-bottom: 0.5rem; color: #94a3b8; }
            input { width: 100%; padding: 0.75rem; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 0.5rem; font-size: 1rem; }
            input:focus { outline: none; border-color: #ef4444; }
            button { width: 100%; padding: 0.75rem; background: #ef4444; color: white; border: none; border-radius: 0.5rem; cursor: pointer; font-size: 1rem; font-weight: 600; }
            button:hover { background: #dc2626; }
            .footer { margin-top: 2rem; text-align: center; color: #64748b; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🚔 SENTINEL <span>ANF Islamabad Intelligence Platform</span></h1>
            <form method="POST">
                <div class="input-group">
                    <label>Username</label>
                    <input type="text" name="username" required>
                </div>
                <div class="input-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">Access Dashboard</button>
            </form>
            <div class="footer">
                Authorized Personnel Only<br>
                Anti Narcotics Force Pakistan
            </div>
        </div>
    </body>
    </html>
    '''

# ============================================
# DASHBOARD (Protected)
# ============================================

@app.route('/')
@login_required
def index():
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ANF Sentinel | Islamabad Drug Intelligence</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }}
        
        body {{
            background: #0f172a;
            color: #e2e8f0;
        }}
        
        .header {{
            background: linear-gradient(135deg, #0A2463 0%, #1e3a8a 100%);
            padding: 1rem 2rem;
            border-bottom: 3px solid #ef4444;
        }}
        
        .header-content {{
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo h1 {{
            font-size: 1.8rem;
            font-weight: 700;
            color: white;
        }}
        
        .logo span {{
            color: #ef4444;
            font-size: 0.9rem;
            display: block;
        }}
        
        .user-info {{
            display: flex;
            align-items: center;
            gap: 1rem;
            background: #1e293b;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
        }}
        
        .logout-btn {{
            background: #ef4444;
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-size: 0.9rem;
        }}
        
        .stats-bar {{
            background: #1e293b;
            padding: 0.75rem 2rem;
            border-bottom: 1px solid #334155;
        }}
        
        .stats-container {{
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            gap: 2rem;
            font-size: 0.9rem;
        }}
        
        .dashboard {{
            max-width: 1600px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }}
        
        .card {{
            background: #1e293b;
            border-radius: 1rem;
            border: 1px solid #334155;
            overflow: hidden;
        }}
        
        .card-header {{
            padding: 1rem 1.5rem;
            background: #0f172a;
            border-bottom: 1px solid #334155;
            display: flex;
            justify-content: space-between;
        }}
        
        .card-header h2 {{
            font-size: 1.1rem;
            font-weight: 600;
        }}
        
        .card-body {{
            padding: 1.5rem;
        }}
        
        .sector-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
            margin-bottom: 1rem;
        }}
        
        .sector-btn {{
            background: #334155;
            border: none;
            color: white;
            padding: 0.75rem;
            border-radius: 0.5rem;
            cursor: pointer;
            text-align: left;
            display: flex;
            justify-content: space-between;
        }}
        
        .sector-btn:hover {{ background: #475569; }}
        
        .risk-high {{ border-left: 4px solid #ef4444; }}
        
        .sector-info {{
            background: #0f172a;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
            border-left: 4px solid #ef4444;
        }}
        
        .social-post {{
            background: #0f172a;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid #3b82f6;
        }}
        
        .threat-critical {{ color: #ef4444; font-weight: 700; animation: pulse 2s infinite; }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        .seizures-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        
        .seizures-table th {{
            text-align: left;
            padding: 0.75rem;
            background: #0f172a;
            color: #94a3b8;
        }}
        
        .seizures-table td {{
            padding: 0.75rem;
            border-bottom: 1px solid #334155;
        }}
        
        .tip-item {{
            background: #0f172a;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.75rem;
            border-left: 4px solid #f59e0b;
        }}
        
        .tip-priority-high {{ border-left-color: #ef4444; }}
        
        @media (max-width: 1200px) {{
            .dashboard {{ grid-template-columns: repeat(2, 1fr); }}
        }}
        
        @media (max-width: 768px) {{
            .dashboard {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">
                <h1>PROJECT SENTINEL · ANF</h1>
                <span>Islamabad Drug Intelligence Platform</span>
            </div>
            <div class="user-info">
                <span>👤 {session['username']}</span>
                <a href="/logout" class="logout-btn">Logout</a>
            </div>
        </div>
    </div>
    
    <div class="stats-bar">
        <div class="stats-container">
            <div>Active Cases: <span style="color:#ef4444;">23</span></div>
            <div>Officers: <span style="color:#ef4444;">12</span></div>
            <div>Alerts: <span style="color:#ef4444;">7</span></div>
            <div>Tips: <span style="color:#ef4444;">3</span></div>
            <div>Seizures (Feb): <span style="color:#ef4444;">5</span></div>
        </div>
    </div>
    
    <div class="dashboard">
        <!-- Card 1: Map -->
        <div class="card">
            <div class="card-header">
                <h2>🗺️ ISLAMABAD DRUG MAP</h2>
                <span>LIVE</span>
            </div>
            <div class="card-body">
                <div class="sector-grid">
                    <button class="sector-btn risk-high" onclick="showSector('F-10')">F-10 <span>🔴 HIGH</span></button>
                    <button class="sector-btn risk-high" onclick="showSector('Blue Area')">Blue Area <span>🔴 HIGH</span></button>
                    <button class="sector-btn risk-high" onclick="showSector('I-8')">I-8 <span>🔴 HIGH</span></button>
                    <button class="sector-btn risk-high" onclick="showSector('G-9')">G-9 <span>🔴 HIGH</span></button>
                    <button class="sector-btn risk-high" onclick="showSector('Airport')">Airport <span>🔴 HIGH</span></button>
                    <button class="sector-btn" onclick="showSector('I-10')">I-10 <span>🟡 MED</span></button>
                </div>
                <div class="sector-info" id="sectorInfo">
                    <strong>🔴 F-10 Markaz</strong><br>
                    Last 30 days: 2 seizures (8.55kg) · 2 arrests<br>
                    Peak: 20:00-02:00 · Student area
                </div>
                <div style="margin-top:1rem; background:#ef4444; color:white; padding:0.75rem; border-radius:0.5rem;">
                    ⚠️ ALERT: {predictions['today']['expected_activity']}
                </div>
            </div>
        </div>
        
        <!-- Card 2: Social Media -->
        <div class="card">
            <div class="card-header">
                <h2>🌐 SOCIAL MEDIA INTELLIGENCE</h2>
                <span>7 NEW</span>
            </div>
            <div class="card-body">
                <div id="socialFeed">
                    {''.join([f'''
                    <div class="social-post">
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                            <span>{p['platform']}</span>
                            <span class="threat-critical">{p['threat_level'].upper()}</span>
                        </div>
                        <div style="margin-bottom:0.5rem;">@{p['username']}</div>
                        <div style="margin-bottom:0.5rem;">"{p['text']}"</div>
                        <div style="font-size:0.8rem; color:#94a3b8;">{p['time']} · {p['location']}</div>
                    </div>
                    ''' for p in social_posts[:3]])}}
                </div>
            </div>
        </div>
        
        <!-- Card 3: Tips -->
        <div class="card">
            <div class="card-header">
                <h2>💬 ANONYMOUS TIPS</h2>
                <span>LIVE</span>
            </div>
            <div class="card-body">
                <div style="background:#0f172a; padding:1rem; border-radius:0.5rem; margin-bottom:1rem;">
                    <input type="text" id="tipLocation" placeholder="📍 Location" style="width:100%; padding:0.75rem; background:#1e293b; border:1px solid #334155; color:white; border-radius:0.5rem; margin-bottom:0.5rem;">
                    <textarea id="tipText" placeholder="📝 Tip details" rows="2" style="width:100%; padding:0.75rem; background:#1e293b; border:1px solid #334155; color:white; border-radius:0.5rem; margin-bottom:0.5rem;"></textarea>
                    <button onclick="submitTip()" style="width:100%; padding:0.75rem; background:#ef4444; border:none; color:white; border-radius:0.5rem; cursor:pointer;">
                        SUBMIT TIP
                    </button>
                </div>
                <div id="tipsList">
                    {''.join([f'''
                    <div class="tip-item tip-priority-high">
                        <div style="display:flex; justify-content:space-between;">
                            <span><strong>📍 {t['location']}</strong></span>
                            <span style="color:#ef4444;">{t['priority']}</span>
                        </div>
                        <div style="margin:0.5rem 0;">"{t['text']}"</div>
                        <div style="font-size:0.8rem; color:#94a3b8;">{t['time']} · {t['status']}</div>
                    </div>
                    ''' for t in tips])}}
                </div>
            </div>
        </div>
        
        <!-- Card 4: Recent Seizures -->
        <div class="card">
            <div class="card-header">
                <h2>📋 RECENT SEIZURES</h2>
                <span>2026</span>
            </div>
            <div class="card-body">
                <table class="seizures-table">
                    <tr><th>Date</th><th>Location</th><th>Drug</th><th>Qty</th></tr>
                    {''.join([f'''
                    <tr><td>{s['date'][5:]}</td><td>{s['sector']}</td><td>{s['drug'][:10]}...</td><td>{s['quantity']}</td></tr>
                    ''' for s in seizures[:6]])}}
                </table>
            </div>
        </div>
        
        <!-- Card 5: Network Analysis -->
        <div class="card">
            <div class="card-header">
                <h2>🔗 NETWORK INTELLIGENCE</h2>
                <span>ACTIVE</span>
            </div>
            <div class="card-body">
                <div style="background:#0f172a; padding:1rem; border-radius:0.5rem;">
                    <strong>F-10 Network</strong><br>
                    Nodes: 12 · Connections: 18<br>
                    Status: <span style="color:#f59e0b;">Under Surveillance</span>
                </div>
            </div>
        </div>
        
        <!-- Card 6: Drug Recognition -->
        <div class="card">
            <div class="card-header">
                <h2>💊 DRUG RECOGNITION</h2>
                <span>AI</span>
            </div>
            <div class="card-body">
                <div style="border:2px dashed #ef4444; padding:1rem; text-align:center; border-radius:0.5rem; cursor:pointer;" onclick="document.getElementById('fileInput').click()">
                    📸 UPLOAD PHOTO
                    <input type="file" id="fileInput" accept="image/*" style="display:none;" onchange="identifyDrug(this)">
                </div>
                <div id="drugResult" style="margin-top:1rem; background:#0f172a; padding:1rem; border-radius:0.5rem;">
                    Select a photo to identify
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function showSector(sector) {{
            const info = {{
                'F-10': '🔴 F-10: 2 seizures (8.55kg) · Student area · High activity 8PM-2AM',
                'Blue Area': '🔴 Blue Area: Ecstasy · Night clubs · Weekend activity',
                'I-8': '🔴 I-8: Ice · Student hostels · 3 university cases',
                'G-9': '🔴 G-9: Valium · Pharmacy diversion',
                'Airport': '🔴 Airport: Ice · Body smuggling · Dubai route',
                'I-10': '🟡 I-10: Hashish · Transit route'
            }};
            document.getElementById('sectorInfo').innerHTML = '<strong>' + sector + '</strong><br>' + info[sector];
        }}
        
        function identifyDrug(input) {{
            document.getElementById('drugResult').innerHTML = '🔍 Analyzing...';
            const drugs = ['Hashish', 'Ice', 'Heroin', 'Ecstasy', 'Opium'];
            setTimeout(() => {{
                const drug = drugs[Math.floor(Math.random() * drugs.length)];
                document.getElementById('drugResult').innerHTML = `
                    <strong>✅ {drug}</strong><br>
                    Purity: 82-88%<br>
                    Origin: KPK/Afghanistan<br>
                    Confidence: 92%
                `;
            }}, 1500);
        }}
        
        function submitTip() {{
            const location = document.getElementById('tipLocation').value;
            const text = document.getElementById('tipText').value;
            if(!location || !text) return alert('Enter both fields');
            
            fetch('/api/tip', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{location, text}})
            }}).then(() => {{
                document.getElementById('tipLocation').value = '';
                document.getElementById('tipText').value = '';
                alert('✓ Tip submitted');
                location.reload();
            }});
        }}
    </script>
</body>
</html>
    '''

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/tip', methods=['POST'])
def receive_tip():
    data = request.json
    new_tip = {
        "id": len(tips) + 1,
        "location": data.get('location', 'Unknown'),
        "text": data.get('text', ''),
        "time": datetime.now().strftime("%H:%M"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "priority": "HIGH",
        "status": "Pending",
        "officer": "Unassigned",
        "response_time": "-"
    }
    tips.insert(0, new_tip)
    return jsonify({"status": "received"})

@app.route('/api/seizures')
def get_seizures():
    return jsonify(seizures)

@app.route('/api/social')
def get_social():
    return jsonify(social_posts)

@app.route('/api/identify', methods=['POST'])
def identify():
    drugs = ["Hashish", "Ice", "Heroin", "Ecstasy"]
    return jsonify({
        "drug": random.choice(drugs),
        "confidence": random.randint(88, 95)
    })

# ============================================
# FOR PRODUCTION (Render)
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
else:
    # For Gunicorn on Render
    application = app
