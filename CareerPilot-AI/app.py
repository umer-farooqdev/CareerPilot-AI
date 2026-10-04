import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

CAREER_DATA = {
    "AI Engineer": {"keywords": ["python", "artificial intelligence", "math", "problem solving", "machine learning"], "skills": ["Python", "Linear algebra basics", "Machine learning", "Prompt engineering", "Model evaluation"], "projects": ["Rule-based chatbot", "Student performance predictor", "Document Q&A assistant"]},
    "Data Analyst": {"keywords": ["data", "statistics", "excel", "sql", "charts", "analysis"], "skills": ["Excel", "SQL", "Statistics", "Python pandas", "Data visualization"], "projects": ["Student marks dashboard", "Sales data analysis", "Public dataset report"]},
    "Software Developer": {"keywords": ["coding", "programming", "web", "apps", "logic", "java", "javascript"], "skills": ["Programming fundamentals", "Git and GitHub", "Data structures", "APIs", "Testing"], "projects": ["Task manager", "Expense tracker", "Portfolio website"]},
    "Cybersecurity Analyst": {"keywords": ["security", "networks", "privacy", "linux", "investigation"], "skills": ["Networking basics", "Linux", "Security fundamentals", "Python scripting", "Incident reporting"], "projects": ["Password strength checker", "Phishing awareness guide", "Log analysis demo"]},
    "UI/UX Designer": {"keywords": ["design", "creative", "visual", "user experience", "figma", "layout"], "skills": ["User research", "Wireframing", "Figma", "Accessibility", "Usability testing"], "projects": ["Redesign a university portal", "Mobile app prototype", "Usability review"]},
}


def fallback_recommendations(interests, skills, education, goal):
    text = f"{interests} {skills} {education} {goal}".lower()
    scored = []
    for career, data in CAREER_DATA.items():
        score = sum(1 for keyword in data["keywords"] if keyword in text)
        scored.append((score, career, data))
    scored.sort(key=lambda item: item[0], reverse=True)
    chosen = scored[:3]
    results = []
    for score, career, data in chosen:
        results.append({
            "title": career,
            "match": min(95, 55 + score * 8),
            "reason": f"This path may fit your stated interests and skills related to {', '.join(data['keywords'][:3])}.",
            "skills": data["skills"],
            "projects": data["projects"],
            "roadmap": [
                f"Week 1: Learn the fundamentals of {data['skills'][0]}.",
                f"Week 2: Practice {data['skills'][1]} with small exercises.",
                f"Week 3: Build a mini-project using {data['skills'][2]}.",
                f"Week 4: Finish one portfolio project and document it on GitHub."
            ]
        })
    return results


def get_ai_recommendations(interests, skills, education, goal):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return fallback_recommendations(interests, skills, education, goal), "demo"
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f'''You are CareerPilot AI, a supportive career exploration assistant for students. Return exactly 3 realistic career paths based on the student profile below. Do not claim the suggestions are guaranteed or scientifically validated. Keep the advice practical and beginner-friendly. Return valid JSON only, with this shape: {{"careers":[{{"title":"Career name","match":75,"reason":"2 short sentences","skills":["skill 1","skill 2","skill 3","skill 4","skill 5"],"projects":["project 1","project 2","project 3"],"roadmap":["Week 1: ...","Week 2: ...","Week 3: ...","Week 4: ..."]}}]}}. Match should be an approximate relevance indicator from 50 to 95, not a probability.
Student education: {education}
Interests: {interests}
Current skills: {skills}
Goal: {goal}
'''
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        import json
        raw = response.text.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        elif raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        data = json.loads(raw.strip())
        careers = data.get("careers", [])[:3]
        if not careers:
            raise ValueError("No careers returned")
        for item in careers:
            item["match"] = max(50, min(95, int(item.get("match", 70))))
            item.setdefault("skills", [])
            item.setdefault("projects", [])
            item.setdefault("roadmap", [])
            item.setdefault("reason", "Explore this option further to see whether it fits your interests.")
        return careers, "ai"
    except Exception as error:
        print("Gemini API error; using demo recommendations:", error)
        return fallback_recommendations(interests, skills, education, goal), "demo"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "Student").strip()[:60] or "Student"
        education = request.form.get("education", "Undergraduate")[:100]
        interests = request.form.get("interests", "").strip()[:500]
        skills = request.form.get("skills", "").strip()[:500]
        goal = request.form.get("goal", "Explore career options").strip()[:300]
        if not interests or not skills:
            return render_template("index.html", error="Please enter your interests and current skills.", form=request.form)
        careers, mode = get_ai_recommendations(interests, skills, education, goal)
        return render_template("results.html", name=name, careers=careers, mode=mode)
    return render_template("index.html", error=None, form={})


if __name__ == "__main__":
    import threading
    import webbrowser

    url = "http://localhost:5000"

    threading.Timer(
        1.5,
        lambda: webbrowser.open(url)
    ).start()

    app.run(debug=True, use_reloader=False)