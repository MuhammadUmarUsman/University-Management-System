# University Management System

## Description

The **University Management System** is a simple application built using **Python** with **Tkinter** for the GUI and **MySQL** for managing student data. It allows administrators to manage students' information, including adding, updating, and deleting student records. The system also allows running custom SQL queries and retrieving data from the database, such as the students taught by a particular faculty member or the department of a student.

## Features

- **Login Authentication**: Admin login system with hardcoded credentials.
- **Student Management**:
  - Add new students to the system.
  - Delete existing students by student ID.
  - Update student details (e.g., name, GPA).
  - View all students and filter them based on different criteria. 
- **Faculty Information**: List the students taught by a specific faculty member.
- **Department Details**: Retrieve and display the department of a student based on their ID.
- **Custom SQL Query Execution**: Execute custom SQL queries and display results in a table format.
- **Responsive UI**: The GUI adjusts dynamically for various screen sizes.
- **Error Handling**: Basic error handling to ensure smooth interaction.

## Technologies Used

- **Python 3.x**: Programming language used for the application.
- **Tkinter**: Used for building the GUI.
- **MySQL**: Database system for storing and managing student information.
- **PrettyTable**: Python library used to display SQL query results in a tabular format.

## Setup Instructions

### Prerequisites

Ensure that the following tools and libraries are installed:

- **Python 3.x**: Install the latest version of Python from [python.org](https://www.python.org/).
- **MySQL**: Install MySQL database server and create a database for this project.
- **Tkinter**: This library is usually bundled with Python. If not, install it using:

    ```bash
    pip install tk
    ```

- **PrettyTable**: Used to format SQL query results into readable tables. Install it via pip:

    ```bash
    pip install prettytable
    ```

### Database Setup

Set up the database and create necessary tables. Here’s a sample SQL to set up all the tables:
.sql file is provided with all the sql commands to create tables, procedures and triggers used in this project. Create a database in MySql using this file

After setting up the database, make sure to update the connection details (e.g., database name and password) in the script file where the MySQL connection is made.

### Running the Application

1. Clone this repository or download the source code.
2. Ensure that your MySQL database is properly set up and the necessary tables are created.
3. Run the Python script:

    ```bash
    python main.py
    ```

4. Log in with the following credentials (hardcoded):
   - **Username**: `admin`
   - **Password**: `password`

5. Once logged in, the main dashboard will display, giving you access to all the features.
