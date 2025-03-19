# Ride-Sharing Service Backend

A simplified ride-sharing backend service built with Python and OpenStreetMap integration.

## 📌 Overview

This project demonstrates:
* **Code Versioning** - Using Git for version control
* **Algorithm Design** - Implementing a ride-matching algorithm based on distance
* **API Integration** - Fetching real-time driver locations from OpenStreetMap
* **Code Deployment** - Docker containerization for easy deployment

## 🚀 Features

✅ **Ride-Matching Algorithm** - Assigns the nearest driver to a rider using the Haversine formula
✅ **Real-Time Geolocation** - Integrates with OpenStreetMap for geocoding and routing
✅ **Dockerized** - Complete Docker setup for easy deployment
✅ **REST API Endpoints** - API for requesting rides, listing drivers, and tracking rides

## 📂 Project Structure

```
📦 ride-sharing-backend
├── 📂 src
│   ├── 📄 app.py - Main application and API endpoints
│   ├── 📄 matching.py - Ride-matching algorithm
│   ├── 📄 api.py - OpenStreetMap API integration
│   ├── 📄 config.env - Environment variables
├── 📂 tests - Unit and integration tests
├── 📄 Dockerfile - Containerization setup
├── 📄 docker-compose.yml - Local development setup
├── 📄 .github/workflows/ci-cd.yml - CI/CD pipeline
├── 📄 README.md - Documentation
```

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/ride-sharing-backend.git
cd ride-sharing-backend
```

### 2️⃣ Set Up Environment Variables

Create a `.env` file in the root directory:

```
PORT=8080
API_KEY=your_api_key_here
```

### 3️⃣ Run with Docker

```bash
docker-compose up --build
```

### 4️⃣ Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python src/app.py
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/request-ride` | Request a ride, match with driver |
| GET | `/drivers` | List available drivers |
| GET | `/ride-status/:id` | Track an ongoing ride |
| POST | `/complete-ride/:id` | Mark a ride as completed |

### Example Request:

```bash
curl -X POST "http://localhost:8080/request-ride" \
  -H "Content-Type: application/json" \
  -d '{"lat": 40.7128, "lon": -74.0060}'
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_matching.py
```

## 🌍 Deployment

### Deploy with Docker

1. Build the Docker image:
```bash
docker build -t ride-sharing-backend .
```

2. Tag and push to a container registry:
```bash
docker tag ride-sharing-backend your-registry/ride-sharing-backend
docker push your-registry/ride-sharing-backend
```

3. Deploy to your cloud platform of choice (AWS, GCP, Azure, etc.)

## 📝 License

This project is licensed under the MIT License