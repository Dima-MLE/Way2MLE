import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_stepik_token():
    auth = requests.auth.HTTPBasicAuth(
        os.getenv('STEPIK_CLIENT_ID'),
        os.getenv('STEPIK_CLIENT_SECRET')
    )
    response = requests.post(
        'https://stepik.org/oauth2/token/',
        data={'grant_type': 'client_credentials'},
        auth=auth
    )
    return response.json().get('access_token')

def get_course_progress(course_id, token):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://stepik.org/api/course-progresses?course={course_id}'
    response = requests.get(url, headers=headers)
    return response.json()

def update_progress_md(progress_data):
    with open('progress.md', 'w') as f:
        f.write("# Stepik Course Progress\n\n")
        f.write(f"## Data Science Starter Progress\n\n")
        for progress in progress_data['course-progresses']:
            percent = progress['score'] * 100
            f.write(f"- Пройдено: {percent:.2f}%\n")

if __name__ == "__main__":
    token = get_stepik_token()
    course_id = os.getenv('STEPIK_COURSE_ID')
    progress_data = get_course_progress(course_id, token)
    update_progress_md(progress_data)
    print("Progress updated successfully!")
