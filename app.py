from flask import Flask, render_template, request
from nlu_engine import SmartIncidentNLU
from db_config import init_db, insert_ticket, get_db_connection

app = Flask(__name__)

# -------------------------------
# Initialize DB
# -------------------------------
print("Initializing database...")
init_db()

# -------------------------------
# Initialize NLU Engine
# -------------------------------
print("Initializing NLU Engine (This may take a moment)...")
nlu = SmartIncidentNLU()


# =====================================================
# HOME ROUTE
# =====================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        complaint = request.form.get('complaint')

        if not complaint:
            return render_template('index.html', error="Please enter a complaint text.")

        analysis = nlu.analyze_complaint(complaint)

        ticket_id = insert_ticket(
            complaint_text=analysis['complaint_text'],
            category=analysis['category'],
            sentiment=analysis['sentiment'],
            priority=analysis['priority'],
            department=analysis['department'],
            escalation_flag=analysis['escalation_flag'],
            reply_text=analysis['reply_text']
        )

        analysis['ticket_id'] = ticket_id
        return render_template('result.html', result=analysis)

    return render_template('index.html')


# =====================================================
# DASHBOARD ROUTE (FIXED)
# =====================================================
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Category Distribution
    cursor.execute("SELECT category, COUNT(*) as count FROM tickets GROUP BY category")
    category_data = cursor.fetchall()

    # Priority Distribution
    cursor.execute("SELECT priority, COUNT(*) as count FROM tickets GROUP BY priority")
    priority_data = cursor.fetchall()

    # Daily Trend
    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM tickets
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """)
    daily_data = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        category_data=category_data,
        priority_data=priority_data,
        daily_data=daily_data
    )


# =====================================================
# RUN
# =====================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)