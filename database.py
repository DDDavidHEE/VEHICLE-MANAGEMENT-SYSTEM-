import sqlite3

DB_NAME = "vehicles.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Xóa bảng nếu đã tồn tại để tránh lỗi cột không tìm thấy
    cursor.execute('DROP TABLE IF EXISTS vehicles')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT NOT NULL,
            vehicle_type TEXT NOT NULL,
            brand TEXT NOT NULL,
            owner TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Hàm lấy tất cả phương tiện
def get_all_vehicles():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles

# Thêm phương tiện
def add_vehicle(license_plate, vehicle_type, brand, owner, registration_date, phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vehicles (license_plate, vehicle_type, brand, owner, registration_date, phone) VALUES (?, ?, ?, ?, ?, ?)", 
                   (license_plate, vehicle_type, brand, owner, registration_date, phone))
    conn.commit()
    conn.close()

# Xóa phương tiện
def delete_vehicle(vehicle_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
    conn.commit()
    conn.close()

# Cập nhật phương tiện
def update_vehicle(vehicle_id, license_plate, vehicle_type, brand, owner, registration_date, phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE vehicles
        SET license_plate = ?, vehicle_type = ?, brand = ?, owner = ?, registration_date = ?, phone = ?
        WHERE id = ?
    ''', (license_plate, vehicle_type, brand, owner, registration_date, phone, vehicle_id))
    conn.commit()
    conn.close()
