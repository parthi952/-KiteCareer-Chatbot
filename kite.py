from shlex import join
import pandas as pd
import google.generativeai as genai
from nltk.tokenize import word_tokenize
import nltk

# nltk.download('punkt')  first one time installation
genai.configure(api_key="YOUR API KEY")

company_details = {
    "Company Name": "KiteCareer",
    "Founded": "2018",
    "Location": "Surandai, Tenkasi, Tamil Nadu, India",
    "Team Size": "11 to 50",
    "Website": "https://kitecareer.com",
    "Email": "hr@kitecareer.com",
    "Phone": "+91 9498478472",
    "Services Offered": "Custom Software Development, Mobile & Web Development, Cloud Integration, Product Development, AI/ML, UI/UX, Training",
    "Technologies Used": "Python, PHP, ReactJS, MERN Stack, Django, Flutter, AWS, Blockchain",
    "Unique Selling Points": "Agile & scalable solutions, Client-centric approach, Innovative tech stack, Digital solution partner"
}

technologies_data = {
    "Technology": ["Python", "PHP", "ReactJS, MERN Stack", "Django", "Flutter, Hybrid Apps", "AWS, Cloud Integration", "AI/ML", "IoT", "UI/UX Design", "Cybersecurity, Blockchain"],
    "Courses/Topics Included": ["Core programming, automation", "Web backend, application logic", "Frontend and fullstack", "Fullstack web framework", "Cross-platform mobile apps", "Cloud services & DevOps basics", "Machine learning fundamentals", "Embedded, connected devices", "Modern design practices", "Security basics & ledger tech"],
    "Typical Applications": ["Software, data science", "Website development", "Web & app development", "Scalable applications", "Android/iOS app development", "Cloud hosting/deployment", "Data science, intelligent apps", "Smart systems, sensors", "Web/mobile interfaces", "Secure applications"]
}
technologies_df = pd.DataFrame(technologies_data)

model = genai.GenerativeModel('gemini-2.5-pro')

while True:
    user_input = input("\nCustomer: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Assistant: Thank you for visiting KiteCareer!")
        break

    tokens = word_tokenize(user_input.lower())
    matched_info = ""

    company_keywords = ['company', 'kitecareer', 'services', 'location', 'email', 'phone', 'contact', 'website', 'details', 'about', 'info']
    if any(token in company_keywords for token in tokens):
        info_list = [f"{key}: {value}" for key, value in company_details.items()]
        matched_info = "\n".join(info_list)

    if not matched_info: 
        matched_technologies = []
        for _, row in technologies_df.iterrows():
            if any(token.replace(',', '').strip() in row['Technology'].lower() for token in tokens):
                matched_technologies.append(row)
        
        if matched_technologies:
            product_info = "\n".join(
                [f"Technology: {p['Technology']}, Courses: {p['Courses/Topics Included']}, Applications: {p['Typical Applications']}" for p in matched_technologies]
            )
            matched_info = product_info

    if matched_info:
        prompt = f"""
        You are a friendly and helpful assistant for KiteCareer.
        Here is the relevant information:
        {matched_info}
        Customer asked: "{user_input}"
        Provide a very short, friendly, SMS-like response.
        Every response must start with a positive greeting and to say for more detial wnt wisit web  and include the company website and email.
        Website: {company_details['Website']}
        Email: {company_details['Email']}
        contact: {company_details['Phone']}
        """
    else:
        prompt = f"""
        You are a friendly and helpful assistant for KiteCareer.
        Customer asked: "{user_input}"
        No matching information was found.
        Provide a very short, polite, SMS-like response.
        Every response must start with a positive greeting and include the company website and email.
        Suggest they ask about company services or details.
        Website: {company_details['Website']}
        Email: {company_details['Email']}
        """

    response = model.generate_content(prompt)
    print("\nAssistant:", response.text)