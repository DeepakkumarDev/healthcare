# healthcare
Healthcare 

create a virtual environmetn first 
To create and activate a virtual environment for your project, follow these steps:

If you are using Windows, 
first create the virtual environment by running 
python -m venv .venv in your terminal.
 Then, activate the virtual environment by running .venv\Scripts\activate. 
 
 If you are using Linux/macOS, first create the virtual environment with
 
python3 -m venv .venv, and then activate it by running source .venv/bin/activate.
Once activated, you can proceed to install project dependencies and run your project within this isolated environment.



Create a file named .env in the root directory (same level as manage.py) and add the following:

# Database Configuration
DB_NAME=your_database_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432





Install Requirements
Make sure you have Python and pip installed. Then run:
pip install -r requirements.txt


Step 4: Apply Migrations
python manage.py makemigrations
python manage.py migrate



Run the Project

python manage.py runserver

Visit:
User Registration
http://127.0.0.1:8000/api/auth/register/

User Login
http://127.0.0.1:8000/api/auth/login/

Current Authenticated User Details
http://127.0.0.1:8000/api/auth/users/



Patient Details
http://127.0.0.1:8000/api/patients/

Doctor Details
http://127.0.0.1:8000/api/doctors/

Mapping between Patients and Doctors
http://127.0.0.1:8000/api/mappings/