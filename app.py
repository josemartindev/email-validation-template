from flask import Flask, request, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
sender_email = 'noreply@codebook.app'

# create a fake token for testing purposes
s = URLSafeTimedSerializer('Thisisasecret!')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
    email = request.form['email']
    # Be sure to check if email exists in the database in order to continue
    token = s.dumps(email, salt='email-confirm')
    link = url_for('confirm_email', token=token, _external=True)
    message = Mail(from_email=sender_email, to_emails=[email], subject='Confirmation Link', plain_text_content='Please confirm your email using this link: {}'.format(link))
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
    return '<h1>We have sent an e-mail confirmation link to {}. The token is {}</h1>'.format(email, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    # change for example isEmailConfirmed variable from false to true in the database
    return '<h1>The token works! You have just confirmed your e-mail.</h1>'

if __name__ == '__main__':
    app.run(debug=True)