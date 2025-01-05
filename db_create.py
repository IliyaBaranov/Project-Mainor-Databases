import sqlite3
import json
import random

# Load data from the JSON file
with open('base_demo.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Create a connection to SQLite and a cursor
with sqlite3.connect('cars.db') as conn:
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            class TEXT,
            year_from INTEGER,
            year_to INTEGER,
            body_type TEXT,
            mark_id INTEGER,
            FOREIGN KEY (mark_id) REFERENCES Marks(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            year_start INTEGER,
            year_stop INTEGER,
            model_id INTEGER,
            FOREIGN KEY (model_id) REFERENCES Models(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Specifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            engine_type TEXT,
            horse_power INTEGER,
            transmission TEXT,
            drive TEXT,
            volume REAL,
            consumption_mixed REAL,
            max_speed INTEGER,
            price REAL,
            model_id INTEGER,
            FOREIGN KEY (model_id) REFERENCES Models(id)
        )
    ''')

    # Function to insert data
    def insert_data():
        for mark in data:
            # Insert mark and get its id
            cursor.execute(
                'INSERT INTO Marks (name, country) VALUES (?, ?)',
                (mark.get('name'), mark.get('country'))
            )
            mark_id = cursor.lastrowid  # Get the generated id of the mark

            for model in mark.get('models', []):
                # Get body_type from the first generation
                body_type = (
                    model.get('generations', [{}])[0]
                    .get('configurations', [{}])[0]
                    .get('body-type')
                )
                cursor.execute(
                    'INSERT INTO Models (name, class, year_from, year_to, body_type, mark_id) VALUES (?, ?, ?, ?, ?, ?)',
                    (
                        model.get('name'),
                        model.get('class'),
                        model.get('year-from'),
                        model.get('year-to'),
                        body_type,
                        mark_id
                    )
                )
                model_id = cursor.lastrowid  # Get the id of the model

                for generation in model.get('generations', []):
                    cursor.execute(
                        'INSERT INTO Generations (name, year_start, year_stop, model_id) VALUES (?, ?, ?, ?)',
                        (
                            generation.get('name'),
                            generation.get('year-start'),
                            generation.get('year-stop'),
                            model_id
                        )
                    )

                    for configuration in generation.get('configurations', []):
                        for modification in configuration.get('modifications', []):
                            specs = modification.get('specifications', {})
                            random_price = random.randint(20, 500) * 100  # Generate a random price rounded to 100
                            cursor.execute(
                                'INSERT INTO Specifications (engine_type, horse_power, transmission, drive, volume, consumption_mixed, max_speed, price, model_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                (
                                    specs.get('engine-type'),
                                    specs.get('horse-power'),
                                    specs.get('transmission'),
                                    specs.get('drive'),
                                    specs.get('volume'),
                                    specs.get('consumption-mixed'),
                                    specs.get('max-speed'),
                                    random_price,
                                    model_id
                                )
                            )

    # Insert data
    insert_data()
    conn.commit()

print("Data successfully loaded into the database.")
