# Soccer Cards API

This is a simple Flask API for managing soccer cards. The API allows you to add new cards with images and retrieve the list of cards.

## Requirements

- Python 3.6+
- Flask
- Flask-CORS
- Requests (for testing)

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/soccer-cards-api.git
    cd soccer-cards-api
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Ensure the `static` directory exists:
    ```sh
    mkdir -p static
    ```

2. Run the Flask application:
    ```sh
    python app.py
    ```

3. The application will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### GET /

- **Description**: Welcome message.
- **URL**: `/`
- **Method**: `GET`
- **Response**: `Welcome! Use /cards to access the cards endpoint.`

### GET /cards

- **Description**: Retrieve the list of cards.
- **URL**: `/cards`
- **Method**: `GET`
- **Response**: JSON array of cards.

### POST /cards

- **Description**: Add a new card.
- **URL**: `/cards`
- **Method**: `POST`
- **Request**: `multipart/form-data`
  - `name`: Name of the card (optional, default: "Unknown")
  - `imageFront`: Front image of the card (file)
  - `imageBack`: Back image of the card (file)
- **Response**: JSON object of the created card.

## Running Tests

1. Ensure you have the `requests` library installed:
    ```sh
    pip install requests
    ```

2. Run the tests:
    ```sh
    python -m unittest tests.py
    ```

## License

This project is licensed under the MIT License.