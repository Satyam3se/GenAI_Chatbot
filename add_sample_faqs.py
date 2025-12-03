import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GENAI.settings')
django.setup()

from chat_app.models import FAQ

def add_sample_faqs():
    faqs_to_add = [
        {
            "question": "What are the company's working hours?",
            "answer": "Our standard working hours are Monday to Friday, 9:00 AM to 5:00 PM.",
            "keywords": "working hours, office hours, schedule",
            "category": "HR Policy"
        },
        {
            "question": "How do I request time off?",
            "answer": "You can request time off through the HR portal. Please submit your request at least two weeks in advance.",
            "keywords": "time off, leave, vacation, holiday",
            "category": "HR Policy"
        },
        {
            "question": "Where can I find the employee handbook?",
            "answer": "The employee handbook is available on the company's intranet under the 'Documents' section.",
            "keywords": "handbook, employee guide, policies",
            "category": "HR Policy"
        },
        {
            "question": "How do I set up my email?",
            "answer": "Please refer to the IT setup guide available on the IT support page. If you encounter issues, contact the IT helpdesk.",
            "keywords": "email setup, outlook, mail",
            "category": "IT Setup"
        },
        {
            "question": "What are the company's benefits?",
            "answer": "We offer a comprehensive benefits package including health insurance, dental, vision, and a 401k plan. More details are available on the HR portal.",
            "keywords": "benefits, health, insurance, 401k",
            "category": "Benefits"
        },
        {
            "question": "How do I connect to the company Wi-Fi?",
            "answer": "The company Wi-Fi network name is 'CompanyNet'. The password can be found on the IT support page or by asking a colleague.",
            "keywords": "wifi, internet, network",
            "category": "IT Setup"
        },
        {
            "question": "Who is my manager?",
            "answer": "Your manager is [Manager's Name]. You can find their contact information in the company directory.",
            "keywords": "manager, supervisor, boss",
            "category": "General"
        },
        {
            "question": "What is the dress code?",
            "answer": "Our dress code is business casual. Please refer to the employee handbook for more specific guidelines.",
            "keywords": "dress code, attire, clothing",
            "category": "HR Policy"
        },
        {
            "question": "How do I access my payslips?",
            "answer": "Payslips are available monthly through the payroll portal. You should have received login credentials during your onboarding.",
            "keywords": "payslip, salary, payroll",
            "category": "HR Policy"
        },
        {
            "question": "What software do I need for my role?",
            "answer": "The essential software for your role includes [Software A], [Software B], and [Software C]. Your IT onboarding checklist provides installation instructions.",
            "keywords": "software, tools, applications",
            "category": "IT Setup"
        },
        {
            "question": "Where is the nearest coffee machine?",
            "answer": "There are coffee machines located on every floor near the kitchen areas.",
            "keywords": "coffee, break room, kitchen",
            "category": "Office Facilities"
        },
        {
            "question": "How do I book a meeting room?",
            "answer": "Meeting rooms can be booked via the company's internal calendar system (e.g., Outlook Calendar or Google Calendar).",
            "keywords": "meeting room, booking, conference room",
            "category": "Office Facilities"
        },
        {
            "question": "What is the policy on remote work?",
            "answer": "Our remote work policy allows for [number] days of remote work per week, subject to manager approval. Details are in the employee handbook.",
            "keywords": "remote work, WFH, work from home",
            "category": "HR Policy"
        },
        {
            "question": "How do I get a new ID card?",
            "answer": "Please contact building security or HR to arrange for a new ID card. A temporary pass can be issued if needed.",
            "keywords": "ID card, access card, badge",
            "category": "General"
        },
        {
            "question": "What is the company's mission statement?",
            "answer": "Our mission is to [Insert Company Mission Statement Here].",
            "keywords": "mission, vision, values",
            "category": "General"
        },
        {
            "question": "How do I set up my new laptop/computer?",
            "answer": "Your IT onboarding checklist provides detailed instructions for setting up your new computer, including connecting to the network, installing essential software, and configuring your email. Please refer to it first. If you encounter any issues, contact the IT helpdesk.",
            "keywords": "laptop setup, computer setup, IT setup, new hire tech, workstation",
            "category": "IT Setup"
        },
        {
            "question": "Where can I find my onboarding checklist?",
            "answer": "Your personalized onboarding checklist is available on the HR portal under the 'New Hire Resources' section. It outlines all the steps you need to complete during your first 30 days.",
            "keywords": "onboarding checklist, new hire tasks, first 30 days, HR portal",
            "category": "Onboarding"
        },
        {
            "question": "How do I get access to internal tools like Jira, Confluence, or Slack?",
            "answer": "Access to internal tools is typically provisioned automatically based on your role. If you are missing access to a specific tool, please submit an IT support ticket, specifying the tool and your team.",
            "keywords": "Jira access, Confluence access, Slack access, internal tools, software access",
            "category": "IT Setup"
        },
        {
            "question": "What is the process for submitting expenses?",
            "answer": "Expenses can be submitted through our expense management system, accessible via the company intranet. Please ensure you attach all receipts. A detailed guide is available in the Finance section of the intranet.",
            "keywords": "expenses, expense report, reimbursement, finance",
            "category": "HR Policy"
        },
        {
            "question": "Who should I contact for HR-related questions during my onboarding?",
            "answer": "For any HR-related questions during your onboarding, please reach out to your dedicated HR buddy, whose contact information was provided in your welcome email. You can also contact the general HR department.",
            "keywords": "HR contact, HR questions, onboarding support, HR buddy",
            "category": "HR Policy"
        },
        {
            "question": "How do I enroll in benefits?",
            "answer": "You will receive an email from HR within your first week with instructions on how to enroll in your benefits package. Please complete this process within 30 days of your start date.",
            "keywords": "benefits enrollment, health insurance, dental, vision, 401k",
            "category": "Benefits"
        },
        {
            "question": "What is the company's policy on vacation and sick leave for new employees?",
            "answer": "New employees accrue vacation and sick leave according to company policy, which can be found in the employee handbook. Specific details regarding accrual rates and usage are outlined there.",
            "keywords": "vacation policy, sick leave, new employee leave, time off",
            "category": "HR Policy"
        },
        {
            "question": "How do I set up my company phone/mobile device?",
            "answer": "If your role requires a company mobile device, IT will provide you with setup instructions and necessary configurations. Please contact the IT helpdesk if you haven't received these.",
            "keywords": "company phone, mobile device setup, phone configuration, IT support",
            "category": "IT Setup"
        },
        {
            "question": "Where can I find information about company culture and values?",
            "answer": "Information about our company culture, values, and mission statement can be found on our internal company portal and in the employee handbook. We also encourage you to speak with your team members.",
            "keywords": "company culture, values, mission, company portal",
            "category": "General"
        },
    ]

    for faq_data in faqs_to_add:
        faq, created = FAQ.objects.get_or_create(
            question=faq_data["question"],
            defaults={
                "answer": faq_data["answer"],
                "keywords": faq_data["keywords"],
                "category": faq_data["category"]
            }
        )
        if created:
            print(f"Added FAQ: {faq.question}")
        else:
            print(f"FAQ already exists (updated if necessary): {faq.question}")
            # Optionally update existing FAQ if needed
            faq.answer = faq_data["answer"]
            faq.keywords = faq_data["keywords"]
            faq.category = faq_data["category"]
            faq.save()


if __name__ == '__main__':
    print("Adding sample FAQs...")
    add_sample_faqs()
    print("Finished adding sample FAQs.")
