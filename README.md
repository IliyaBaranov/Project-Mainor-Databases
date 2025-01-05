# Automated Car Inventory System

## Project Description

The project aims to develop an automated car inventory system for dealerships. The system provides the following functionalities:

- Manage car records with the ability to add, edit, and delete entries.
- Provide a user-friendly interface for managing and filtering information.
- Store and manage data on employees and cars.
- Implement user authentication using password hashing.

## Advantages

- Accelerates the car selection process for clients.
- Automates data management and reduces employee workload.
- Enhances the accuracy of inventory tracking and customer service.
- Fully integrates with the dealership’s local database.

## Technology Stack

- **Database**: SQLite
- **Programming Language**: Python
- **Libraries**:
  - `hashlib` (password hashing)
  - `sqlite3` (SQLite database interaction)
  - `PyQt5` (GUI creation)
  - `json` (JSON data handling)

## Database Structure

### Tables

1. **Marks (Car Brands):**
   - `id` (INTEGER, PRIMARY KEY)
   - `name` (TEXT)
   - `country` (TEXT)

2. **Models (Car Models):**
   - `id` (INTEGER, PRIMARY KEY)
   - `name` (TEXT)
   - `class` (TEXT)
   - `year_from` (INTEGER)
   - `year_to` (INTEGER)
   - `body_type` (TEXT)
   - `mark_id` (INTEGER, FOREIGN KEY)

3. **Generations (Model Generations):**
   - `id` (INTEGER, PRIMARY KEY)
   - `name` (TEXT)
   - `year_start` (INTEGER)
   - `year_stop` (INTEGER)
   - `model_id` (INTEGER, FOREIGN KEY)

4. **Specifications (Car Specifications):**
   - `id` (INTEGER, PRIMARY KEY)
   - `engine_type` (TEXT)
   - `horse_power` (INTEGER)
   - `transmission` (TEXT)
   - `drive` (TEXT)
   - `volume` (REAL)
   - `consumption_mixed` (REAL)
   - `max_speed` (INTEGER)
   - `price` (REAL)
   - `model_id` (INTEGER, FOREIGN KEY)

5. **Employees (Dealership Employees):**
   - `id` (INTEGER, PRIMARY KEY)
   - `name` (TEXT)
   - `login` (TEXT)
   - `password` (TEXT, hashed)

## Installation

1. Install Python version 3.8 or higher.
2. Install dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script to initialize the database.

## Features

- Add, update, and delete car data.
- User authentication using password hashing.
- Filter cars based on specified parameters.
- Manage dealership employee data.

## Potential Improvements

- Add car images.
- Integrate vehicle inspection records.
- Include fields for car color and location.
- Add information about the technical condition of cars.
- Support notes and additional attachments.

## Screenshots

User creation and login

![check1](https://github.com/user-attachments/assets/2d8a1519-2cbc-4c87-bf9c-707b92727afc)

Search functionality

![check2](https://github.com/user-attachments/assets/d584f153-a5b2-4d61-94d4-e0d327b453c4)

Adding a record

![check3](https://github.com/user-attachments/assets/f47be1fd-f3d9-4be2-84e5-ac9119dc68ec)

Editing a record

![check4](https://github.com/user-attachments/assets/504751b8-89c9-4597-9cc5-333e66aeda54)

Deleting a record

![check5](https://github.com/user-attachments/assets/382f5d17-ffa2-4a55-99f9-27176cd43008)

## Developer: *Illia Baranov*
