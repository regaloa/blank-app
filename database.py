import sqlite3

def create_database():
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        study_date TEXT,
        study_time INTEGER,
        category TEXT,
        problem_name TEXT,
        result TEXT,
        memo TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals(
        id INTEGER PRIMARY KEY,
        goal_problems INTEGER,
        goal_time INTEGER
    )
    """)

    # 初期目標データがない場合のみデフォルト値を挿入
    cursor.execute("SELECT COUNT(*) FROM goals")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO goals (id, goal_problems, goal_time) VALUES (1, 10, 300)")

    conn.commit()
    conn.close()

def save_log(study_date, study_time, category, problem_name, result, memo):
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO study_logs(
        study_date,
        study_time,
        category,
        problem_name,
        result,
        memo
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        str(study_date),
        study_time,
        category,
        problem_name,
        result,
        memo
    ))

    conn.commit()
    conn.close() # 途切れていた接続クローズ処理を修正

def get_statistics():
    """学習ログから合計問題数と総学習時間を取得する"""
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(study_time) FROM study_logs")
    row = cursor.fetchone()
    conn.close()
    
    total_problems = row[0] if row[0] is not None else 0
    total_time = row[1] if row[1] is not None else 0
    return {
        "total_problems": total_problems,
        "total_time": total_time
    }

def get_goal():
    """設定された目標（目標問題数など）を取得する"""
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()
    cursor.execute("SELECT goal_problems, goal_time FROM goals LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "goal_problems": row[0],
            "goal_time": row[1]
        }
    return {
        "goal_problems": 10,
        "goal_time": 300
    }

def get_weak_categories():
    """カテゴリごとに正解率を計算し、低い（苦手な）順にソートして返す"""
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT category, 
           COUNT(*) as total,
           SUM(CASE WHEN result = '○' THEN 1 ELSE 0 END) as correct
    FROM study_logs
    GROUP BY category
    """)
    rows = cursor.fetchall()
    conn.close()
    
    weak_list = []
    for row in rows:
        category = row[0]
        total = row[1]
        correct = row[2]
        accuracy = (correct / total * 100) if total > 0 else 0
        weak_list.append((category, accuracy))
        
    # 正解率の低い順（苦手な順）にソート
    weak_list.sort(key=lambda x: x[1])
    return weak_list
