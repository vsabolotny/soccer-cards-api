# Soccer Cards API

This is a Flask-based API for managing soccer cards and user authentication.

## File Structure

soccer-cards-api/ ├── app/ │ ├── models/ │ │ ├── card.py │ │ ├── user.py │ ├── services/ │ │ ├── card_service.py │ │ ├── auth_service.py │ ├── routes/ │ │ ├── cards.py │ │ ├── auth.py ├── config.py ├── run.py ├── requirements.txt ├── .env ├── README.md

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd soccer-cards-api
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Configure environment variables: Create a .env file in the root directory and add the following:
  ```
  SECRET_KEY=you_should_change_this
  DATABASE_URL=sqlite:///backend/soccer_cards_app.db
  JWT_SECRET_KEY=you_should_change_this
  TEST_JWT_SECRET_KEY=test_jwt_secret_key
  ``` 
## Running the Application
To run the backend application, execute the following command:
```
python run.py
```
The application will start on http://127.0.0.1:5000/.

## API Endpoints
### Cards Endpoints
1. Get All Cards
URL: /cards
Method: GET
Description: Retrieve all cards with optional filters.
Parameters: Query parameters for filtering cards.
Response: JSON list of cards.

2. Add a Card
URL: /cards
Method: POST
Description: Add a new card.
Body: Form data with imageFront, imageBack, and card details.
Response: JSON object of the created card.

3. Get a Card by ID
URL: /cards/<int:card_id>
Method: GET
Description: Retrieve a card by its ID.
Response: JSON object of the card or a 404 error.

4. Delete a Card
URL: /cards/<int:card_id>
Method: DELETE
Description: Delete a card by its ID.
Response: 204 status for success or 404 error.

### Auth Endpoints

1. Login
URL: /login
Method: POST
Description: Authenticate a user and return a JWT access token.
Body: JSON with email and password.
Response: JSON object with access_token or a 401 error.

2. Register
URL: /register
Method: POST
Description: Register a new user.
Body: JSON with email and password.
Response: 201 status for success or 400 error.

3. Protected Route
URL: /protected
Method: GET
Description: Access a protected route (requires JWT token).
Response: JSON message confirming access.

## Notes
Ensure the .env file is properly configured before running the application.
Use tools like Postman or curl to test the API endpoints.
For development, the application runs in debug mode. Disable debug mode in production by setting debug=False in run.py.
