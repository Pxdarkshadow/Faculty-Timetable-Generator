Faculty Timetable Generator

Overview
The Faculty Timetable Generator is a Django-based web application designed to streamline the process of creating, managing, and distributing faculty schedules in educational institutions. It allows administrators to efficiently generate, customize, and manage weekly timetables for faculty members, ensuring optimal use of resources and reducing scheduling conflicts.

# Key Features
- User Authentication: Secure login and sign-up for administrators and faculty members with role-based access control.
- Dynamic Timetable Generation: Generate and manage timetables for a 5-day schedule (Monday to Friday) from 9 AM to 5 PM.
- Customizable Inputs: Add details such as teacher names, departments, subjects, class types (lecture, lab), and time slots, along with breaks.
- Interactive Management: Edit, delete, and regenerate timetables with an intuitive interface.
- PDF Export: Easily export timetables to PDF format for printing or sharing.
- Responsive Design: A user-friendly and interactive UI that works seamlessly across devices.

# Technologies Used
- Backend: Django (Python)
- Frontend: HTML, CSS
- Database: SQLite3
- PDF Generation: ReportLab 
- Authentication: Django's built-in authentication system

# Installation and Setup
Prerequisites
- Python 3.x
- Django 5.1
- MySQL

# Step-by-Step Guide
1. Clone the Repository:
    ```bash/cmd
    git clone https://github.com/Pxdarkshadow/faculty-timetable-generator.git
    cd faculty-timetable-generator
   ```

3. Create and Activate a Virtual Environment:
    ```bash/cmd
    python -m venv venv
    venv\Scripts\activate
    ```

4. Install Dependencies:
    ```bash/cmd
    pip install -r requirements.txt
    ```

5. Apply Migrations:
    ```bash/cmd
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Create a Superuser:
    ```bash/cmd
    python manage.py createsuperuser
    ```
    then enter your details accordingly

7. Run the Development Server:
    ```bash
    python manage.py runserver
    ```

8. Access the Application:
   - Open your browser and copy the link in bash/cmd

# Usage
- Admin Panel: Access the admin panel at `/admin` for managing users and schedules.
-*Timetable Management: Use the dashboard to generate, edit, or delete timetables.
- Export to PDF: Click the "Download PDF" button to download a printable version of the timetable.

# Future Enhancements
- Automated Conflict Detection: Highlight scheduling conflicts automatically.
- Email Notifications: Notify faculty members of their schedules via email.
- ML Integration: Integrating an ML model which will take student timetable as input. It will then segregate all the lectures and insert it in faculty's timetable accordingly.

# Contributing
Contributions are welcome! Please open an issue or submit a pull request if you'd like to contribute to this project.

# Contact
For any inquiries or support, please contact:
- Name: Shaun
- Email: shaunmat13@gmail.com
- Phone: 9820717161
P.S: i prolly won't pick up cuz I'll be busy playing Valorant.
