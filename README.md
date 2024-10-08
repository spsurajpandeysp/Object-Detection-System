
# Object Detection System

A dynamic website with real-time object detection using **YOLO (You Only Look Once)** and neural networks. This project focuses on automated **Car Counting** and **People Counting**. It also includes user-friendly forms for "Contact Us", "Complaints", and "Feedback". Built using **Django** for the backend, **SQL** for database management, and **TensorFlow** with **OpenCV** for image processing, the system provides a seamless user experience across both frontend and backend technologies.


## Interface

| Home Page | Services Page | Object Detection Page | People Counter Page |
|-------------|-------------|---------------------|-----------------------|
| ![Home Page](./readmemedia/homeimage.png) | ![Services Page](./readmemedia/servicesimage.png) | ![Object Detection Page](./readmemedia/objectdetectionimage.png) | ![People Counter Page](./readmemedia/peoplecounterimage.png) |

| Car Counter Page |  About page | Complain Page | Contact Us Page |
|-------------------|------------------------------|----------------------|---------------------------|
| ![Car Counter Page](./readmemedia/carcounterimage.png) | ![About Page](./readmemedia/aboutimage.png) | ![Complain Page](./readmemedia/complainimage.png) | ![Contact Us Page](./readmemedia/contactimage.png) |


## Features
- **Real-time Object Detection**: Identifies and counts cars and people using YOLO.
- **User Forms**: Includes forms for submitting feedback, complaints, and contact information.
- **Responsive Design**: The frontend is designed to provide a smooth experience across devices.
- **Backend Management**: Admin access to handle feedback, complaints, and form submissions.

## Technologies Used
- **Frontend**: HTML, CSS
- **Backend**: Python, Django
- **Database**: SQL
- **Machine Learning**: TensorFlow, YOLO, OpenCV

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/spsurajpandeysp/object-detection-system.git
```

### 2. Navigate to the project directory
```bash
cd object-detection-system
```

### 3. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure the database

Open `AITool/settings.py` and set the database configurations as follows:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'enter database name',
        'USER': 'enter username of database',
        'PASSWORD': 'enter your database password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

### 6. Configure the email server

Also, in `AITool/settings.py`, configure the email server:

```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'enter your email id'
EMAIL_HOST_PASSWORD = 'enter less secure password'
EMAIL_USE_TLS = True
```

### 7. Apply database migrations
```bash
python manage.py migrate
```

### 8. Run the development server
```bash
python manage.py runserver
```

### 9. Access the application

Open your web browser and navigate to:

```
http://127.0.0.1:8000/
```

to access the Object Detection Syste
## Usage

- **Object Detection**:Using Webcam detect object and Upload video to  count cars and people in real time.
- **Forms**: Fill out the "Contact Us", "Complaints", or "Feedback" forms to submit information.
  

---

## Contact
For any inquiries or support, feel free to contact:
- **Name**: [Suraj Pandey]
- **Email**: [surajpandey7493@gmail.com]
- **GitHub**: [https://github.com/spsurajpandeysp](https://github.com/spsurajpandeysp)]
- **My Portfolio**: [https://surajpandey.vercel.app](https://surajpandey.vercel.app)]


🌟 **Thank You for Taking the Time to Explore Our Project!** 🌟
