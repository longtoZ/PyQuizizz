# About PyQuizizz

- This project automatically gets full questions, options and answers for each Quizizz link. It also allows you to search for keywords and download the table as *.csv* file.
- Demo video [here](https://drive.google.com/file/d/1oIElxsZWVVzzJ8ujdArjv_fNPrD-8lEA/view?usp=sharing).


# Libraries/Modules

**1. Backend:**
- Flask
- Selenium
- Javascript

**2. Frontend:**
- HTML, CSS

# Setup & Installation

**1. Clone the repository to your local device.**
```
git clone https://github.com/longtoZ/PyQuizizz.git
```

**2. Create virtual environment for the app (recommended).**
```
pip install virtualenv
```

- Go to the app directory.
```
virtualenv venv
```

- Activate virtual environment (Windows).
```
venv\Scripts\activate
```

**3. Install required libraries.**
```
pip install -r requirements.txt
```

**4. Run the app**
- Change this line in `main.py` to `driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)`
```
python main.py
```

**5. View the app**

- Go to `http://127.0.0.1:5000`
