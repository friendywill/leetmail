# LeetMail 📧

A minimal, Dockerized LeetCode accountability system that helps groups track
their coding progress together. LeetMail automatically fetches LeetCode progress
for group members and sends email updates to keep everyone motivated and
accountable.

## Features 🚀

- **Progress Tracking**: Automatically fetches LeetCode progress for all group members
- **Email Updates**: Sends formatted progress reports via email using Resend
- **Simple Configuration**: YAML-based user management
- **Secure Updates**: Basic authentication for cron job endpoints
- **Docker Ready**: Easy deployment with Docker

## Prerequisites 📋

- Docker
- Resend API key ([Get one here](https://resend.com))
- LeetCode usernames of group members
- Email addresses for updates

## Quick Start 🏃‍♂️

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/leetmail.git
   cd leetmail
   ```

2. **Set up environment variables**

   ```bash
   cp .env.template .env
   ```

   Edit `.env` with your actual values.

3. **Configure users**
   Edit `config.yml` to add group members:

   ```yaml
   users:
     - leetcode_username: "user1"
       email: "user1@example.com"
     - leetcode_username: "user2"
       email: "user2@example.com"
   ```

4. **Build and run with Docker**

   ```bash
   docker build -t leetmail .
   docker run -p 8000:8000 --env-file .env leetmail
   ```

## API Endpoints 🛠️

### List Users

```bash
GET /users
```

Returns list of registered users and their email addresses.

### Add User

```bash
POST /users
Content-Type: application/json

{
    "leetcode_username": "user1",
    "email": "user1@example.com"
}
```

### Get Progress

```bash
GET /progress
```

Returns current LeetCode progress for all users.

### Trigger Update

```bash
POST /trigger-update
# Requires Basic Authentication
```

Triggers progress check and sends email updates to all users.

## Scheduling Updates ⏰

To schedule regular updates, set up a cron job that calls the trigger endpoint. Example:

```bash
# Run daily at 9 PM
0 21 * * * curl -X POST http://localhost:8000/trigger-update -u $CRON_USERNAME:$CRON_PASSWORD
```

## Email Format 📝

Updates are sent in a clean, readable format:

```txt
LeetCode Progress Update

User: username1
Problems Solved: 125
Current Streak: 7 days
Recent Problems:
- Two Sum
- Valid Parentheses
- ...

User: username2
...
```

## Development

1. **Local Setup**

   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. **Run Development Server**

   ```bash
   python app.py
   ```

3. **Testing API Endpoints**

   ```bash
   # List users
   curl http://localhost:8000/users

   # Add user
   curl -X POST http://localhost:8000/users \
     -H "Content-Type: application/json" \
     -d '{"leetcode_username":"newuser","email":"new@example.com"}'

   # Trigger update
   curl -X POST http://localhost:8000/trigger-update -u admin:your_password
   ```

## Configuration Options ⚙️

### Environment Variables

| Variable       | Description                       | Default  |
| -------------- | --------------------------------- | -------- |
| RESEND_API_KEY | Resend API key for sending emails | Required |
| CRON_USERNAME  | Username for update endpoint auth | admin    |
| CRON_PASSWORD  | Password for update endpoint auth | Required |
| PORT           | Server port                       | 8000     |
| HOST           | Server host                       | 0.0.0.0  |

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments 🙏

- [FastAPI](https://fastapi.tiangolo.com/)
- [Resend](https://resend.com/)
- [Alfa-Leetcode-API](https://alfa-leetcode-api.onrender.com/)
