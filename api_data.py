import requests
import json
import os
from datetime import datetime
from crud import save_holidays, load_holidays

DATA_DIR = "datarac"
HOLIDAYS_FILE = os.path.join(DATA_DIR, "holidays.json")

HOLIDAYS_API_URL = "https://date.nager.date/api/v3/PublicHolidays/{year}/VN"

def get_public_holidays():
    current_year = datetime.now().year
    url = HOLIDAYS_API_URL.format(year=current_year)

    try:
        response = requests.get(url)
        response.raise_for_status() # Gây ra lỗi HTTPError cho các mã trạng thái lỗi
        data = response.json()

        processed_holidays = []
        for h in data:
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
        print("Ngày lễ của năm hiện tại:")
        for h in current_year_holidays:
            print(f"- {h['date']}: {h['localName']}")