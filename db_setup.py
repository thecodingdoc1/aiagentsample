import sqlite3

def create_db():
    
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    table_query = [('''CREATE TABLE IF NOT EXISTS supply_manifest (
                    itemId INTEGER PRIMARY KEY,
                    itemName TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    destination TEXT NOT NULL
                )'''),
                ('''CREATE TABLE IF NOT EXISTS personnel (
                    userId INTEGER PRIMARY KEY,
                    userName TEXT NOT NULL,
                    securityLevel TEXT NOT NULL                   
                )'''),
                ('''CREATE TABLE IF NOT EXISTS vehicleType (
                    vehicleId INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicleType TEXT NOT NULL
                )'''),
                ('''CREATE TABLE IF NOT EXISTS vehicles (
                    vehicleId INTEGER PRIMARY KEY,
                    vehicleType INTEGER NOT NULL,
                    vehicleCapacity INTEGER NOT NULL,
                    FOREIGN KEY (vehicleType) REFERENCES vehicleType(vehicleId)
                )'''),
                ('''CREATE TABLE IF NOT EXISTS vehicle_assignments (
                    assignmentId INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicleId INTEGER NOT NULL,
                    driverId INTEGER NOT NULL,
                    contentsId INTEGER NOT NULL,
                    FOREIGN KEY (contentsId) REFERENCES supply_manifest(itemId),
                    FOREIGN KEY (vehicleId) REFERENCES vehicles(vehicleId),
                    FOREIGN KEY (driverId) REFERENCES personnel(userId)
                )''')]
    
    for query in table_query:
        cursor.execute(query)
    cursor.execute('DELETE FROM supply_manifest')
    cursor.execute('DELETE FROM personnel')
    cursor.execute('DELETE FROM vehicleType')
    cursor.execute('DELETE FROM vehicles')
    cursor.execute('DELETE FROM vehicle_assignments')
    conn.commit()

    personnel_data = [(1, "John Doe", "Driver"),
                       (2, "Jane Smith", "Mechanic"),
                       (3, "Bob Johnson", "Supervisor")]
    cursor.executemany('INSERT INTO personnel VALUES (?,?,?)', personnel_data)

    vehicle_type_data = [(1, "Truck"),
                         (2, "Van"),
                         (3, "Cargo Plane")]
    cursor.executemany('INSERT INTO vehicleType VALUES (?,?)', vehicle_type_data)

    vehicles_data = [(1, 1, 5000),
                     (2, 2, 2000),
                     (3, 3, 10000)]
    cursor.executemany('INSERT INTO vehicles VALUES (?,?,?)', vehicles_data)

    assignments_data = [(1, 1, 1, 1),
                        (2, 2, 2, 2),
                        (3, 3, 3, 3)]
    cursor.executemany('INSERT INTO vehicle_assignments VALUES (?,?,?,?)', assignments_data)

    data = [(1, "Rations", 10, "AFB"),
        (2, "Bunks", 5, "Fort Ridge"), 
        (3, "Beans", 15, "Fort Bridge")]
    
    cursor.executemany('INSERT INTO supply_manifest VALUES (?,?,?,?)', data)
    conn.commit()
    conn.close()

    newconn = sqlite3.connect('logistics.db')
    newcursor = newconn.cursor()
    newcursor.execute('''SELECT * FROM supply_manifest''')
    rows = newcursor.fetchall()
  
    newconn.close()
