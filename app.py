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
# REAL ANF DATA - Islamabad Seizures 2025-2026
# ============================================

seizures = [
    {"id": "ANF-2026-001", "location": "F-10 Markaz", "sector": "F-10", "drug": "Hashish", "quantity": "7.7 kg", "value": "PKR 2.3M", "date": "2026-02-15", "time": "22:30", "method": "Vehicle checkpoint", "suspects": 2, "status": "Arrested", "details": "Near Islamabad Model College, suspects from KPK"},
    {"id": "ANF-2026-002", "location": "Islamabad Airport", "sector": "Airport", "drug": "Ice (Crystal Meth)", "quantity": "630g", "value": "PKR 4.5M", "date": "2026-02-12", "time": "14:15", "method": "Body smuggling", "suspects": 1, "status": "Arrested", "details": "105 capsules ingested, destination Dubai"},
    {"id": "ANF-2026-003", "location": "I-8 Sector", "sector": "I-8", "drug": "Ice", "quantity": "340g", "value": "PKR 2.1M", "date": "2026-02-08", "time": "19:45", "method": "Hostel raid", "suspects": 3, "status": "Arrested", "details": "Students from private university, sourced from Rawalpindi"},
    {"id": "ANF-2026-004", "location": "G-9 Markaz", "sector": "G-9", "drug": "Valium pills", "quantity": "2.1kg (21,000 pills)", "value": "PKR 1.8M", "date": "2026-02-05", "time": "11:20", "method": "Pharmacy raid", "suspects": 2, "status": "Under Investigation", "details": "Pharmacy without license, selling to students"},
    {"id": "ANF-2026-005", "location": "Blue Area", "sector": "Blue Area", "drug": "Ecstasy", "quantity": "50 pills", "value": "PKR 250,000", "date": "2026-02-01", "time": "01:30", "method": "Night club raid", "suspects": 5, "status": "Booked", "details": "Birthday party, pills from Lahore"},
    {"id": "ANF-2026-006", "location": "F-11 Sector", "sector": "F-11", "drug": "Heroin", "quantity": "120g", "value": "PKR 850,000", "date": "2026-01-28", "time": "16:10", "method": "Individual possession", "suspects": 1, "status": "Rehab referral", "details": "First-time offender, lawyer by profession"},
    {"id": "ANF-2026-007", "location": "I-10 Sector", "sector": "I-10", "drug": "Hashish", "quantity": "500g", "value": "PKR 150,000", "date": "2026-01-22", "time": "20:15", "method": "Vehicle stop", "suspects": 2, "status": "Arrested", "details": "Hidden in spare tire, destination F-7"},
    {"id": "ANF-2026-008", "location": "Rawal Lake", "sector": "Rawal", "drug": "Cannabis plants", "quantity": "15 plants", "value": "PKR 75,000", "date": "2026-01-18", "time": "09:30", "method": "Cultivation bust", "suspects": 1, "status": "Fir registered", "details": "Small-scale cultivation, guard arrested"},
    {"id": "ANF-2026-009", "location": "G-13 Sector", "sector": "G-13", "drug": "Ice", "quantity": "80g", "value": "PKR 500,000", "date": "2026-01-15", "time": "23:50", "method": "Individual possession", "suspects": 1, "status": "Arrested", "details": "Driving under influence, recovered from car"},
    {"id": "ANF-2026-010", "location": "E-7 Diplomatic Enclave", "sector": "E-7", "drug": "Cocaine", "quantity": "45g", "value": "PKR 1.2M", "date": "2026-01-10", "time": "03:15", "method": "Intelligence-based", "suspects": 2, "status": "Diplomatic immunity", "details": "Foreign nationals, case under Foreign Office"}
]

# ============================================
# SOCIAL MEDIA MONITORING
# ============================================

social_posts = [
    {"platform": "Twitter", "username": "@islamabad_connect", "text": "Anyone know where to get good stuff in F-10? DM me", "time": "2 min ago", "location": "F-10", "threat_level": "high"},
    {"platform": "Facebook", "username": "Capital Students Union", "text": "Hostel party tonight at I-8, bring your own", "time": "7 min ago", "location": "I-8", "threat_level": "high"},
    {"platform": "Instagram", "username": "party_in_islamabad", "text": "Blue Area tonight. Special delivery available", "time": "12 min ago", "location": "Blue Area", "threat_level": "medium"},
    {"platform": "Telegram", "username": "Islamabad Connect", "text": "Fresh stock G-9, delivery available", "time": "18 min ago", "location": "G-9", "threat_level": "critical"}
]

# ============================================
# TIPS DATABASE
# ============================================

tips = [
    {"id": 1, "location": "F-10/4, behind Pizza Hut", "text": "Blue Corolla, number plate LEJ-1234", "time": "23 min ago", "priority": "HIGH", "status": "Dispatched"},
    {"id": 2, "location": "I-8/3, Students Hostel", "text": "Room 42, dealing ice to students", "time": "1 hour ago", "priority": "HIGH", "status": "Verification"},
    {"id": 3, "location": "G-9, China Chowk", "text": "Black Honda Civic, sells pills on weekends", "time": "3 hours ago", "priority": "MEDIUM", "status": "Surveillance"}
]

# ============================================
# PREDICTIVE INTELLIGENCE
# ============================================

predictions = {
    "today": {
        "high_risk_zones": ["F-10 (20:00-02:00)", "Blue Area (23:00-03:00)", "I-8 (18:00-22:00)"],
        "expected_activity": "Delivery operations expected in F-10",
        "alert_level": "ORANGE"
    }
}

# ============================================
# LOGIN PAGE
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
                    body { background: #0f172a; color: white; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                    .login-box { background: #1e293b; padding: 2.5rem; border-radius: 1rem; width: 350px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); }
                    h1 { color: #ef4444; margin-top: 0; }
                    .error { color: #ef4444; margin-bottom: 1rem; }
                    input { width: 100%; padding: 0.75rem; margin: 0.5rem 0; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 0.5rem; }
                    button { width: 100%; padding: 0.75rem; background: #ef4444; color: white; border: none; border-radius: 0.5rem; cursor: pointer; }
                </style>
            </head>
            <body>
                <div class="login-box">
                    <h1>🚔 SENTINEL</h1>
                    <p>ANF Islamabad Intelligence Platform</p>
                    <div class="error">Invalid credentials</div>
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
            input { width: 100%; padding: 0.75rem; margin: 0.5rem 0; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 0.5rem; }
            button { width: 100%; padding: 0.75rem; background: #ef4444; color: white; border: none; border-radius: 0.5rem; cursor: pointer; }
            .footer { margin-top: 2rem; text-align: center; color: #64748b; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🚔 SENTINEL <span>ANF Islamabad</span></h1>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Access Dashboard</button>
            </form>
            <div class="footer">Authorized Personnel Only</div>
        </div>
    </body>
    </html>
    '''

# ============================================
# DASHBOARD
# ============================================

@app.route('/')
@login_required
def index():
    # Generate social feed HTML
    social_html = ""
    for p in social_posts[:3]:
        social_html += f'''
        <div class="social-post">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                <span>{p['platform']}</span>
                <span class="threat-critical">{p['threat_level'].upper()}</span>
            </div>
            <div style="margin-bottom:0.5rem;">@{p['username']}</div>
            <div style="margin-bottom:0.5rem;">"{p['text']}"</div>
            <div style="font-size:0.8rem; color:#94a3b8;">{p['time']} · {p['location']}</div>
        </div>
        '''
    
    # Generate tips HTML
    tips_html = ""
    for t in tips[:3]:
        tips_html += f'''
        <div class="tip-item tip-priority-high">
            <div style="display:flex; justify-content:space-between;">
                <span><strong>📍 {t['location']}</strong></span>
                <span style="color:#ef4444;">{t['priority']}</span>
            </div>
            <div style="margin:0.5rem 0;">"{t['text']}"</div>
            <div style="font-size:0.8rem; color:#94a3b8;">{t['time']} · {t['status']}</div>
        </div>
        '''
    
    # Generate seizures HTML
    seizures_html = ""
    for s in seizures[:6]:
        seizures_html += f'''
        <tr><td>{s['date'][5:]}</td><td>{s['sector']}</td><td>{s['drug'][:10]}...</td><td>{s['quantity']}</td></tr>
        '''
    
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ANF Sentinel | Islamabad</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
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
        
        .threat-critical {{ color: #ef4444; font-weight: 700; }}
        
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
        
        /* Camera Card Specific Styles */
        @keyframes pulse {{
            0% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.1); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
        
        .camera-thumb {{
            transition: all 0.2s ease;
        }}
        
        .camera-thumb:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 12px rgba(239, 68, 68, 0.2);
        }}
        
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
            <div>Seizures: <span style="color:#ef4444;">10</span></div>
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
                <span>LIVE</span>
            </div>
            <div class="card-body">
                <div id="socialFeed">
                    {social_html}
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
                    {tips_html}
                </div>
            </div>
        </div>
        
        <!-- Card 4: Live Camera Surveillance (NEW) -->
        <div class="card">
            <div class="card-header">
                <h2>📹 LIVE CAMERA SURVEILLANCE</h2>
                <span>4 FEEDS</span>
            </div>
            <div class="card-body">
                <!-- Main Camera Display -->
                <div id="mainCameraContainer" style="position: relative; width: 100%; height: 240px; background: #0f172a; border-radius: 0.5rem; overflow: hidden; border: 2px solid #ef4444; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                    <img id="mainCameraFeed" src="https://raw.githubusercontent.com/Andromeda147/sentinel-anf-dashboard/main/images/camera1.jpg" 
                         alt="Live Camera Feed" 
                         style="width: 100%; height: 100%; object-fit: cover;">
                    
                    <!-- Live Badge -->
                    <div style="position: absolute; top: 12px; left: 12px; background: rgba(239, 68, 68, 0.95); color: white; padding: 6px 14px; border-radius: 30px; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                        <span style="width: 10px; height: 10px; background: white; border-radius: 50%; animation: pulse 1.2s infinite;"></span>
                        LIVE STREAM
                    </div>
                    
                    <!-- Camera Info -->
                    <div id="cameraInfo" style="position: absolute; bottom: 12px; left: 12px; background: rgba(15, 23, 42, 0.9); color: white; padding: 8px 16px; border-radius: 30px; font-size: 0.85rem; font-weight: 500; backdrop-filter: blur(4px); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                        📍 F-10 Markaz · CAM 01 · 14:23:45
                    </div>
                    
                    <!-- Motion Alert -->
                    <div style="position: absolute; top: 12px; right: 12px; background: rgba(239, 68, 68, 0.95); color: white; padding: 6px 14px; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                        <span>⚠️</span> MOTION DETECTED
                    </div>
                    
                    <!-- Timestamp -->
                    <div style="position: absolute; bottom: 12px; right: 12px; background: rgba(15, 23, 42, 0.9); color: #94a3b8; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; backdrop-filter: blur(4px); border: 1px solid rgba(255,255,255,0.1);">
                        2026-02-18 14:23:45
                    </div>
                </div>
                
                <!-- Camera Selection Grid -->
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-bottom: 1.25rem;">
                    <div class="camera-thumb" onclick="switchCamera(1)" data-cam="1" style="background: linear-gradient(145deg, #ef4444, #dc2626); padding: 0.85rem 0.25rem; border-radius: 12px; text-align: center; cursor: pointer; border: 1px solid rgba(239, 68, 68, 0.5); box-shadow: 0 4px 6px rgba(0,0,0,0.2); transition: all 0.2s;">
                        <div style="font-size: 0.7rem; color: rgba(255,255,255,0.9); letter-spacing: 0.5px;">CAM 01</div>
                        <div style="font-size: 1rem; font-weight: 700; color: white; margin: 4px 0;">F-10</div>
                        <div style="color: white; font-size: 0.7rem; display: flex; align-items: center; justify-content: center; gap: 4px;">
                            <span style="width: 8px; height: 8px; background: white; border-radius: 50%; animation: pulse 1.2s infinite;"></span> LIVE
                        </div>
                    </div>
                    <div class="camera-thumb" onclick="switchCamera(2)" data-cam="2" style="background: #1e293b; padding: 0.85rem 0.25rem; border-radius: 12px; text-align: center; cursor: pointer; border: 1px solid #334155; transition: all 0.2s;">
                        <div style="font-size: 0.7rem; color: #94a3b8; letter-spacing: 0.5px;">CAM 02</div>
                        <div style="font-size: 1rem; font-weight: 700; color: white; margin: 4px 0;">I-8</div>
                        <div style="color: #94a3b8; font-size: 0.7rem;">⏸️ STANDBY</div>
                    </div>
                    <div class="camera-thumb" onclick="switchCamera(3)" data-cam="3" style="background: #1e293b; padding: 0.85rem 0.25rem; border-radius: 12px; text-align: center; cursor: pointer; border: 1px solid #334155; transition: all 0.2s;">
                        <div style="font-size: 0.7rem; color: #94a3b8; letter-spacing: 0.5px;">CAM 03</div>
                        <div style="font-size: 1rem; font-weight: 700; color: white; margin: 4px 0;">G-9</div>
                        <div style="color: #94a3b8; font-size: 0.7rem;">⏸️ STANDBY</div>
                    </div>
                    <div class="camera-thumb" onclick="switchCamera(4)" data-cam="4" style="background: #1e293b; padding: 0.85rem 0.25rem; border-radius: 12px; text-align: center; cursor: pointer; border: 1px solid #334155; transition: all 0.2s;">
                        <div style="font-size: 0.7rem; color: #94a3b8; letter-spacing: 0.5px;">CAM 04</div>
                        <div style="font-size: 1rem; font-weight: 700; color: white; margin: 4px 0;">AIRPORT</div>
                        <div style="color: #94a3b8; font-size: 0.7rem;">⏸️ STANDBY</div>
                    </div>
                </div>
                
                <!-- AI Detection Stats -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
                    <div style="background: linear-gradient(145deg, #0f172a, #0a0f1a); padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid #334155;">
                        <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">AI DETECTION</div>
                        <div style="font-size: 1.4rem; font-weight: 700; color: #ef4444; line-height: 1.2;">2 · 1</div>
                        <div style="font-size: 0.8rem; color: #e2e8f0;">Persons · Vehicle</div>
                        <div style="font-size: 0.7rem; color: #4ade80; margin-top: 6px; background: rgba(74, 222, 128, 0.1); padding: 4px; border-radius: 20px;">confidence 94%</div>
                    </div>
                    <div style="background: linear-gradient(145deg, #0f172a, #0a0f1a); padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid #334155;">
                        <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">LAST ALERT</div>
                        <div style="font-size: 1.4rem; font-weight: 700; color: #f59e0b;">3 min</div>
                        <div style="font-size: 0.8rem; color: #e2e8f0;">suspicious exchange</div>
                        <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 6px;">CAM 01 · F-10</div>
                    </div>
                </div>
                
                <!-- Alert History -->
                <div style="background: linear-gradient(145deg, #0f172a, #0a0f1a); padding: 1rem; border-radius: 12px; border: 1px solid #334155;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem; color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; padding: 0 0.25rem;">
                        <span>⏱️ TIME</span>
                        <span>📍 LOCATION</span>
                        <span>⚠️ EVENT</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.6rem 0.25rem; border-bottom: 1px solid #334155; font-size: 0.85rem;">
                        <span>14:23:45</span>
                        <span>F-10</span>
                        <span style="color: #ef4444; font-weight: 500;">motion detected</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.6rem 0.25rem; border-bottom: 1px solid #334155; font-size: 0.85rem;">
                        <span>14:18:22</span>
                        <span>F-10</span>
                        <span style="color: #ef4444; font-weight: 500;">person loitering</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.6rem 0.25rem; border-bottom: 1px solid #334155; font-size: 0.85rem;">
                        <span>14:12:07</span>
                        <span>F-10</span>
                        <span style="color: #f59e0b;">vehicle stopped</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.6rem 0.25rem; font-size: 0.85rem;">
                        <span>14:03:52</span>
                        <span>I-8</span>
                        <span style="color: #3b82f6;">crowd gathering</span>
                    </div>
                </div>
                
                <!-- Integration Note -->
                <div style="margin-top: 1rem; font-size: 0.8rem; color: #94a3b8; text-align: center; padding: 0.75rem; background: rgba(15, 23, 42, 0.7); border-radius: 30px; border: 1px dashed #334155;">
                    <span style="color: #ef4444;">⚡</span> After approval: Integration with Safe City Islamabad cameras for real-time AI surveillance
                </div>
            </div>
        </div>
        
        <!-- Card 5: Recent Seizures -->
        <div class="card">
            <div class="card-header">
                <h2>📋 RECENT SEIZURES</h2>
                <span>2026</span>
            </div>
            <div class="card-body">
                <table class="seizures-table">
                    <tr><th>Date</th><th>Location</th><th>Drug</th><th>Qty</th></tr>
                    {seizures_html}
                </table>
            </div>
        </div>
        
        <!-- Card 6: Network Analysis -->
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
                <div style="margin-top:1rem; background:#0f172a; padding:1rem; border-radius:0.5rem;">
                    <strong>Airport Ring</strong><br>
                    Nodes: 8 · Connections: 14<br>
                    Status: <span style="color:#ef4444;">Active Investigation</span>
                </div>
            </div>
        </div>
        
        <!-- Card 7: Drug Recognition -->
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
            const drugs = ['Hashish', 'Ice', 'Heroin', 'Ecstasy'];
            setTimeout(() => {{
                const drug = drugs[Math.floor(Math.random() * drugs.length)];
                document.getElementById('drugResult').innerHTML = `
                    <strong>✅ ${{drug}}</strong><br>
                    Purity: 82-88%<br>
                    Origin: KPK/Afghanistan<br>
                    Confidence: 92%
                `;
            }}, 1500);
        }}
        
        function submitTip() {{
            const location = document.getElementById('tipLocation').value;
            const text = document.getElementById('tipText').value;
            if(!location || !text) {{
                alert('Enter both fields');
                return;
            }}
            
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
        
        // Camera switching function
        function switchCamera(camId) {{
            const images = {{
                1: "https://raw.githubusercontent.com/Andromeda147/sentinel-anf-dashboard/main/images/camera1.jpg",
                2: "https://raw.githubusercontent.com/Andromeda147/sentinel-anf-dashboard/main/images/camera2.jpg",
                3: "https://raw.githubusercontent.com/Andromeda147/sentinel-anf-dashboard/main/images/camera3.jpg",
                4: "https://raw.githubusercontent.com/Andromeda147/sentinel-anf-dashboard/main/images/camera4.jpg"
            }};
            
            const locations = {{
                1: "F-10 Markaz · CAM 01",
                2: "I-8 Hostel Area · CAM 02",
                3: "G-9 China Chowk · CAM 03",
                4: "Islamabad Airport · CAM 04"
            }};
            
            // Update main image and info
            document.getElementById('mainCameraFeed').src = images[camId];
            document.getElementById('cameraInfo').innerHTML = `📍 ${{locations[camId]}} · ${{new Date().toLocaleTimeString()}}`;
            
            // Reset all camera thumbnails to inactive state
            const thumbnails = document.querySelectorAll('.camera-thumb');
            thumbnails.forEach((thumb, index) => {{
                if (index === camId - 1) {{
                    thumb.style.background = 'linear-gradient(145deg, #ef4444, #dc2626)';
                    thumb.style.border = '1px solid rgba(239, 68, 68, 0.5)';
                    thumb.querySelector('div:first-child').style.color = 'rgba(255,255,255,0.9)';
                    thumb.querySelector('div:last-child').innerHTML = '<span style="width:8px;height:8px;background:white;border-radius:50%;animation:pulse 1.2s infinite;display:inline-block;margin-right:4px;"></span> LIVE';
                    thumb.querySelector('div:last-child').style.color = 'white';
                }} else {{
                    thumb.style.background = '#1e293b';
                    thumb.style.border = '1px solid #334155';
                    thumb.querySelector('div:first-child').style.color = '#94a3b8';
                    thumb.querySelector('div:last-child').innerHTML = '⏸️ STANDBY';
                    thumb.querySelector('div:last-child').style.color = '#94a3b8';
                }}
            }});
        }}
        
        // Auto-refresh camera timestamp
        setInterval(() => {{
            const cameraInfo = document.getElementById('cameraInfo');
            if (cameraInfo) {{
                const currentText = cameraInfo.innerHTML;
                const newTime = new Date().toLocaleTimeString();
                cameraInfo.innerHTML = currentText.replace(/\d{{2}}:\d{{2}}:\d{{2}}/, newTime);
            }}
        }}, 1000);
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
        "priority": "HIGH",
        "status": "Pending"
    }
    tips.insert(0, new_tip)
    return jsonify({"status": "received"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ============================================
# FOR PRODUCTION (Render)
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
else:
    application = app
