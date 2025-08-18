# url-shortener
A simple and secure URL shortening service built with Django and Django REST Framework. This project allows users to shorten URLs, optionally protect them with a password, track clicks, and manage expiration.

---

## Features

- **Shorten URLs** with unique hash-based codes.
- **Password protection** for sensitive links (GET without password, POST with password).
- **Expiration dates** for temporary URLs.
- **Click analytics** track total and unique clicks by IP address.
- **Rate limiting** to prevent API abuse.
- **Swagger & ReDoc** documentation for easy API exploration.
- **Testing** The project includes unit and integration tests for models, serializers, views, and API endpoints, ensuring functionality and reliability.

---

## Installation

git clone [https://github.com/OU-G-L/Appoint.git](https://github.com/OU-G-L/url-shortener.git)

cd project-folder

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

---

## Usage

Run the development server **python manage.py runserver**

Access the API **http://localhost:8000/api/swagger/**

---

## Running Tests

You can run tests using Django’s built-in test runner **python manage.py test** or with **pytest** for a more detailed output: pytest.
