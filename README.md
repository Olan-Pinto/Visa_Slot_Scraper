# Visa Slot Checker

Automatically checks for Abu Dhabi visa appointment slots every 15 minutes and sends email + SMS notifications when slots become available.

## Features

- 🔄 Runs automatically every 15 minutes via GitHub Actions
- 📧 Email notifications when slots open up
- 📱 SMS notifications via Twilio
- 💾 Tracks state between runs to avoid duplicate alerts
- 🆓 Free to run (within GitHub Actions free tier)

## Setup Instructions

### 1. Create a GitHub Repository

1. Create a new repository on GitHub (can be private)
2. Clone it to your local machine
3. Copy these files into the repository:
   - `check_visa_slots.py`
   - `.github/workflows/check_visa_slots.yml`
   - `last_state.json`
   - `requirements.txt`
   - `README.md`

### 2. Set Up Twilio (for SMS)

1. Sign up for a free Twilio account: https://www.twilio.com/try-twilio
2. Get your trial phone number
3. Note down:
   - Account SID
   - Auth Token
   - Your Twilio phone number
4. Verify your personal phone number in Twilio (required for trial accounts)

### 3. Set Up Email (Gmail Example)

**For Gmail:**
1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other" device
   - Copy the 16-character password
3. Note down:
   - Your Gmail address
   - The app password

**For other email providers:**
- Use their SMTP server and credentials
- Common SMTP servers:
  - Gmail: `smtp.gmail.com:587`
  - Outlook: `smtp-mail.outlook.com:587`
  - Yahoo: `smtp.mail.yahoo.com:587`

### 4. Add GitHub Secrets

Go to your repository on GitHub:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these secrets one by one:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `VISA_API_KEY` | Your CheckVisaSlots access code | `EOXH4L` |
| `EMAIL_FROM` | Your email address | `yourname@gmail.com` |
| `EMAIL_TO` | Where to send alerts | `yourname@gmail.com` |
| `EMAIL_PASSWORD` | Email app password | `abcd efgh ijkl mnop` |
| `SMTP_SERVER` | SMTP server address | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port number | `587` |
| `TWILIO_ACCOUNT_SID` | From Twilio dashboard | `ACxxxxxxxxxxxxx` |
| `TWILIO_AUTH_TOKEN` | From Twilio dashboard | `your_auth_token` |
| `TWILIO_FROM_PHONE` | Your Twilio phone | `+1234567890` |
| `TO_PHONE` | Your personal phone | `+1234567890` |

**Note:** Phone numbers must include country code (e.g., `+1` for US, `+971` for UAE)

### 5. Push to GitHub

```bash
git add .
git commit -m "Initial commit: Visa slot checker"
git push origin main
```

### 6. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. If prompted, click **I understand my workflows, go ahead and enable them**

### 7. Test the Workflow

1. Go to **Actions** tab
2. Click on **Check Visa Slots** workflow
3. Click **Run workflow** → **Run workflow**
4. Watch it run (takes ~30 seconds)
5. Check the logs to see if it worked

## How It Works

1. **Every 15 minutes**, GitHub Actions runs the Python script
2. The script calls the CheckVisaSlots API with your access code
3. It checks Abu Dhabi slot availability
4. If slots went from 0 to positive (or increased), it:
   - Sends you an email with details
   - Sends you an SMS alert
5. Saves the current state to `last_state.json`
6. Commits the state file back to the repository

## Monitoring

- Check the **Actions** tab to see workflow runs
- Each run shows logs of what happened
- Failed runs will show up in red
- You'll get notifications if the workflow fails repeatedly

## Customization

### Change Target Location

Edit `check_visa_slots.py` line 23:
```python
TARGET_LOCATION = "DUBAI"  # Change to DUBAI or any other location
```

### Change Check Frequency

Edit `.github/workflows/check_visa_slots.yml` line 6:
```yaml
- cron: '*/15 * * * *'  # Every 15 minutes
- cron: '*/30 * * * *'  # Every 30 minutes
- cron: '0 * * * *'     # Every hour
```

### Alert on Any Change

Edit `check_visa_slots.py` around line 125 to alert on any increase:
```python
if current_slots > last_slots:  # Alert on ANY increase
    slots_opened = True
```

## Troubleshooting

**Workflow not running?**
- Make sure Actions are enabled in repository settings
- Check the schedule syntax in the workflow file

**Not receiving notifications?**
- Check the workflow logs for errors
- Verify all secrets are set correctly
- For Gmail, make sure you used an App Password, not your regular password
- For Twilio trial, verify your recipient phone number is verified

**API errors?**
- Verify your access code is correct
- Check if the CheckVisaSlots service is working

**State file not updating?**
- Make sure the repository has write permissions
- Check the commit step in workflow logs

## Cost

- **GitHub Actions**: Free (2,000 minutes/month for private repos, unlimited for public)
- **Twilio**: Free trial credits (~$15), then pay-as-you-go (SMS costs ~$0.0075 per message)
- **Email**: Free with Gmail

**Estimated monthly cost after free trial**: ~$0.50 for SMS (if you get alerts)

## Notes

- The script only alerts when slots **open up** (go from 0 to positive)
- It won't spam you with notifications for every check
- State is preserved between runs
- You can manually trigger the workflow anytime from GitHub Actions UI

## Support

If you encounter issues:
1. Check the Actions logs for error messages
2. Verify all secrets are set correctly
3. Test your Twilio credentials in their console
4. Test your email credentials with a simple Python script

## License

Free to use and modify for personal use.
