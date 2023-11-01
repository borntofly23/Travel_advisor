# Travel Advisor

Travel Advisor is a Flask-based web application that provides travel-related information to users, including flights, weather, hotels, and attractions. It integrates various APIs to deliver a comprehensive travel experience.

## Features

- **User Authentication**: Provides user registration and login functionalities. Utilizes password hashing for security and token-based authentication for protected routes.

- **API Integration**: Makes use of various external APIs to fetch travel data, including flights, weather information, hotels, and nearby attractions.

- **Data Storage**: Utilizes MongoDB to store user information and location details for efficient retrieval.

## Prerequisites

Before running the application, ensure you have the following:

- Python installed
- Required Python packages: Flask, pymongo, requests, jwt
- MongoDB installed and running
- API keys for RapidAPI services (flight, weather, hotel, attractions) and MongoDB connection string

## Installation and Setup

1. Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2. Install required Python packages:

    ```bash
    pip install flask pymongo requests
    ```

3. Set up MongoDB and configure the connection string in the Flask app.

4. Obtain API keys for the external services and update the corresponding keys in the Flask app.

## Running the Application

1. Navigate to the project directory:

    ```bash
    cd Travel_Advisor
    ```

2. Run the Flask application:

    ```bash
    python app.py
    ```

3. Access the application through a web browser at `http://localhost:5000` or the specified port.

## Usage

- Register as a new user or log in with existing credentials.
- Navigate to the Home page to search for travel details by providing a location.
- View the fetched flight, weather, hotel, and attraction information on the details page.

## Contributors

- Rushikesh Jadhav (https://github.com/borntofly23)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Mention any external libraries, APIs, or resources used in the project.
- Attribute credits to the APIs and services used for fetching travel data.

---

This README template provides a structured overview of the Travel Advisor Flask application, including its features, prerequisites, installation, usage guidelines, contributors, license information, and acknowledgments. Go through requirements.txt if still any library is missing.
