# Airline Management API

This API provides functionality for managing airline operations, including flights, routes, airports, crew, tickets, orders, airplanes, and airplane types. It is built with Django and Django REST Framework and includes comprehensive OpenAPI documentation using DRF Spectacular.

---

## Features

- Manage flights, routes, airports, and airplanes.
- Handle orders, tickets, and crew details.
- Optimize queries with `select_related` and `prefetch_related` for better performance.
- Calculate available and taken seats dynamically.
- Detailed API schema documentation.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/airline-management-api.git
   cd airline-management-api
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the API**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

---

## Additional Notes

- Use `python manage.py createsuperuser` to create an admin user for the Django admin panel.
- The OpenAPI schema is available at `/schema/` (adjustable in the settings).