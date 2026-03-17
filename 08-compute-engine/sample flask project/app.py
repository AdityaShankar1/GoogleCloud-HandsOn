from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
# Updated path for GCP Cloud Storage FUSE mount
DB_PATH = "/app/data"
DB_NAME = os.path.join(DB_PATH, "life_app.db")

session = requests.Session()
retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def init_db():
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, meal_type TEXT, difficulty TEXT, temp TEXT, flavor TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS finance (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, amount REAL)")
        conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)")
    conn.commit()

def get_weather_multi():
    cities = ["Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore", "Indore", "Varanasi"]
    weather_reports = []
    for city in cities:
        try:
            r = session.get(f"https://wttr.in/{city}?format=3", timeout=2)
            weather_reports.append(r.text.strip()) if r.status_code == 200 else weather_reports.append(f"{city}: N/A")
        except:
            weather_reports.append(f"{city}: Timeout")
    return weather_reports

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        recipes = conn.execute("SELECT * FROM recipes ORDER BY id DESC").fetchall()
        finance = conn.execute("SELECT * FROM finance ORDER BY id DESC").fetchall()
        notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    weather_list = get_weather_multi()

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Life++</title>
        <style>
            :root { 
                --glass: rgba(255, 255, 255, 0.94); 
                --text: #202124; 
                --bg-overlay: rgba(255, 255, 255, 0.40); 
                --bg-img: url('/static/hero.jpg');
                --panel-border: rgba(0, 0, 0, 0.1);
            }
            body.dark-mode { 
                --glass: rgba(30, 30, 30, 0.96); 
                --text: #f1f1f1; 
                --bg-overlay: rgba(0, 0, 0, 0.40); 
                --bg-img: url('/static/night.avif');
                --panel-border: rgba(255, 255, 255, 0.1);
            }
            body { 
                font-family: -apple-system, sans-serif; margin: 0; padding: 25px; color: var(--text);
                background: linear-gradient(var(--bg-overlay), var(--bg-overlay)), var(--bg-img);
                background-size: cover; background-attachment: fixed; background-position: center; 
                min-height: 100vh; transition: background 0.4s ease-in-out;
            }
            .app-header { text-align: center; margin-bottom: 30px; }
            .app-header h1 { font-size: 2.5rem; font-weight: 800; letter-spacing: -1px; margin: 0; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); }
            .main-grid { display: grid; grid-template-columns: 320px 1fr 340px; gap: 20px; max-width: 1600px; margin: auto; }
            .panel { background: var(--glass); padding: 20px; border-radius: 16px; box-shadow: 0 12px 40px rgba(0,0,0,0.25); backdrop-filter: blur(12px); border: 1px solid var(--panel-border); display: flex; flex-direction: column; }
            h3 { margin: 0 0 15px 0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; border-bottom: 1px solid rgba(0,0,0,0.1); padding-bottom: 8px; color: #444; }
            .dark-mode h3 { border-bottom-color: #444; color: #bbb; }
            input, select, textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; font-size: 14px; background: #fff; }
            .dark-mode input, .dark-mode select, .dark-mode textarea { background: #252525; color: white; border-color: #444; }
            .btn { padding: 10px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px; transition: transform 0.1s; }
            .btn-blue { background: #1a73e8; color: white; }
            .btn-green { background: #1e8e3e; color: white; width: 100%; }
            .btn-red { background: #d93025; color: white; }
            #mode-toggle { position: fixed; top: 20px; right: 20px; z-index: 1000; padding: 10px 18px; border-radius: 20px; background: var(--glass); border: 1px solid var(--panel-border); cursor: pointer; font-weight: bold; font-size: 11px; }
            .scroll-area { max-height: 400px; overflow-y: auto; }
            .recipe-card { background: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; border-left: 5px solid #1e8e3e; margin-bottom: 10px; }
            .note-item { background: rgba(255, 255, 255, 0.6); padding: 12px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.1); margin-bottom: 12px; }
            .dark-mode .note-item { background: rgba(255, 255, 255, 0.05); }
            .clear-link { font-size: 11px; color: #d93025; text-decoration: none; text-align: center; display: block; margin-top: 10px; font-weight: 600; opacity: 0.7; }
        </style>
    </head>
    <body>
        <button id="mode-toggle" onclick="toggleMode()">🌓 TOGGLE THEME</button>
        <div class="app-header"><h1>Life++</h1></div>
        <div class="main-grid">
            <div style="display: flex; flex-direction: column; gap: 20px;">
                <div class="panel">
                    <h3>📈 Markets</h3>
                    <div style="display:flex; justify-content:space-between; font-size:14px;"><span>NIFTY 50</span><b style="color:#1e8e3e">22,453</b></div>
                    <div style="display:flex; justify-content:space-between; font-size:14px; margin-top:5px;"><span>USD/INR</span><b>₹83.12</b></div>
                </div>
                <div class="panel">
                    <h3>💰 Expenses</h3>
                    <form action="/api/finance/add" method="POST">
                        <input type="text" name="item" placeholder="Item Name">
                        <input type="number" name="amount" placeholder="Amount (₹)">
                        <button type="submit" class="btn btn-blue" style="width:100%;">Log Expense</button>
                    </form>
                    <div class="scroll-area" style="max-height: 200px; margin-top: 12px;">
                        {% for f in finance %}
                            <div style="font-size:13px; padding:8px 0; border-bottom:1px solid rgba(0,0,0,0.05); display:flex; justify-content:space-between;">
                                <span>{{ f[1] }}</span><b>₹{{ f[2] }}</b>
                            </div>
                        {% endfor %}
                    </div>
                    {% if finance %}
                    <a href="/api/finance/clear" class="clear-link" onclick="return confirm('Clear all expenses?')">🗑 Clear All Expenses</a>
                    {% endif %}
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 20px;">
                <div class="panel">
                    <h3>🍲 Recipe Central</h3>
                    <form action="/api/recipes/add" method="POST">
                        <input type="text" name="title" placeholder="New Dish">
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top:10px;">
                            <select name="meal_type"><option>Breakfast</option><option>Lunch</option><option>Dinner</option></select>
                            <select name="difficulty"><option>Easy</option><option>Medium</option><option>Hard</option></select>
                            <div style="font-size:12px; padding:10px; border:1px solid #ddd; border-radius:8px; background: rgba(255,255,255,0.5);">
                                <label><input type="radio" name="temp" value="Hot" checked> Hot</label><br>
                                <label><input type="radio" name="temp" value="Cold"> Cold</label>
                            </div>
                            <div style="font-size:12px; padding:10px; border:1px solid #ddd; border-radius:8px; background: rgba(255,255,255,0.5);">
                                <label><input type="radio" name="flavor" value="Sweet" checked> Sweet</label><br>
                                <label><input type="radio" name="flavor" value="Spicy"> Spicy</label>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-green" style="margin-top:10px;">Add to Cookbook</button>
                    </form>
                </div>
                <div class="panel">
                    <h3>👨‍🍳 Cookbook</h3>
                    <div class="scroll-area" style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        {% for r in recipes %}
                        <div class="recipe-card">
                            <div style="font-weight:700; font-size:14px;">{{ r[1] }}</div>
                            <div style="font-size:10px; opacity: 0.7; margin-top:4px;">{{ r[2] }} | {{ r[4] }} | {{ r[5] }}</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 20px;">
                <div class="panel">
                    <h3>☁️ Weather India</h3>
                    {% for w in weather %}
                        <div style="font-size:13px; padding:8px 0; border-bottom:1px solid rgba(0,0,0,0.05);">{{ w }}</div>
                    {% endfor %}
                </div>
                <div class="panel">
                    <h3>📝 Notes</h3>
                    <form action="/api/notes/add" method="POST">
                        <textarea name="content" placeholder="Quick note..." style="height: 50px;"></textarea>
                        <button type="submit" class="btn btn-blue" style="width:100%;">Add Note</button>
                    </form>
                    <div class="scroll-area" style="margin-top:15px;">
                        {% for n in notes %}
                        <div class="note-item">
                            <form action="/api/notes/edit/{{ n[0] }}" method="POST">
                                <textarea name="content" style="height:40px; background:transparent; border:none; color:inherit; resize:none; font-size:13px; width:100%;">{{ n[1] }}</textarea>
                                <div style="display:flex; gap:5px; margin-top:5px;">
                                    <button type="submit" class="btn btn-blue" style="flex:1; padding:4px; font-size:11px;">Update</button>
                                    <a href="/api/notes/delete/{{ n[0] }}" class="btn btn-red" style="flex:1; padding:4px; text-decoration:none; text-align:center; font-size:11px;">Delete</a>
                                </div>
                            </form>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        <script>
            function toggleMode() {
                document.body.classList.toggle('dark-mode');
                const isDark = document.body.classList.contains('dark-mode');
                localStorage.setItem('theme', isDark ? 'dark' : 'light');
            }
            if (localStorage.getItem('theme') === 'dark') {
                document.body.classList.add('dark-mode');
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, recipes=recipes, finance=finance, notes=notes, weather=weather_list)

@app.route('/api/finance/add', methods=['POST'])
def add_finance():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO finance (item, amount) VALUES (?, ?)", (request.form['item'], request.form['amount']))
    return redirect(url_for('index'))

@app.route('/api/finance/clear')
def clear_finance():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM finance")
    return redirect(url_for('index'))

@app.route('/api/recipes/add', methods=['POST'])
def add_recipe():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO recipes (title, meal_type, difficulty, temp, flavor) VALUES (?, ?, ?, ?, ?)", (request.form['title'], request.form['meal_type'], request.form['difficulty'], request.form['temp'], request.form['flavor']))
    return redirect(url_for('index'))

@app.route('/api/notes/add', methods=['POST'])
def add_note():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO notes (content) VALUES (?)", (request.form['content'],))
    return redirect(url_for('index'))

@app.route('/api/notes/edit/<int:nid>', methods=['POST'])
def edit_note(nid):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE notes SET content = ? WHERE id = ?", (request.form['content'], nid))
    return redirect(url_for('index'))

@app.route('/api/notes/delete/<int:nid>')
def delete_note(nid):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (nid,))
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
