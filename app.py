import streamlit as st
from datetime import datetime
import pandas as pd

# ==========================================================
# AI ENGINE
# ==========================================================

from modules.ai_engine import (
    explain_concept,
    chat_with_notes,
    generate_ai_summary,
    generate_quiz,
    generate_flashcards,
    generate_study_plan,
    generate_learning_recommendation
)

# ==========================================================
# DOCUMENT PROCESSOR
# ==========================================================

from modules.document_processor import (
    extract_text
)

# ==========================================================
# NLP SUMMARIZER
# ==========================================================

from modules.summarizer import (
    tfidf_summary
)

# ==========================================================
# PROGRESS TRACKER
# ==========================================================

from modules.progress_tracker import (
    load_data,
    save_quiz_result,
    add_bookmark,
    remove_bookmark,
    add_study_session,
    get_progress_statistics
)

# ==========================================================
# STUDY PLANNER
# ==========================================================

from modules.study_planner import (
    create_plan
)

# ==========================================================
# REPORT GENERATOR
# ==========================================================

from modules.report_generator import (
    create_report
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = []

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🎓 AI Study Buddy")

    st.caption(
        "Your Personal AI Learning Assistant"
    )

    st.divider()

    # ------------------------------------------------------
    # DATE AND TIME
    # ------------------------------------------------------

    current_time = datetime.now()

    st.info(
        f"📅 **Date:** "
        f"{current_time.strftime('%d %B %Y')}\n\n"
        f"🕐 **Time:** "
        f"{current_time.strftime('%I:%M:%S %p')}"
    )

    st.divider()

    # ------------------------------------------------------
    # NAVIGATION
    # ------------------------------------------------------

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📚 Study Material",
            "🤖 AI Chat",
            "💡 Concept Explainer",
            "📝 Smart Summary",
            "❓ AI Quiz",
            "🗂️ Flashcards",
            "🎯 Weak Concepts",
            "🧠 Study Plan",
            "📈 Progress",
            "⏱️ Study Timer",
            "📌 Bookmarks",
            "📄 Study Report"
        ]
    )

    st.divider()

    # ------------------------------------------------------
    # AI TECHNIQUES
    # ------------------------------------------------------

    st.subheader("🧠 AI Techniques")

    st.write("• Natural Language Processing")
    st.write("• TF-IDF")
    st.write("• Cosine Similarity")
    st.write("• Large Language Model")
    st.write("• Performance Analysis")
    st.write("• Personalized Recommendations")

    st.divider()

    st.caption(
        "Powered by Llama 3.2 3B + Ollama"
    )


# ==========================================================
# MAIN HEADER
# ==========================================================

st.title("🎓 AI Study Buddy")

st.write(
    "An AI-powered personal learning assistant "
    "for studying, summarization, quizzes and "
    "personalized learning."
)

st.divider()


# ==========================================================
# DASHBOARD
# ==========================================================

if page == "🏠 Dashboard":

    st.subheader(
        "👋 Welcome to your AI Study Dashboard"
    )

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    # Latest score

    if history:

        latest_score = history[-1].get(
            "percentage",
            0
        )

    else:

        latest_score = 0

    # ------------------------------------------------------
    # DASHBOARD METRICS
    # ------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Study Words",
            len(
                st.session_state.notes.split()
            )
        )

    with col2:

        st.metric(
            "📝 Quiz Attempts",
            len(history)
        )

    with col3:

        st.metric(
            "🎯 Latest Score",
            f"{latest_score:.1f}%"
        )

    with col4:

        st.metric(
            "📌 Bookmarks",
            len(
                data.get(
                    "bookmarks",
                    []
                )
            )
        )

    st.divider()

    # ------------------------------------------------------
    # QUICK START
    # ------------------------------------------------------

    st.subheader("🚀 Quick Start")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📚 **Study Material**\n\n"
            "Upload PDF, TXT or DOCX notes."
        )

    with col2:

        st.info(
            "🤖 **AI Chat**\n\n"
            "Ask questions about your notes."
        )

    with col3:

        st.info(
            "❓ **AI Quiz**\n\n"
            "Generate quizzes from your notes."
        )

    st.divider()

    # ------------------------------------------------------
    # CURRENT DATE AND TIME
    # ------------------------------------------------------

    st.subheader("📅 Current Date & Time")

    now = datetime.now()

    st.write(
        now.strftime(
            "%A, %d %B %Y | %I:%M:%S %p"
        )
    )

    st.divider()

    # ------------------------------------------------------
    # HOW IT WORKS
    # ------------------------------------------------------

    st.subheader(
        "🧠 How AI Study Buddy Works"
    )

    step1, step2, step3, step4 = st.columns(4)

    with step1:

        st.markdown("### 1️⃣")
        st.write("Upload notes")

    with step2:

        st.markdown("### 2️⃣")
        st.write("AI processes content")

    with step3:

        st.markdown("### 3️⃣")
        st.write("Take AI quiz")

    with step4:

        st.markdown("### 4️⃣")
        st.write("Detect weak concepts")


# ==========================================================
# STUDY MATERIAL
# ==========================================================

elif page == "📚 Study Material":

    st.subheader(
        "📚 Study Material"
    )

    st.write(
        "Upload your study material or enter it manually."
    )

    # ------------------------------------------------------
    # FILE UPLOAD
    # ------------------------------------------------------

    uploaded_file = st.file_uploader(
        "Upload Study Material",
        type=[
            "txt",
            "pdf",
            "docx"
        ]
    )

    if uploaded_file:

        try:

            content = extract_text(
                uploaded_file
            )

            st.session_state.notes = content

            st.success(
                "✅ Study material loaded successfully!"
            )

        except Exception as error:

            st.error(
                f"❌ Error reading file: {error}"
            )

    st.divider()

    # ------------------------------------------------------
    # TEXT AREA
    # ------------------------------------------------------

    notes = st.text_area(
        "✏️ Enter or edit your study material",
        value=st.session_state.notes,
        height=400
    )

    st.session_state.notes = notes

    # ------------------------------------------------------
    # MATERIAL STATISTICS
    # ------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📖 Words",
            len(notes.split())
        )

    with col2:

        st.metric(
            "🔤 Characters",
            len(notes)
        )

    with col3:

        st.metric(
            "📝 Lines",
            len(notes.splitlines())
        )

    st.divider()

    # ------------------------------------------------------
    # CLEAR MATERIAL
    # ------------------------------------------------------

    if st.button(
        "🗑️ Clear Study Material"
    ):

        st.session_state.notes = ""

        st.success(
            "✅ Study material cleared!"
        )

        st.rerun()


# ==========================================================
# AI CHAT
# ==========================================================

elif page == "🤖 AI Chat":

    st.subheader(
        "🤖 AI Chat with Your Notes"
    )

    st.write(
        "Ask questions about your study material "
        "using your local AI assistant."
    )

    if not st.session_state.notes.strip():

        st.warning(
            "⚠️ Please add study material first."
        )

    else:

        question = st.text_input(
            "💬 Ask your question",
            placeholder=(
                "Example: Explain inheritance simply"
            )
        )

        if st.button(
            "🤖 Ask AI",
            type="primary"
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "🧠 AI is thinking..."
                ):

                    answer = chat_with_notes(
                        question,
                        st.session_state.notes
                    )

                # Save chat

                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )

                st.success(
                    "🤖 AI Answer"
                )

                st.markdown(answer)

    # ------------------------------------------------------
    # CHAT HISTORY
    # ------------------------------------------------------

    if st.session_state.chat_history:

        st.divider()

        st.subheader(
            "💬 Previous Questions"
        )

        for chat in reversed(
            st.session_state.chat_history
        ):

            with st.expander(
                chat["question"]
            ):

                st.write(
                    chat["answer"]
                )

    st.divider()

    st.info(
        "🧠 Powered by Llama 3.2 3B running locally "
        "through Ollama. No OpenAI API required."
    )


# ==========================================================
# CONCEPT EXPLAINER
# ==========================================================

elif page == "💡 Concept Explainer":

    st.subheader(
        "💡 AI Concept Explainer"
    )

    st.write(
        "Ask the AI to explain a difficult concept "
        "in a level that matches your understanding."
    )

    topic = st.text_input(
        "📌 Enter a concept",
        placeholder="Example: Inheritance in Python"
    )

    difficulty = st.selectbox(
        "🎓 Explanation Level",
        [
            "Simple - Beginner",
            "Intermediate",
            "Detailed - Advanced"
        ]
    )

    if st.button(
        "✨ Explain Concept",
        type="primary"
    ):

        if not topic.strip():

            st.warning(
                "Please enter a concept."
            )

        else:

            with st.spinner(
                "🧠 AI is preparing the explanation..."
            ):

                result = explain_concept(
                    topic,
                    st.session_state.notes,
                    difficulty
                )

            st.markdown(result)


# ==========================================================
# SMART SUMMARY
# ==========================================================

elif page == "📝 Smart Summary":

    st.subheader(
        "📝 Smart Summary"
    )

    if not st.session_state.notes.strip():

        st.warning(
            "⚠️ Please add study material first."
        )

    else:

        summary_type = st.selectbox(
            "📋 Summary Type",
            [
                "Bullet Points",
                "Paragraph"
            ]
        )

        if st.button(
            "✨ Generate AI Summary",
            type="primary"
        ):

            with st.spinner(
                "🧠 AI is summarizing your notes..."
            ):

                summary = generate_ai_summary(
                    st.session_state.notes,
                    summary_type
                )

            st.markdown(summary)

        st.divider()

        # --------------------------------------------------
        # TF-IDF SUMMARY
        # --------------------------------------------------

        st.subheader(
            "🔬 NLP Extractive Summary"
        )

        number = st.slider(
            "Number of important sentences",
            3,
            10,
            5
        )

        if st.button(
            "🔍 Generate TF-IDF Summary"
        ):

            summary = tfidf_summary(
                st.session_state.notes,
                number
            )

            if summary:

                for index, sentence in enumerate(
                    summary,
                    1
                ):

                    st.write(
                        f"**{index}.** {sentence}"
                    )

            else:

                st.warning(
                    "Could not generate summary."
                )


# ==========================================================
# AI QUIZ
# ==========================================================

elif page == "❓ AI Quiz":

    st.subheader(
        "❓ AI Quiz Generator"
    )

    st.write(
        "Generate an interactive multiple-choice quiz "
        "from your study material."
    )

    if not st.session_state.notes.strip():

        st.warning(
            "⚠️ Please add study material first."
        )

    else:

        number = st.slider(
            "Number of questions",
            min_value=3,
            max_value=10,
            value=5
        )

        # --------------------------------------------------
        # GENERATE QUIZ
        # --------------------------------------------------

        if st.button(
            "🎲 Generate AI Quiz",
            type="primary"
        ):

            with st.spinner(
                "🧠 AI is creating your quiz..."
            ):

                quiz = generate_quiz(
                    st.session_state.notes,
                    number
                )

            if quiz:

                st.session_state.quiz = quiz

                st.session_state.quiz_results = []

                st.success(
                    f"✅ {len(quiz)} questions generated!"
                )

            else:

                st.error(
                    "❌ Quiz generation failed.\n\n"
                    "Please make sure Ollama is running "
                    "and try again."
                )

        # --------------------------------------------------
        # DISPLAY QUIZ
        # --------------------------------------------------

        if st.session_state.quiz:

            st.divider()

            st.subheader(
                "📝 Answer the Questions"
            )

            answers = {}

            for index, question in enumerate(
                st.session_state.quiz
            ):

                st.markdown(
                    f"### Question {index + 1}"
                )

                st.write(
                    question["question"]
                )

                answers[index] = st.radio(
                    "Choose your answer:",
                    question["options"],
                    key=f"quiz_answer_{index}"
                )

                st.divider()

            # --------------------------------------------------
            # SUBMIT QUIZ
            # --------------------------------------------------

            if st.button(
                "✅ Submit Quiz",
                type="primary"
            ):

                results = []

                correct_count = 0

                weak_topics = []

                for index, question in enumerate(
                    st.session_state.quiz
                ):

                    selected = answers[index]

                    correct = (
                        selected ==
                        question["answer"]
                    )

                    if correct:

                        correct_count += 1

                    else:

                        weak_topics.append(
                            question["concept"]
                        )

                    results.append(
                        {
                            "question":
                                question["question"],

                            "selected":
                                selected,

                            "correct_answer":
                                question["answer"],

                            "correct":
                                correct,

                            "concept":
                                question["concept"],

                            "explanation":
                                question["explanation"]
                        }
                    )

                # Save results in session

                st.session_state.quiz_results = results

                total = len(
                    st.session_state.quiz
                )

                percentage = (
                    correct_count /
                    total
                ) * 100

                # Save progress

                save_quiz_result(
                    correct_count,
                    total,
                    list(
                        set(weak_topics)
                    )
                )

                # --------------------------------------------------
                # RESULT
                # --------------------------------------------------

                st.divider()

                st.subheader(
                    "🏆 Quiz Result"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "✅ Correct",
                        correct_count
                    )

                with col2:

                    st.metric(
                        "📝 Total",
                        total
                    )

                with col3:

                    st.metric(
                        "🎯 Score",
                        f"{percentage:.1f}%"
                    )

                st.progress(
                    percentage / 100
                )

                if percentage >= 80:

                    st.success(
                        "🎉 Excellent performance!"
                    )

                elif percentage >= 50:

                    st.warning(
                        "👍 Good performance! "
                        "Keep practicing."
                    )

                else:

                    st.error(
                        "📚 More revision is recommended."
                    )

                # --------------------------------------------------
                # ANSWER REVIEW
                # --------------------------------------------------

                st.divider()

                st.subheader(
                    "📋 Answer Review"
                )

                for result in results:

                    if result["correct"]:

                        st.success(
                            f"✅ {result['question']}"
                        )

                        st.write(
                            f"Your answer: "
                            f"**{result['selected']}**"
                        )

                    else:

                        st.error(
                            f"❌ {result['question']}"
                        )

                        st.write(
                            f"Your answer: "
                            f"**{result['selected']}**"
                        )

                        st.write(
                            f"Correct answer: "
                            f"**{result['correct_answer']}**"
                        )

                    st.info(
                        f"💡 {result['explanation']}"
                    )

                # --------------------------------------------------
                # WEAK TOPICS
                # --------------------------------------------------

                if weak_topics:

                    st.divider()

                    st.subheader(
                        "🎯 Topics to Practice"
                    )

                    for topic in sorted(
                        set(weak_topics)
                    ):

                        st.warning(
                            f"📚 {topic}"
                        )


# ==========================================================
# FLASHCARDS
# ==========================================================

elif page == "🗂️ Flashcards":

    st.subheader(
        "🗂️ AI Flashcards"
    )

    st.write(
        "Generate AI-powered flashcards "
        "for quick revision."
    )

    if not st.session_state.notes.strip():

        st.warning(
            "⚠️ Please add study material first."
        )

    else:

        number = st.slider(
            "Number of flashcards",
            min_value=3,
            max_value=15,
            value=5
        )

        # --------------------------------------------------
        # GENERATE FLASHCARDS
        # --------------------------------------------------

        if st.button(
            "🪄 Generate Flashcards",
            type="primary"
        ):

            with st.spinner(
                "🧠 Creating flashcards..."
            ):

                cards = generate_flashcards(
                    st.session_state.notes,
                    number
                )

            if cards:

                st.session_state.flashcards = cards

                st.success(
                    f"✅ {len(cards)} flashcards created!"
                )

            else:

                st.error(
                    "❌ Could not generate flashcards. "
                    "Please try again."
                )

        # --------------------------------------------------
        # DISPLAY FLASHCARDS
        # --------------------------------------------------

        if st.session_state.flashcards:

            st.divider()

            st.subheader(
                "📚 Revision Cards"
            )

            for index, card in enumerate(
                st.session_state.flashcards,
                1
            ):

                with st.expander(
                    f"📌 Card {index}: "
                    f"{card['question']}"
                ):

                    st.markdown(
                        "### ❓ Question"
                    )

                    st.write(
                        card["question"]
                    )

                    st.divider()

                    st.markdown(
                        "### 💡 Answer"
                    )

                    st.success(
                        card["answer"]
                    )

                    st.caption(
                        f"🧠 Concept: "
                        f"{card['concept']}"
                    )

            # --------------------------------------------------
            # DOWNLOAD FLASHCARDS
            # --------------------------------------------------

            flashcard_text = ""

            for index, card in enumerate(
                st.session_state.flashcards,
                1
            ):

                flashcard_text += (
                    f"FLASHCARD {index}\n\n"
                    f"Question: "
                    f"{card['question']}\n\n"
                    f"Answer: "
                    f"{card['answer']}\n\n"
                    f"Concept: "
                    f"{card['concept']}\n"
                    f"{'-' * 60}\n\n"
                )

            st.download_button(
                "⬇️ Download Flashcards",
                flashcard_text,
                file_name="AI_Flashcards.txt",
                mime="text/plain"
            )


# ==========================================================
# WEAK CONCEPTS
# ==========================================================

elif page == "🎯 Weak Concepts":

    st.subheader(
        "🎯 AI Weak Concept Detector"
    )

    st.write(
        "This section identifies concepts where "
        "you repeatedly make mistakes."
    )

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    if not history:

        st.info(
            "📝 Complete at least one quiz "
            "to detect weak concepts."
        )

    else:

        concept_stats = {}

        # --------------------------------------------------
        # COUNT MISTAKES
        # --------------------------------------------------

        for attempt in history:

            for topic in attempt.get(
                "weak_topics",
                []
            ):

                if topic not in concept_stats:

                    concept_stats[topic] = 0

                concept_stats[topic] += 1

        if not concept_stats:

            st.success(
                "🎉 No weak concepts detected!"
            )

        else:

            st.write(
                "The following concepts caused "
                "mistakes across your quiz attempts."
            )

            sorted_topics = sorted(
                concept_stats.items(),
                key=lambda x: x[1],
                reverse=True
            )

            # --------------------------------------------------
            # DISPLAY WEAK CONCEPTS
            # --------------------------------------------------

            for topic, mistakes in sorted_topics:

                if mistakes >= 3:

                    status = "🔴 High Priority"

                elif mistakes == 2:

                    status = "🟠 Needs Practice"

                else:

                    status = "🟡 Review"

                col1, col2, col3 = st.columns(
                    [4, 2, 1]
                )

                with col1:

                    st.write(
                        f"📚 **{topic}**"
                    )

                with col2:

                    st.write(
                        status
                    )

                with col3:

                    st.metric(
                        "Mistakes",
                        mistakes
                    )

            # --------------------------------------------------
            # TOP PRIORITY
            # --------------------------------------------------

            st.divider()

            most_weak = sorted_topics[0]

            st.warning(
                f"🎯 **Top Priority:** "
                f"{most_weak[0]}"
            )

            st.info(
                "### Recommended Action\n\n"
                "1. 📖 Review the concept\n\n"
                "2. 🧠 Ask AI for a simple explanation\n\n"
                "3. 🗂️ Create flashcards\n\n"
                "4. ❓ Retake the quiz\n\n"
                "5. 📈 Check your progress"
            )

            # --------------------------------------------------
            # AI RECOMMENDATION
            # --------------------------------------------------

            if st.button(
                "🤖 Generate AI Recommendation"
            ):

                weak_topics = [
                    topic
                    for topic, mistakes
                    in sorted_topics
                ]

                with st.spinner(
                    "🧠 AI is analyzing your weak areas..."
                ):

                    recommendation = (
                        generate_learning_recommendation(
                            weak_topics,
                            0
                        )
                    )

                st.markdown(
                    recommendation
                )


# ==========================================================
# STUDY PLAN
# ==========================================================

elif page == "🧠 Study Plan":

    st.subheader(
        "🧠 AI Personalized Study Plan"
    )

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    weak_topics = []

    for attempt in history:

        weak_topics.extend(
            attempt.get(
                "weak_topics",
                []
            )
        )

    weak_topics = list(
        dict.fromkeys(
            weak_topics
        )
    )

    if weak_topics:

        st.write(
            "🎯 Your detected weak topics:"
        )

        for topic in weak_topics:

            st.warning(
                f"📚 {topic}"
            )

    else:

        st.info(
            "No weak topics detected yet. "
            "The plan will focus on general revision."
        )

    study_hours = st.slider(
        "⏰ Study hours per day",
        min_value=1,
        max_value=8,
        value=2
    )

    if st.button(
        "🧠 Generate Study Plan",
        type="primary"
    ):

        with st.spinner(
            "🧠 Creating personalized study plan..."
        ):

            # Local planner

            plan = create_plan(
                weak_topics,
                study_hours
            )

        st.markdown(plan)

        st.divider()

        # AI enhanced recommendation

        if weak_topics:

            with st.spinner(
                "🤖 AI is improving your study strategy..."
            ):

                ai_plan = generate_study_plan(
                    weak_topics,
                    study_hours
                )

            st.subheader(
                "🤖 AI Learning Recommendation"
            )

            st.markdown(
                ai_plan
            )


# ==========================================================
# PROGRESS
# ==========================================================

elif page == "📈 Progress":

    st.subheader(
        "📈 Learning Progress"
    )

    stats = get_progress_statistics()

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    # ------------------------------------------------------
    # MAIN METRICS
    # ------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🎯 Latest Score",
            f"{stats['latest_score']}%"
        )

    with col2:

        st.metric(
            "📊 Average Score",
            f"{stats['average_score']}%"
        )

    with col3:

        st.metric(
            "🏆 Best Score",
            f"{stats['best_score']}%"
        )

    with col4:

        st.metric(
            "🔥 Learning Streak",
            f"{stats['streak']} days"
        )

    st.divider()

    # ------------------------------------------------------
    # ADDITIONAL METRICS
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📝 Quiz Attempts",
            stats["quiz_attempts"]
        )

    with col2:

        total_minutes = stats["total_minutes"]

        hours = total_minutes // 60

        minutes = total_minutes % 60

        st.metric(
            "⏱️ Study Time",
            f"{hours}h {minutes}m"
        )

    st.divider()

    # ------------------------------------------------------
    # IMPROVEMENT
    # ------------------------------------------------------

    if stats["improvement"] > 0:

        st.success(
            f"📈 Your latest score improved by "
            f"{stats['improvement']} percentage points."
        )

    elif stats["improvement"] < 0:

        st.warning(
            f"📉 Your latest score decreased by "
            f"{abs(stats['improvement'])} percentage points."
        )

    else:

        st.info(
            "📊 Take another quiz to measure improvement."
        )

    # ------------------------------------------------------
    # SCORE HISTORY
    # ------------------------------------------------------

    if history:

        st.divider()

        st.subheader(
            "📊 Quiz Score History"
        )

        scores = [
            item.get(
                "percentage",
                0
            )
            for item in history
        ]

        chart_df = pd.DataFrame(
            {
                "Quiz Attempt":
                    range(
                        1,
                        len(scores) + 1
                    ),

                "Score":
                    scores
            }
        )

        st.line_chart(
            chart_df.set_index(
                "Quiz Attempt"
            )
        )

        # --------------------------------------------------
        # DETAILED HISTORY
        # --------------------------------------------------

        st.divider()

        st.subheader(
            "📋 Detailed Quiz History"
        )

        for index, item in enumerate(
            reversed(history),
            1
        ):

            attempt_number = (
                len(history) - index + 1
            )

            percentage = item.get(
                "percentage",
                0
            )

            with st.expander(
                f"Quiz Attempt "
                f"{attempt_number} "
                f"— {percentage}%"
            ):

                st.write(
                    f"📅 Date: "
                    f"{item.get('date', 'Unknown')}"
                )

                st.write(
                    f"Correct: "
                    f"{item.get('correct', 0)} / "
                    f"{item.get('total', 0)}"
                )

                st.progress(
                    min(
                        percentage / 100,
                        1.0
                    )
                )

                weak = item.get(
                    "weak_topics",
                    []
                )

                if weak:

                    st.write(
                        "🎯 Weak Topics:"
                    )

                    for topic in weak:

                        st.write(
                            f"• {topic}"
                        )


# ==========================================================
# STUDY TIMER
# ==========================================================

elif page == "⏱️ Study Timer":

    st.subheader(
        "⏱️ Study Session Timer"
    )

    st.write(
        "Record the amount of time you spend studying."
    )

    minutes = st.number_input(
        "⏱️ Study session duration (minutes)",
        min_value=1,
        max_value=180,
        value=25
    )

    st.info(
        f"Recommended session: "
        f"{minutes} minutes"
    )

    if st.button(
        "✅ Record Study Session",
        type="primary"
    ):

        add_study_session(
            int(minutes)
        )

        st.success(
            f"✅ {minutes} minute study session recorded!"
        )


# ==========================================================
# BOOKMARKS
# ==========================================================

elif page == "📌 Bookmarks":

    st.subheader(
        "📌 Bookmarked Topics"
    )

    topic = st.text_input(
        "📌 Topic to bookmark",
        placeholder="Example: Python Inheritance"
    )

    if st.button(
        "📌 Add Bookmark"
    ):

        if topic.strip():

            add_bookmark(
                topic.strip()
            )

            st.success(
                "✅ Topic bookmarked!"
            )

            st.rerun()

        else:

            st.warning(
                "Please enter a topic."
            )

    data = load_data()

    bookmarks = data.get(
        "bookmarks",
        []
    )

    if bookmarks:

        st.divider()

        for index, bookmark in enumerate(
            bookmarks
        ):

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                st.write(
                    f"📌 **{bookmark}**"
                )

            with col2:

                if st.button(
                    "Remove",
                    key=f"remove_bookmark_{index}"
                ):

                    remove_bookmark(
                        bookmark
                    )

                    st.rerun()

    else:

        st.info(
            "No bookmarked topics yet."
        )


# ==========================================================
# STUDY REPORT
# ==========================================================

elif page == "📄 Study Report":

    st.subheader(
        "📄 AI Study Report"
    )

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    bookmarks = data.get(
        "bookmarks",
        []
    )

    study_sessions = data.get(
        "study_sessions",
        []
    )

    stats = get_progress_statistics()

    # ------------------------------------------------------
    # LATEST RESULT
    # ------------------------------------------------------

    if history:

        latest = history[-1]

        score = latest.get(
            "percentage",
            0
        )

        weak_topics = latest.get(
            "weak_topics",
            []
        )

    else:

        score = 0

        weak_topics = []

    # ------------------------------------------------------
    # REPORT PREVIEW
    # ------------------------------------------------------

    st.subheader(
        "📊 Report Preview"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🎯 Latest Score",
            f"{score}%"
        )

    with col2:

        st.metric(
            "📊 Average Score",
            f"{stats['average_score']}%"
        )

    with col3:

        st.metric(
            "🏆 Best Score",
            f"{stats['best_score']}%"
        )

    with col4:

        st.metric(
            "📝 Quiz Attempts",
            stats["quiz_attempts"]
        )

    st.divider()

    # ------------------------------------------------------
    # STUDY TIME
    # ------------------------------------------------------

    total_minutes = stats[
        "total_minutes"
    ]

    hours = total_minutes // 60

    minutes = total_minutes % 60

    st.info(
        f"⏱️ Total Study Time: "
        f"**{hours} hours {minutes} minutes**"
    )

    # ------------------------------------------------------
    # WEAK CONCEPTS
    # ------------------------------------------------------

    st.subheader(
        "🎯 Weak Concepts"
    )

    if weak_topics:

        for topic in weak_topics:

            st.warning(
                f"📚 {topic}"
            )

    else:

        st.success(
            "🎉 No weak concepts recorded."
        )

    st.divider()

    # ------------------------------------------------------
    # BOOKMARKS
    # ------------------------------------------------------

    st.subheader(
        "📌 Bookmarked Topics"
    )

    if bookmarks:

        for bookmark in bookmarks:

            st.write(
                f"📌 {bookmark}"
            )

    else:

        st.write(
            "No bookmarks available."
        )

    st.divider()

    # ------------------------------------------------------
    # REPORT SUMMARY
    # ------------------------------------------------------

    st.subheader(
        "✏️ Report Summary"
    )

    report_summary = st.text_area(
        "Enter additional comments",
        value=(
            "This report summarizes my learning "
            "performance using AI Study Buddy."
        ),
        height=150
    )

    # ------------------------------------------------------
    # GENERATE PDF
    # ------------------------------------------------------

    if st.button(
        "📄 Generate PDF Report",
        type="primary"
    ):

        with st.spinner(
            "📄 Creating your study report..."
        ):

            filepath = create_report(
                "study_report.pdf",
                score,
                report_summary,
                weak_topics,
                history,
                bookmarks,
                study_sessions
            )

        try:

            with open(
                filepath,
                "rb"
            ) as file:

                pdf_data = file.read()

            st.download_button(
                "⬇️ Download Study Report",
                pdf_data,
                file_name="AI_Study_Buddy_Report.pdf",
                mime="application/pdf"
            )

            st.success(
                "✅ Your study report is ready!"
            )

        except Exception as error:

            st.error(
                f"❌ Could not prepare PDF: {error}"
            )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "🎓 AI Study Buddy | "
    "Python + Streamlit + NLP + "
    "Machine Learning + Llama 3.2 + Ollama"
)