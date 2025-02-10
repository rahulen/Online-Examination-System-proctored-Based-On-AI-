# Online Examination System (Proctored Based on AI)
![image alt](https://raw.githubusercontent.com/rahulen/Online-Examination-System-proctored-Based-On-AI-/461671e8e47efbfa9543a6e9cbbc82fa9850fb9c/screenshot_1.png)




## Installation Guide

### Step 1: Install Python 3.10
Ensure you have Python 3.10 installed on your system. If not, download and install it from the official Python website: [Python Downloads](https://www.python.org/downloads/)

### Step 2: Edit the Path Variable
After installation, you need to set up the environment variables.

1. Open **System Properties** and navigate to **Advanced System Settings**.
2. Under **System Variables**, find **Path** and click **Edit**.
3. Add the following paths:
   - `C:\Users\gjayk\AppData\Local\Programs\Python\Python311\Scripts\`
   - `C:\Users\gjayk\AppData\Local\Programs\Python\Python311\`
4. Click **OK** to save changes.

### Step 3: Install Required Dependencies
Navigate to your project directory and install the required dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Project
To start the project, execute the following command:

```bash
python manage.py runserver
```
```bash
python .\manage.py runserver              
```

This will start the Django development server. You can access the application at `http://127.0.0.1:8000/` in your browser.

## Additional Notes
- Ensure that all dependencies listed in `requirements.txt` are installed.
- Use a virtual environment for better package management: `python -m venv venv`
- Activate the virtual environment before installing dependencies:
  - On Windows: `venv\Scripts\activate`
  - On macOS/Linux: `source venv/bin/activate`

## Contribution
Feel free to fork this repository and submit pull requests with improvements!

## License
This project is open-source and licensed under the MIT License.

