# Climb Tracker backend

A Django REST API for private climbing logs. It contains no frontend.

## Included

- Account registration, JWT sign-in/refresh, profile retrieval and update, and permanent account deletion
- Django's built-in password hashing and per-password salts; plaintext passwords are never stored
- Private user-owned climb records with V, YDS, French, UIAA, and Fontainebleau grades
- Private photo uploads (10 MB per image) and per-photo deletion
- A Django admin feature toggle to enable or disable all photo uploads immediately
- A chart-ready progress endpoint that returns successful climbs grouped by date and grade system
- SQLite for local development, with PostgreSQL configuration support for production
- Admin management, rate limiting, production security headers, and a Docker image

## Local setup

Install Python 3.12 or later, then from this folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API will run at `http://127.0.0.1:8000`. Its admin console is at `/admin/`.

The frontend is served from the root URL at `http://127.0.0.1:8000/`. It supports registration, sign-in, logging attempts, a responsive month/week calendar, and progress stats. It uses the same-origin API, so no separate frontend server or CORS configuration is needed for local development. Account email collection is controlled by `REQUIRE_ACCOUNT_EMAIL` and is off by default. Passwords must be at least 6 characters.

For a container deployment, copy `.env.example` to `.env`, set production values, then run:

```powershell
docker compose up --build
```

## API

All API responses are JSON. For protected endpoints, send `Authorization: Bearer <access-token>`.

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/auth/register/` | Create an account. Requires `username`, `email`, `password` (12+ characters). |
| POST | `/api/auth/login/` | Get `access` and `refresh` JWTs using `username` and `password`. |
| POST | `/api/auth/refresh/` | Exchange a refresh token for a new access token. |
| GET/PATCH | `/api/auth/me/` | Fetch or update the signed-in user’s profile. |
| DELETE | `/api/auth/delete/` | Permanently delete the signed-in account and its climbs/photos. |
| GET/POST | `/api/climbs/` | List or add the user’s climbs. |
| GET/PATCH/DELETE | `/api/climbs/{id}/` | Retrieve, edit, or delete one of the user's climbs. |
| POST | `/api/climbs/{id}/photos/` | Upload multipart `image` and optional `caption`. |
| DELETE | `/api/climbs/{id}/photos/{photo_id}/` | Remove one photo. |
| GET | `/api/climbs/progress/?grade_system=V` | Chart series by date; grade system filter is optional. |
| GET | `/api/climbs/features/` | Feature availability for the signed-in user, including `photo_uploads_enabled`. |

## Managing photo uploads

Create a Django superuser during setup, then sign in at `/admin/`. Open **Feature settings** and clear **Photo uploads enabled** to disable future uploads site-wide. The API returns `403 Forbidden` for uploads while disabled. Existing photos remain available to their owners.

Example climb body:

```json
{
  "climbed_on": "2026-10-05",
  "name": "Midnight Lightning",
  "location": "Camp 4",
  "discipline": "boulder",
  "grade_system": "V",
  "grade": "V8",
  "attempts": 4,
  "sent": true,
  "notes": "Cool morning conditions."
}
```

## Production checklist

1. Use a maintained VPS provider and Ubuntu LTS. Point DNS to Cloudflare, enable proxying, and configure Cloudflare's SSL/TLS mode as Full (strict). Do not expose the origin IP publicly; restrict the VPS firewall to SSH, plus web traffic only from Cloudflare IP ranges.
2. Set a strong `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, exact `DJANGO_ALLOWED_HOSTS`, and exact `DJANGO_CORS_ALLOWED_ORIGINS`. Keep `.env` outside version control.
3. Use managed PostgreSQL or a regular backed-up PostgreSQL instance. SQLite is intentionally supported for local/small deployments, but is not suitable for concurrent production traffic.
4. Store images in object storage (Cloudflare R2, S3, or similar) and keep bucket access private. Add image processing and malware scanning before a public launch.
5. Terminate HTTPS at Cloudflare or a reverse proxy, run migrations before releases, back up the database and media, and test restoration.
6. Use Cloudflare rate limiting/WAF rules for `/api/auth/login/` and `/api/auth/register/`. The app also has application-level request throttles.

## California privacy operations

The API supports access through `GET /api/auth/me/` and `GET /api/climbs/`, and deletion through `DELETE /api/auth/delete/`. Before collecting production data, publish a privacy notice that identifies what is collected, why it is used, retention periods, service providers, and how a California resident can make access/deletion/correction requests. Verify the requester before fulfilling a request, record requests and outcomes, and ensure storage/CDN vendors are contractually restricted to service-provider use. Obtain legal review for the notice and workflow before launch; requirements depend on the business and data volume.

