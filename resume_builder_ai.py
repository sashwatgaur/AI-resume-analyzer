import random

ACTION_VERBS = [
    "Developed", "Built", "Designed", "Implemented", "Led", "Architected",
    "Optimized", "Delivered", "Launched", "Improved", "Reduced", "Increased",
    "Streamlined", "Automated", "Spearheaded", "Collaborated", "Managed",
    "Created", "Deployed", "Engineered", "Established", "Executed", "Drove",
    "Integrated", "Migrated", "Monitored", "Oversaw", "Produced", "Resolved"
]

WEAK_STARTERS = ["i ", "we ", "the ", "a ", "an ", "worked on", "helped with",
                 "did ", "was responsible for", "responsible for", "assisted"]

SKILLS_BY_ROLE = {
    "software engineer":    ["Python", "Java", "Docker", "Kubernetes", "REST APIs", "Git", "CI/CD", "AWS"],
    "frontend developer":   ["React", "TypeScript", "CSS", "HTML", "Next.js", "Webpack", "Jest", "Figma"],
    "backend developer":    ["Node.js", "Python", "PostgreSQL", "Redis", "Docker", "REST APIs", "GraphQL", "AWS"],
    "full stack developer": ["React", "Node.js", "PostgreSQL", "Docker", "TypeScript", "AWS", "REST APIs", "Git"],
    "data engineer":        ["Python", "SQL", "Spark", "Airflow", "dbt", "BigQuery", "Kafka", "AWS"],
    "data scientist":       ["Python", "TensorFlow", "PyTorch", "Pandas", "Scikit-learn", "SQL", "Jupyter", "MLflow"],
    "devops engineer":      ["Docker", "Kubernetes", "Terraform", "AWS", "CI/CD", "Linux", "Ansible", "Prometheus"],
    "machine learning":     ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "MLflow", "Docker", "SQL", "Spark"],
    "product manager":      ["Agile", "Scrum", "JIRA", "Roadmapping", "A/B Testing", "SQL", "Figma", "OKRs"],
    "ux designer":          ["Figma", "Sketch", "Adobe XD", "User Research", "Wireframing", "Prototyping", "CSS"],
}


def enhance_bullet(bullet: str) -> str:
    bullet = bullet.strip()
    if not bullet:
        return bullet
    lower = bullet.lower()
    for weak in WEAK_STARTERS:
        if lower.startswith(weak):
            rest = bullet[len(weak):].strip()
            rest = rest[0].lower() + rest[1:] if rest else rest
            bullet = f"{random.choice(ACTION_VERBS)} {rest}"
            break
    if bullet and bullet[0].islower():
        bullet = bullet[0].upper() + bullet[1:]
    return bullet


def generate_summary(personal: dict, experience: list, skills: list) -> str:
    name = personal.get("name", "").split()[0] if personal.get("name") else "Professional"
    role = ""
    years = 0
    if experience:
        role = experience[0].get("role", "")
        years = len(experience)

    skill_sample = ", ".join(skills[:4]) if skills else "various technologies"

    templates = [
        f"Results-driven {role or 'professional'} with {years}+ year{'s' if years != 1 else ''} of hands-on experience building impactful solutions. Proficient in {skill_sample}. Passionate about writing clean, maintainable code and delivering measurable business value.",
        f"Dynamic {role or 'professional'} experienced in {skill_sample}. Proven track record of delivering high-quality work across {years}+ role{'s' if years != 1 else ''}. Adept at working in fast-paced environments and collaborating across teams.",
        f"Versatile {role or 'professional'} with expertise in {skill_sample}. Committed to continuous learning and technical excellence, with experience spanning {years}+ professional role{'s' if years != 1 else ''}. Strong communicator and collaborative team player.",
    ]
    return random.choice(templates)


def suggest_skills(role: str, current_skills: list) -> list:
    role_lower = role.lower()
    suggestions = []
    for key, skills in SKILLS_BY_ROLE.items():
        if key in role_lower or role_lower in key:
            for s in skills:
                if s not in current_skills:
                    suggestions.append(s)
    return suggestions[:5]


def enhance_resume_data(data: dict) -> dict:
    personal = data.get("personal", {})
    experience = data.get("experience", [])
    skills = data.get("skills", [])
    projects = data.get("projects", [])

    if not personal.get("summary") and experience:
        personal["summary"] = generate_summary(personal, experience, skills)

    enhanced_exp = []
    for exp in experience:
        raw_bullets = exp.get("bullets", [])
        enhanced_bullets = [enhance_bullet(b) for b in raw_bullets if b.strip()]
        enhanced_exp.append({**exp, "bullets": enhanced_bullets})

    enhanced_proj = []
    for proj in projects:
        desc = proj.get("description", "")
        enhanced_proj.append({**proj, "description": enhance_bullet(desc) if desc else desc})

    role = experience[0].get("role", "") if experience else ""
    suggested = suggest_skills(role, skills)

    return {
        **data,
        "personal": personal,
        "experience": enhanced_exp,
        "projects": enhanced_proj,
        "suggested_skills": suggested,
    }
