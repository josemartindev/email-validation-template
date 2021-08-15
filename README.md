# email-validation-template
Email validation link in Python Flask.

1. Set an environment variable with the Sendgrid API key:
export SENDGRID_API_KEY="SG.y65hJF...."

2. Add your sender email to the variable sender_email, for example:
sender_email = noreply@company.com 

3. python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

4. python app.py