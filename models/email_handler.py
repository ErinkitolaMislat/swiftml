# import threading
from firebmail import sendmail, BatchMail
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.conf import settings



def success_email_after_application(**kwargs)->bool:
    """
    Send an email to the applicant after a successful application
    """
    try:
        html_message = render_to_string(
            'mails/application_done.html', {
                'applicant_name': kwargs.get('applicant_name'),
                'current_year': now().year,
            }
        )
        sender = settings.APP_EMAIL
        password = settings.APP_PASSWORD
        mail_args = {
            'sender': sender,
            'password': password,
            'recipient': kwargs.get('applicant_email', ''),
            'sender_name': "Firebcorps Mentorship",
            'subject': 'Application Received',
            'payload': html_message,
            'type_': 'html',
        }
        # threading.Thread(target=sendmail, kwargs=mail_args).start()
        sendmail(
            **mail_args
        )
        return True
    except Exception as e:
        return False
    
def copy_email_to_admin(**kwargs)->bool:
    """
    Send an email to the admin after a successful application
    """
    try:
        context = {
            'applicant_name': kwargs.get('applicant_name'),
            'applicant_email': kwargs.get('applicant_email'),
            'career_choice': kwargs.get('career'),
            'no_of_hours_per_day': kwargs.get('no_of_hours_per_day'),
            'device': kwargs.get('device'),
            'preferred_study_materials': kwargs.get('preferred_study_materials'),
            'interest_in_tech': kwargs.get('interest_in_tech'),
            'goals_as_a_technologist': kwargs.get('goals_as_a_technologist'),
            'how_did_you_hear_about_us': kwargs.get('how_did_you_hear_about_us'),
            'why_you_should_be_accepted': kwargs.get('why_you_should_be_accepted'),
            'anything_else': kwargs.get('anything_else'),
        }
        html_message = render_to_string(
            'mails/copy_to_admin.html', context
        )
        sender = settings.APP_EMAIL
        password = settings.APP_PASSWORD
        mail_args = {
            'sender': sender,
            'password': password,
            'recipient': settings.ADMIN_EMAIL,
            'subject': 'New Application Received',
            'payload': html_message,
            'type_': 'html',
        }
        # threading.Thread(target=sendmail, kwargs=mail_args).start()
        sendmail(
            **mail_args
        )
        return True
    except Exception as e:
        return False
    

def send_direct_mail_to(recipient:str, subject:str, payload:str)->bool:
    try:
        # payload = render_to_string(payload)
        sender = settings.APP_EMAIL
        password = settings.APP_PASSWORD
        mail_args = {
            'sender': sender,
            'password': password,
            'sender_name': "Firebcorps Mentorship",
            'recipient': recipient,
            'subject': subject,
            'payload': payload,
            'type_': 'html',
        }
        sendmail(**mail_args)
        return True
    except Exception as e:
        print(e, 'exception')
        return False
    

def send_multiple_emails(recipients:list, subject:str, payload:str)->bool:
    try:
        sender = settings.APP_EMAIL
        password = settings.APP_PASSWORD
        mail_args = {
            'sender': sender,
            'password': password,
            'sender_name': "Firebcorps Mentorship",
            'subject': subject,
            'payload': payload,
            'type_': 'html',
        }
        batch_sender = BatchMail(**mail_args)
        batch_sender.send_batch(recipients)
        return True
    except Exception as e:
        return False
    
def send_mail_to_self(subject:str, payload:str)->bool:
    try:
        sender = settings.APP_EMAIL
        password = settings.APP_PASSWORD
        mail_args = {
            'sender': sender,
            'password': password,
            'sender_name': "Firebcorps Mentorship",
            'recipient': settings.ADMIN_EMAIL,
            'subject': subject,
            'payload': payload,
            'type_': 'html',
        }
        sendmail(**mail_args)
        return True
    except Exception as e:
        return False