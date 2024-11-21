# FastAPI Passwordless Authentication System

A secure, modern passwordless authentication system built with FastAPI and Redis. This system implements magic link-based authentication, providing a secure and user-friendly way to authenticate users without passwords.

## Features

- 🔐 Passwordless Authentication via Magic Links
- 📧 Email-based User Verification
- 🔑 JWT Token-based Session Management
- 🚀 Fast and Async API with FastAPI
- 📦 Redis for Secure Token Storage
- 🐳 Docker and Docker Compose Setup
- 📚 Interactive API Documentation (Swagger UI)

## Technology Stack

- **Backend Framework**: FastAPI
- **Token Storage**: Redis
- **Authentication**: JWT (JSON Web Tokens)
- **Container**: Docker & Docker Compose
- **Email**: SMTP Support (configurable)

## Project Structure

```
fastapi-passwordless-login/
│
├── app/
│   └── main.py          # Main FastAPI application
│
├── docker/
│   └── Dockerfile       # Docker configuration
│
├── requirements.txt     # Python dependencies
├── docker-compose.yml  # Docker Compose configuration
└── README.md          # Project documentation
```

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- Email server (for production)

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-passwordless-login
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Request Login Link
```http
POST /request-login
Content-Type: application/json

{
    "email": "user@example.com"
}
```
Response:
```json
{
    "message": "Magic link sent to your email"
}
```

### 2. Verify Magic Link
```http
GET /verify?token=<magic-link-token>
```
Response:
```json
{
    "access_token": "<jwt-token>",
    "token_type": "bearer"
}
```

### 3. Protected Route Example
```http
GET /protected
Authorization: Bearer <jwt-token>
```
Response:
```json
{
    "message": "Hello user@example.com! This is a protected route."
}
```

## Development Mode Features

- Magic link tokens are printed to the console instead of being sent via email
- Swagger UI available at `/docs` for easy API testing
- Automatic code reload on changes

## Security Features

1. **Token Security**:
   - Magic links expire after 10 minutes
   - Tokens are single-use only
   - Secure token generation using `secrets` module

2. **JWT Security**:
   - Configurable expiration time
   - Signed with a secret key
   - Bearer token authentication

3. **Redis Security**:
   - Tokens stored securely in Redis
   - Automatic token cleanup
   - Isolated container environment

## Production Deployment

For production deployment, make sure to:

1. Set secure environment variables:
   ```env
   SECRET_KEY=your-secure-secret-key
   REDIS_HOST=redis
   REDIS_PORT=6379
   ```

2. Configure email settings in `main.py`:
   ```python
   # Update email configuration
   message.send(
       to=email,
       smtp={
           "host": "smtp.your-server.com",
           "port": 587,
           "user": "your-user",
           "password": "your-password",
           "tls": True
       }
   )
   ```

3. Enable HTTPS in production
4. Update CORS settings for your domain
5. Set appropriate rate limits
6. Use a production-grade Redis configuration

## API Documentation

The API documentation is automatically generated and can be accessed at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
