import random
import re

def analyze_resume(text):
    word_count = len(text.split())
    char_count = len(text)

    skills_pool = [
        "Python", "JavaScript", "TypeScript", "React", "Node.js", "SQL", "AWS",
        "Docker", "Git", "REST APIs", "Machine Learning", "Data Analysis",
        "Java", "C++", "CSS", "HTML", "Linux", "PostgreSQL", "MongoDB",
        "Kubernetes", "CI/CD", "Agile", "Scrum", "TensorFlow", "Pandas"
    ]

    missing_skills_pool = [
        "Cloud Architecture (AWS/GCP/Azure)",
        "System Design principles",
        "Containerization (Docker/Kubernetes)",
        "CI/CD pipeline experience",
        "Unit and integration testing",
        "Technical documentation",
        "GraphQL APIs",
        "Microservices architecture",
        "Performance optimization",
        "Security best practices"
    ]

    roles_pool = [
        "Software Engineer", "Full Stack Developer", "Backend Developer",
        "Frontend Developer", "Data Engineer", "DevOps Engineer",
        "Machine Learning Engineer", "Platform Engineer", "Site Reliability Engineer",
        "Technical Lead", "Solutions Architect"
    ]

    detected_skills = [s for s in skills_pool if s.lower() in text.lower()]
    if len(detected_skills) < 4:
        detected_skills = random.sample(skills_pool, random.randint(4, 7))

    score = min(95, max(45, 50 + len(detected_skills) * 3 + min(word_count // 50, 20)))

    missing = random.sample(missing_skills_pool, random.randint(2, 4))
    roles = random.sample(roles_pool, random.randint(3, 5))

    strengths = []
    if any(s in text.lower() for s in ["experience", "worked", "developed", "built"]):
        strengths.append("Clear demonstration of hands-on project experience")
    if word_count > 200:
        strengths.append("Well-detailed resume with sufficient depth")
    if len(detected_skills) >= 4:
        strengths.append(f"Strong technical skill set ({', '.join(detected_skills[:4])})")
    if any(s in text.lower() for s in ["team", "collaborate", "led", "managed"]):
        strengths.append("Evidence of teamwork and collaboration skills")
    if not strengths:
        strengths = [
            "Resume is clearly structured and readable",
            "Shows initiative in technical areas",
            "Good foundational skill set presented"
        ]

    weaknesses = []
    if word_count < 150:
        weaknesses.append("Resume is brief — consider expanding on project descriptions")
    if not any(s in text.lower() for s in ["github", "portfolio", "linkedin"]):
        weaknesses.append("No portfolio or GitHub profile mentioned")
    if not any(s in text.lower() for s in ["achievement", "improved", "increased", "reduced", "%"]):
        weaknesses.append("Lacks quantified achievements (e.g., 'reduced load time by 30%')")
    weaknesses.append("Could benefit from a dedicated summary/objective section")
    if len(weaknesses) < 2:
        weaknesses.append("Work experience descriptions could be more impact-focused")

    report = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI RESUME ANALYSIS REPORT  (Demo Mode)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 RESUME SCORE: {score}/100
{'★' * (score // 20)}{'☆' * (5 - score // 20)}  {'Excellent' if score >= 85 else 'Good' if score >= 70 else 'Average' if score >= 55 else 'Needs Work'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ STRENGTHS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(f'  • {s}' for s in strengths)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  WEAKNESSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(f'  • {w}' for w in weaknesses)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 DETECTED SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {', '.join(detected_skills)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ MISSING / RECOMMENDED SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(f'  • {m}' for m in missing)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💼 RECOMMENDED ROLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(f'  • {r}' for r in roles)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 RESUME STATS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Word count   : {word_count}
  Skills found : {len(detected_skills)}
  Role matches : {len(roles)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Note: This is a demo analysis generated locally.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return report
