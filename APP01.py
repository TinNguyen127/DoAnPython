import tkinter as tk
from tkinter import messagebox, ttk
from crud import update_activity, delete_activity, write_activity, get_all_activities, get_user_activities
from account import register_user, login_user, ensure_admin_exists
import uuid
from datetime import datetime
from tkcalendar import Calendar, DateEntry
from api_data import get_public_holidays
from crud import get_all_holidays, save_holidays
import os

class DailyApp:
    def __init__(self, root):
        if not os.path.exists("datarac"):
            os.makedirs("datarac")
            
        ensure_admin_exists()
        self.root = root
        self.root.title("Ứng dụng Quản lý Sinh hoạt Hằng ngày")
        self.root.geometry("900x700")

        self.current_user = None
        self.current_role = None
        self.holidays = []

        self.create_widgets()
        self.login_window()
        
    def load_holidays_data(self):
        print("Đang tải dữ liệu ngày lễ...")
        if not os.path.exists("datarac"):
            os.makedirs("datarac")
            
        self.holidays = get_all_holidays()
        if not self.holidays or datetime.now().year not in [datetime.strptime(h['date'], '%Y-%m-%d').year for h in self.holidays]: 
            messagebox.showinfo("Thông báo", "Đang tải dữ liệu ngày lễ từ Internet. Vui lòng đợi...", parent=self.root)
            self.holidays = get_public_holidays()
            save_holidays(self.holidays)
        
        if hasattr(self, 'cal'):
            self.update_calendar_highlights()
        print("Đã tải xong dữ liệu ngày lễ.")

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.main_frame, text="Chào mừng đến với Ứng dụng Quản lý Sinh hoạt", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.calendar_frame = tk.Frame(self.notebook)
        self.activities_frame = tk.Frame(self.notebook)

        self.notebook.add(self.calendar_frame, text="Lịch & Ngày lễ")
        self.notebook.add(self.activities_frame, text="Hoạt động hằng ngày")
        
        self.create_calendar_tab()
        self.create_activities_tab()

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)


    def create_calendar_tab(self):
        self.cal = Calendar(self.calendar_frame, selectmode='day',
                           font="Arial 12",
                           locale='vi_VN',
                           headersfont="Arial 12 bold",
                           weekendbackground='lightgray',
                           othermonthforeground='gray',
                           normalbackground='white',
                           foreground='black',
                           selectbackground='blue',
                           selectforeground='white',
                           showweeknumbers=False)
        self.cal.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.cal.bind("<<CalendarSelected>>", self.show_selected_date_activities)
        
        self.selected_date_label = tk.Label(self.calendar_frame, text="Chọn một ngày trên lịch để xem hoạt động và ngày lễ.", font=("Arial", 10))
        self.selected_date_label.pack(pady=5)

        self.date_info_text = tk.Text(self.calendar_frame, height=8, width=50, font=("Arial", 10), wrap=tk.WORD)
        self.date_info_text.pack(pady=5, padx=10, fill=tk.X, expand=False)
        self.date_info_text.config(state=tk.DISABLED)

    def update_calendar_highlights(self):
        self.cal.calevent_remove('all')
        
        for holiday in self.holidays:
            try:
                h_date = datetime.strptime(holiday["date"], "%Y-%m-%d").date()
                self.cal.calevent_create(h_date, holiday["localName"], 'holiday_tag')
            except ValueError:
                continue
        self.cal.tag_config('holiday_tag', background='lightblue', foreground='red', borderwidth=1, relief="raised")
        
        if self.current_user:
            user_activities = get_user_activities(self.current_user)
            activity_dates = set()
            for act in user_activities:
                activity_dates.add(act["date"])
            
            for date_str in activity_dates:
                try:
                    a_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if not self.cal.calevent_cget(a_date, tag="holiday_tag"):
                        self.cal.calevent_create(a_date, "Có hoạt động", 'activity_tag')
                except ValueError:
                    continue
        self.cal.tag_config('activity_tag', background='lightgreen', foreground='darkgreen', borderwidth=1, relief="ridge")


    def show_selected_date_activities(self, event=None):
        selected_date = self.cal.selection_get()
        date_str = selected_date.strftime("%Y-%m-%d")
        self.selected_date_label.config(text=f"Hoạt động và ngày lễ cho ngày: {date_str}")
        
        self.date_info_text.config(state=tk.NORMAL)
        self.date_info_text.delete(1.0, tk.END)

        holidays_on_selected_date = [h for h in self.holidays if h["date"] == date_str]
        if holidays_on_selected_date:
            self.date_info_text.insert(tk.END, "--- NGÀY LỄ ---\n")
            for h in holidays_on_selected_date:
                self.date_info_text.insert(tk.END, f"- {h['localName']} ({h['name']})\n")
            self.date_info_text.insert(tk.END, "\n")
        
        activities_on_selected_date = []
        if self.current_user:
            activities_on_selected_date = [
                act for act in get_user_activities(self.current_user)
                if act["date"] == date_str
]