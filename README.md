# Soccer Cards App Backend

This project is a backend application for managing soccer cards, built using Flask. It provides functionalities for user authentication, card scanning, saving, and displaying a list of saved cards with filtering options.

## Features

- User authentication (login and registration)
- Upload and save soccer card images
- Retrieve and display a list of saved soccer cards
- Filter cards by date and player name

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Initializes the Flask app instance
│   ├── routes/               # Contains route definitions
│   │   ├── __init__.py      # Initializes the routes module
│   │   ├── auth.py          # Authentication routes
│   │   └── cards.py         # Card management routes
│   ├── models/               # Contains data models
│   │   ├── __init__.py      # Initializes the models module
│   │   ├── user.py          # User model definition
│   │   └── card.py          # Card model definition
│   ├── services/             # Contains business logic
│   │   ├── __init__.py      # Initializes the services module
│   │   ├── auth_service.py   # User authentication logic
│   │   └── card_service.py    # Card data handling logic
│   └── static/               # Directory for static files (e.g., images)
├── run.py                    # Entry point for running the application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation for the backend
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd soccer-cards-app/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the backend application, execute the following command:
```
python run.py
```

The application will start on `http://127.0.0.1:5000/`.

## API Endpoints

- `POST /auth/login`: User login
- `POST /auth/register`: User registration
- `GET /cards`: Retrieve all saved cards
- `POST /cards`: Add a new soccer card

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.