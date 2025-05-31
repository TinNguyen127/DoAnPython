import json
import os

DATA_DIR = "datarac"
DATA_FILE = os.path.join(DATA_DIR, "HD.JSON")
HOLIDAYS_FILE = os.path.join(DATA_DIR, "holidays.json")

def load_activities():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Lỗi: File {DATA_FILE} không hợp lệ hoặc rỗng. Trả về danh sách rỗng.")
            return []

def save_activities(activities):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(activities, f, ensure_ascii=False, indent=4)

def write_activity(username: str, date: str, content: str, activity_id: str):
    activities = load_activities()
    activities.append({
        "id": activity_id,
        "username": username,
        "date": date,
        "content": content
    })
    save_activities(activities)

def get_all_activities():
    return load_activities()

def get_user_activities(username: str):
    return [act for act in load_activities() if act.get("username") == username]

def update_activity(activity_id: str, new_content: str):
    activities = load_activities()
    updated = False
    for act in activities:
        if act.get("id") == activity_id:
            act["content"] = new_content
            updated = True
            break
    if updated:
        save_activities(activities)
    else:
        raise ValueError(f"Không tìm thấy hoạt động với id = {activity_id}")

def delete_activity(activity_id: str):
    activities = load_activities()
    new_activities = [act for act in activities if act.get("id") != activity_id]
    if len(new_activities) < len(activities):
        save_activities(new_activities)
    else:
        raise ValueError(f"Không tìm thấy hoạt động với id = {activity_id}")

def load_holidays():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(HOLIDAYS_FILE):
        return []
    with open(HOLIDAYS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_holidays(holidays):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(HOLIDAYS_FILE, "w", encoding="utf-8") as f:
        json.dump(holidays, f, indent=4, ensure_ascii=False)

def get_holidays_by_date(date_str: str):
    holidays = load_holidays()
    return [h for h in holidays if h["date"] == date_str]

def get_all_holidays():
    return load_holidays()