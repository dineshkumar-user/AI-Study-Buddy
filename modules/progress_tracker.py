import json
import os
from datetime import datetime, timedelta


DATA_FILE = "study_data.json"


def default_data():

    return {
        "quiz_history": [],
        "bookmarks": [],
        "study_sessions": []
    }


def load_data():

    if not os.path.exists(DATA_FILE):

        return default_data()

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        # Make sure keys exist
        if "quiz_history" not in data:
            data["quiz_history"] = []

        if "bookmarks" not in data:
            data["bookmarks"] = []

        if "study_sessions" not in data:
            data["study_sessions"] = []

        return data

    except Exception:

        return default_data()


def save_data(data):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def save_quiz_result(
    correct,
    total,
    weak_topics
):

    data = load_data()

    percentage = (
        correct / total * 100
        if total > 0
        else 0
    )

    result = {
        "date": datetime.now().strftime(
            "%d %B %Y %I:%M %p"
        ),
        "correct": correct,
        "total": total,
        "percentage": round(
            percentage,
            1
        ),
        "weak_topics": weak_topics
    }

    data["quiz_history"].append(result)

    save_data(data)


def add_bookmark(topic):

    data = load_data()

    topic = topic.strip()

    if topic and topic not in data["bookmarks"]:

        data["bookmarks"].append(topic)

    save_data(data)


def remove_bookmark(topic):

    data = load_data()

    if topic in data["bookmarks"]:

        data["bookmarks"].remove(topic)

    save_data(data)


def add_study_session(minutes):

    data = load_data()

    session = {
        "date": datetime.now().strftime(
            "%d %B %Y %I:%M %p"
        ),
        "minutes": int(minutes)
    }

    data["study_sessions"].append(session)

    save_data(data)


def calculate_streak(history):

    if not history:
        return 0

    dates = set()

    for item in history:

        try:

            date = datetime.strptime(
                item["date"],
                "%d %B %Y %I:%M %p"
            ).date()

            dates.add(date)

        except Exception:
            continue

    if not dates:
        return 0

    today = datetime.now().date()

    # If there is no activity today,
    # check whether yesterday was active.
    if today not in dates:

        yesterday = today - timedelta(days=1)

        if yesterday not in dates:
            return 0

        current = yesterday

    else:

        current = today

    streak = 0

    while current in dates:

        streak += 1

        current -= timedelta(days=1)

    return streak


def get_progress_statistics():

    data = load_data()

    history = data["quiz_history"]

    sessions = data["study_sessions"]

    if history:

        scores = [
            item["percentage"]
            for item in history
        ]

        average_score = sum(scores) / len(scores)

        best_score = max(scores)

        latest_score = scores[-1]

        if len(scores) >= 2:

            previous_score = scores[-2]

            improvement = (
                latest_score -
                previous_score
            )

        else:

            improvement = 0

    else:

        average_score = 0
        best_score = 0
        latest_score = 0
        improvement = 0

    total_minutes = sum(
        session["minutes"]
        for session in sessions
    )

    streak = calculate_streak(history)

    return {
        "average_score": round(
            average_score,
            1
        ),
        "best_score": round(
            best_score,
            1
        ),
        "latest_score": round(
            latest_score,
            1
        ),
        "improvement": round(
            improvement,
            1
        ),
        "total_minutes": total_minutes,
        "quiz_attempts": len(history),
        "streak": streak
    }