# -*- coding: utf-8 -*-
"""
Created on Sat May 31 12:44:08 2025

@author: bingu
"""

import requests
import json
import os
from datetime import datetime


DATA_DIR = "datarac"
HOLIDAYS_FILE = os.path.join(DATA_DIR, "holidays.json")


HOLIDAYS_API_URL = "https://date.nager.date/api/v3/PublicHolidays/{year}/VN"

def load_holidays():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(HOLIDAYS_FILE):
        return []
    with open(HOLIDAYS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Lỗi: File {HOLIDAYS_FILE} không hợp lệ hoặc rỗng. Trả về danh sách rỗng.")
            return []

def save_holidays(holidays):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR) # Đảm bảo thư mục tồn tại
    with open(HOLIDAYS_FILE, "w", encoding="utf-8") as f:
        json.dump(holidays, f, indent=4, ensure_ascii=False)

def get_public_holidays(year=None):
    if year is None:
        year = datetime.now().year

    url = HOLIDAYS_API_URL.format(year=year)
    print(f"Đang lấy ngày lễ từ API: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        holidays_data = response.json()
        processed_holidays = []
        for h in holidays_data:
            processed_holidays.append({
                "date": h["date"],
                "name": h["name"],
                "localName": h["localName"]
            })
        
        print(f"Đã lấy được {len(processed_holidays)} ngày lễ từ API.")
        save_holidays(processed_holidays)
        return processed_holidays
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi lấy dữ liệu ngày lễ từ API (có thể do mạng hoặc API không phản hồi): {e}")
        current_holidays = load_holidays()
        if current_holidays:
            print("Đang sử dụng dữ liệu ngày lễ đã lưu trữ trước đó.")
        return current_holidays
    except json.JSONDecodeError as e:
        print(f"Lỗi phân tích JSON từ API (phản hồi không phải JSON hợp lệ): {e}")
        current_holidays = load_holidays()
        if current_holidays:
            print("Đang sử dụng dữ liệu ngày lễ đã lưu trữ trước đó.")
        return current_holidays
    except Exception as e:
        print(f"Lỗi không xác định khi lấy ngày lễ: {e}")
        current_holidays = load_holidays()
        if current_holidays:
            print("Đang sử dụng dữ liệu ngày lễ đã lưu trữ trước đó.")
        return current_holidays

if __name__ == "__main__":
    current_year_holidays = get_public_holidays()
    if current_year_holidays:
        print("\nNgày lễ năm hiện tại:")
        for h in current_year_holidays:
            print(f"  {h['date']}: {h['localName']} ({h['name']})")
    else:
        print("Không thể tải ngày lễ.")