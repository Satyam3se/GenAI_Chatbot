import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GENAI.settings')
django.setup()

from chat_app.models import FAQ

def add_sample_it_support_faq():
    # Sample FAQ 1: Password Reset
    faq_data_1 = {
        'question': 'How do I reset my password?',
        'answer': 'To reset your password, please visit the password reset portal at https://yourcompany.com/password-reset and follow the instructions. If you encounter issues, contact IT support.',
        'keywords': 'password, reset, login, account',
        'category': 'IT Support'
    }
    FAQ.objects.get_or_create(question=faq_data_1['question'], defaults=faq_data_1)
    print("Added sample FAQ: 'How do I reset my password?'")

    # Sample FAQ 2: Wi-Fi Connection
    faq_data_2 = {
        'question': 'How do I connect to the office Wi-Fi?',
        'answer': 'To connect to the office Wi-Fi, select the network "YourCompany_WiFi", then enter your network username and password. If you have trouble connecting, ensure your Wi-Fi drivers are up to date or contact IT support.',
        'keywords': 'wifi, wi-fi, network, connect, internet',
        'category': 'IT Support'
    }
    FAQ.objects.get_or_create(question=faq_data_2['question'], defaults=faq_data_2)
    print("Added sample FAQ: 'How do I connect to the office Wi-Fi?'")

    # Sample FAQ 3: Software Installation Request
    faq_data_3 = {
        'question': 'How can I request new software?',
        'answer': 'To request new software, please submit a software request ticket through our IT portal at https://yourcompany.com/it-portal/software-request. Provide details about the software and your business need.',
        'keywords': 'software, install, request, new program',
        'category': 'IT Support'
    }
    FAQ.objects.get_or_create(question=faq_data_3['question'], defaults=faq_data_3)
    print("Added sample FAQ: 'How can I request new software?'")

if __name__ == '__main__':
    add_sample_it_support_faq()
