**📈 StockAlert:  Personalized Stock Analysis Dashboard**

**Welcome to  my StockAlert project , a dynamic web application designed to help you keep an eye on the Indian stock market. This project offers a clean, interactive interface to analyze stock performance, track significant price changes, and even receive email alerts for big market movements.
Even if  you're a seasoned investor or just curious about stock trends, StockAlert provides a user-friendly experience with powerful features.**

------------------IMAGES-----------------------------------------------------------------------
![PROJECT IMAGE 0](https://github.com/user-attachments/assets/6b88e259-e0bc-4bae-8df7-1c9b2c9cff47)
![PROJECT IMAGE 8](https://github.com/user-attachments/assets/9c23bcd2-c4fb-4883-853c-e8309513d1bb)
![PROJECT IMAGE 7](https://github.com/user-attachments/assets/11da492e-5cdb-4e57-a42d-773b750d6b06)
![PROJECT IMAGE 6](https://github.com/user-attachments/assets/5b169919-fb92-4d0d-9a40-09a319959977)
![PROJECT IMAGE 5](https://github.com/user-attachments/assets/bbc6b48f-1f08-4dea-be16-ca83aa00754c)
![PROJECT IMAGE 4](https://github.com/user-attachments/assets/4a42491c-5ecc-457a-ad5a-8f68432037bb)
![PROJECT IMAGE 3](https://github.com/user-attachments/assets/f4cb9ff5-6f1e-4f33-8786-f25c6634b2a7)
![PROJECT IMAGE 2](https://github.com/user-attachments/assets/c40446b9-f91d-4f85-ad37-290223235feb)
![PROJECT IMAGE 1](https://github.com/user-attachments/assets/2c1ed68c-418e-4a56-8f13-38b2b085063c)



----------------------- Key Features :----------------------------------------
* User Authentication: Securely register and log in to your personalized dashboard. Your preferences are saved just for you!
* Interactive Candlestick Charts: Visualize stock price movements over time with professional, interactive candlestick charts powered by Plotly.js. Zoom, pan, and explore data with ease.
* Stock Performance Analysis: Get quick insights into daily stock changes for a selection of top Indian companies.
* Customizable Date Ranges: Choose specific periods to analyze historical stock data.
* Personalized Email Alerts: Opt-in to receive email notifications if a stock you're analyzing experiences a significant price change (5% or more).
* Dark/Light Mode: Switch between dark and light themes to suit your viewing preference, saved automatically to your profile.
* Company Logos: See familiar company logos displayed alongside your analysis for a better visual experience.
* CLI Demo: A separate route to demonstrate the core stock analysis logic as if it were run from a command-line interface.

---------------------- Technologies Used :--------------------------------------

Backend:

* Python 3: Core programming language.

* Flask:  Web framework for handling routes, requests, and serving templates.

* yfinance: Library to fetch real-time and historical market data from Yahoo! Finance.

* Firebase Admin SDK: For secure user authentication and storing user preferences in Firestore.

* python-dotenv: To manage environment variables securely.

* smtplib: Python's built-in library for sending email alerts.

Frontend:

* HTML5: Structure of the web pages.

* Tailwind CSS: Framework for rapid and responsive UI development.

* JavaScript: For dynamic content, AJAX requests, and client-side interactivity.

* Plotly.js:  JavaScript graphing library for creating interactive candlestick charts.

Database:

* Google Cloud Firestore: A flexible, scalable NoSQL cloud database for storing user accounts and preferences.
Setup and install it 

------------------------- Configure Environment Variables------------------------------------------------------


* Create a file named .env in the root of your project directory (the same level as app.py) and add the following, replacing the placeholder values:

FIREBASE_SERVICE_ACCOUNT_PATH=/full/path/to/your-project-id-firebase-adminsdk-xxxxx-xxxxxx.json
FIREBASE_API_KEY=YOUR_WEB_API_KEY_FROM_FIREBASE_CONSOLE
FLASK_SECRET_KEY=a_very_long_and_random_secret_key_for_flask_sessions

FIREBASE_SERVICE_ACCOUNT_PATH: The full path to the JSON file you downloaded above .

FIREBASE_API_KEY: The apiKey you copied in previous step

FLASK_SECRET_KEY: Generate a strong, random string for this (e.g., import os; print(os.urandom(24).hex()) in a Python console). This is important  for Flask session security.

-------------------Project Structure-------------------------------------------


Ensure your project directory looks like this:

your-project-directory/
├── .env
├── app.py(for web)
├── main.py(if you want it to run it simple CLI)
├── stocks.py
├── sendmail.py
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   └── cli_output.html
└── static/
    └── charts/ (This directory will be created by the app, but no images saved here anymore)
    ├── Logos/(This directory contains the logos.png .ADD all the png here)
   
  
  

------------------------. Run the Application--------------------------------------
From your terminal, navigate to the project directory and run the Flask application:

python app.py

The application should start, and you'll see a message indicating the URL (e.g., http://127.0.0.1:5000  )

 ----------------------------------Usage--------------------------------------------------------

1. Access the App: Open your web browser and go to the URL provided by Flask (e.g., http://127.0.0.1:5000/).
2. Register/Login: You'll be redirected to the login page. If you're a new user, register an account.
3. Analyze Stocks: Once logged in, select a company and a date range. Click "Analyze Stock" to see the performance message and an interactive candlestick chart.
4. Manage Preferences: In the "User Preferences" section, you can:
5. Toggle between Dark and Light mode.
6. Enable email alerts by providing your email address and an App Password (highly recommended for Gmail users with 2FA enabled).
7. Save your preferences.
8. CLI Demo: Click "Run CLI Demo" to see a simulated command-line output of the stock analysis.



----------------------------------- Contribution :---------------------------------------------------
Feel free to fork this repository, open issues, or submit pull requests. Any contributions are welcome!

