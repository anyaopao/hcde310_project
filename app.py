from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def fetch_birthday_events(month, day):
    try:
        query = f"{month}_{day}"
        url = f"https://en.wikipedia.org/wiki/{query}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            events_section = soup.find('span', {'id': 'Events'})
            if events_section:
                events_list = events_section.find_next('ul')
                if events_list:
                    events = []
                    for li in events_list.find_all('li'):
                        event_text = li.text.strip()
                        event_url = li.find('a', href=True)
                        if event_url:
                            event_url = event_url['href']
                            events.append((event_text, event_url))
                    return events[:10]
            return None
        else:
            print("Failed to fetch Wikipedia page.")
            return None
    except Exception as e:
        print("Error:", e)
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch_events', methods=['POST'])
def fetch_events():
    month = request.form['month']
    day = request.form['day']
    events = fetch_birthday_events(month, day)
    if events:
        return render_template(
            'events.html', month=month, day=day, events=events
        )
    else:
        return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True)
