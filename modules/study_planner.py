from .ai_engine import generate_study_plan


def create_plan(weak_topics, study_hours):

    if not weak_topics:
        return (
            "No weak concepts detected yet. "
            "Complete a quiz first."
        )

    return generate_study_plan(
        weak_topics,
        study_hours
    )