from src.analyzer import SECTION_WEIGHTS, calculate_skill_match
from src.comparator import calculate_similarity


def calculate_weighted_score(
    semantic_score,
    job_skills,
    resume_skills,
    section_scores=None,
    semantic_weight=0.65,
    skills_weight=0.25,
    sections_weight=0.10,
):
    """
    Combina similitud semantica, coincidencia de habilidades y secciones del CV.
    """
    skill_match = calculate_skill_match(job_skills, resume_skills)
    section_score = _aggregate_section_scores(section_scores or {})

    components = {
        "semantic": semantic_score,
        "skills": skill_match["score"],
        "sections": section_score,
    }

    active_weights = {"semantic": semantic_weight}
    if skill_match["score"] is not None:
        active_weights["skills"] = skills_weight
    if section_score is not None:
        active_weights["sections"] = sections_weight

    total_weight = sum(active_weights.values())
    final_score = 0

    for key, weight in active_weights.items():
        final_score += components[key] * (weight / total_weight)

    return {
        "final_score": round(final_score, 2),
        "semantic_score": semantic_score,
        "skill_score": skill_match["score"],
        "section_score": section_score,
        "matched_skills": skill_match["matched"],
        "missing_skills": skill_match["missing"],
        "extra_skills": skill_match["extra"],
    }


def calculate_section_scores(job_text, resume_sections, model_name=None):
    """
    Evalua la similitud entre la oferta y cada seccion detectada del CV.
    """
    scores = {}
    for section, content in resume_sections.items():
        if content.strip():
            scores[section] = calculate_similarity(job_text, content, model_name)
    return scores


def _aggregate_section_scores(section_scores):
    weighted_sum = 0
    used_weight = 0

    for section, score in section_scores.items():
        weight = SECTION_WEIGHTS.get(section, 0)
        if weight > 0:
            weighted_sum += score * weight
            used_weight += weight

    if used_weight == 0:
        return None

    return round(weighted_sum / used_weight, 2)


def build_explanation(score_data, max_items=6):
    """
    Genera explicaciones breves para el dashboard del reclutador.
    """
    matched = score_data["matched_skills"][:max_items]
    missing = score_data["missing_skills"][:max_items]

    if matched:
        matched_text = ", ".join(matched)
    else:
        matched_text = "No se detectaron habilidades requeridas de forma explicita"

    if missing:
        missing_text = ", ".join(missing)
    else:
        missing_text = "Sin brechas explicitas en la taxonomia detectada"

    return {
        "coincidencias": matched_text,
        "brechas": missing_text,
        "resumen": (
            f"Similitud semantica: {score_data['semantic_score']}%. "
            f"Skills: {_format_optional_score(score_data['skill_score'])}. "
            f"Secciones: {_format_optional_score(score_data['section_score'])}."
        ),
    }


def _format_optional_score(score):
    if score is None:
        return "no evaluado"
    return f"{score}%"
