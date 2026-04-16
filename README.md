# Bot-intraday

# SeaTalk Bot Server

Lightweight bot server for SeaTalk with this capture flow:

1. check whether new non-blank values appeared in `F7:AC7`
2. export the configured Google Sheets capture range to PDF
3. convert PDF to PNG with Poppler
4. trim, optimize, sharpen, and enhance PNG with ImageMagick
5. send a single interactive message card to the SeaTalk group only when new values are detected
6. repeat on the configured `BOT_INTERVAL_MINUTES`

## Message format

Each send posts one interactive message card:

```text
[Interactive Message]
Title: SOC 5 OTP Hourly Update as of Apr-16 9:30 AM
Description: FMS Latest Update: Apr-16 9:00 AM - Completed
Image: rendered report snapshot
Button: View Report Link
```

## Config

The app reads the existing local `.env` file format directly:

```text
sheet_id: <google-sheet-id>
tab_name: otp_hourly
seatalk_webhook_url: <seatalk-webhook-url>
capture_range: B2:M30
report_link: <google-sheet-report-link>
```

Optional settings:

```text
BOT_HOST=0.0.0.0
BOT_PORT=8080
BOT_INTERVAL_MINUTES=60
BOT_TIMEZONE=Asia/Manila
BOT_REQUEST_TIMEOUT_SECONDS=30
BOT_RUN_ON_STARTUP=false
BOT_PDF_DPI=400
BOT_IMAGE_BORDER_PX=20
BOT_IMAGE_RESIZE_WIDTH=2200
BOT_USE_ENV_PROXY=false
GOOGLE_SERVICE_ACCOUNT_FILE=google-service-account.json
```

Use `.env.example` as the committed template and keep real values only in your local `.env`.

The service stores the last seen `F7:AC7` snapshot in `.runtime/seatalk-watch-state.json` so it can suppress duplicate sends across polling cycles and restarts.

## Docker

Build the image:

```powershell
docker build -t seatalk-bot .
```

Run the container:

```powershell
docker run -d --name seatalk-bot `
  -p 8080:8080 `
  -v ${PWD}/.env:/app/.env:ro `
  -v ${PWD}/google-service-account.json:/app/google-service-account.json:ro `
  seatalk-bot
```

Stop and remove the container:

```powershell
docker rm -f seatalk-bot
```

`docker-compose.yml` is included if you want a compose-based start command on a machine that has Compose installed.

## Endpoints

- `GET /` or `GET /healthz`: current service status
- `POST /trigger`: manual run that sends the current snapshot immediately

## Notes

- The container image installs both `poppler-utils` and `imagemagick`.
- The Google service account must have access to the target spreadsheet.
- Render deployment steps are documented in [docs/render_web_service_deployment.md](docs/render_web_service_deployment.md).
- UptimeRobot setup steps are documented in [docs/uptimerobot_setup.md](docs/uptimerobot_setup.md).
