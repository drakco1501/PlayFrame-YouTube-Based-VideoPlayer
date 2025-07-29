# PlayFrame-YouTube-Based-VideoPlayer
Play Frame is a Django-based video sharing platform that lets users register, create profiles, upload/edit/delete videos, and browse content via a dashboard with random suggestions and search functionality. Sample videos are included for testing and demo.


🚀 Features

- User Registration & Authentication (Login/Logout)
- Profile Creation & Editing
- Video Upload, Edit, and Delete
- Dashboard with Random Video Suggestions
- Video Search Functionality
- Sample videos included in the `videos/` folder

------------------------------------------------------------

🛠️ Setup Instructions

Follow these steps to run the project locally:

1. 📥 Download & Extract

- Download the ZIP file of the repository.
- Extract the files to your desired location.

2. 🐍 Create Virtual Environment

Open terminal/command prompt and navigate to the project folder:

python -m venv env

Activate the environment:

- On Windows:
  env\Scripts\activate

- On Mac/Linux:
  source env/bin/activate

3. 📦 Install Dependencies

pip install -r requirements.txt

4. 🛠️ Apply Migrations

python manage.py makemigrations
python manage.py migrate

5. 👤 Create Superuser

python manage.py createsuperuser

Follow the prompts to set up the admin account.

6. ▶️ Run the Server

python manage.py runserver

Now open your browser and go to:
http://127.0.0.1:8000

------------------------------------------------------------

📁 Additional Notes

- You must create a profile after registering to upload videos.
- Sample videos are available inside the `videos/` folder for testing/demo purposes.

------------------------------------------------------------

🤝 Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

------------------------------------------------------------

📜 License

MIT – Feel free to use and modify for learning or personal projects.
