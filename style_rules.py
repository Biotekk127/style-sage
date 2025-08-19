from typing import Dict, Any, List
import math

# Very simple rules engine that merges image stats + survey into a profile.
# You can later swap this for an ML model.

OCCASION_TO_STYLES = {
    "work": ["Business Casual", "Smart Casual"],
    "school": ["Casual", "Athleisure"],
    "dates": ["Smart Casual", "Chic Minimalist"],
    "nights_out": ["Streetwear", "Trendy"],
    "weddings": ["Modern Formal"],
    "interviews": ["Business Formal", "Smart Casual"],
    "travel": ["Comfy Minimalist", "Athleisure"],
}

GOAL_TO_STYLES = {
    "look_taller": ["Monochrome Minimalist", "Slim-Fit Modern"],
    "more_muscular": ["Structured Streetwear", "Layered Casual"],
    "professional": ["Business Casual", "Smart Casual"],
    "expressive": ["Streetwear", "Eclectic"],
    "low_maintenance": ["Minimalist", "Capsule Wardrobe"],
}

PALETTE_TO_STYLES = {
    "Neutral / Minimalist": ["Minimalist", "Modern Classic", "Capsule Wardrobe"],
    "Soft / Earthy": ["Scandi Casual", "Workwear", "Smart Casual"],
    "Bold / Vibrant": ["Streetwear", "Trendy", "Sport Luxe"],
}

def _merge_unique(lists: List[List[str]]) -> List[str]:
    seen = set()
    out = []
    for lst in lists:
        for x in lst:
            if x not in seen:
                seen.add(x)
                out.append(x)
    return out

def _fit_tips(brightness: float, saturation: float) -> List[str]:
    tips = []
    if brightness < 0.35:
        tips.append("Use lighter tops to brighten your look and draw focus upward.")
    else:
        tips.append("Balance light tops with darker bottoms for definition.")
    if saturation < 0.2:
        tips.append("Introduce a small accent color (belt, hat, sneakers) to add interest.")
    else:
        tips.append("Anchor bold colors with one neutral piece to avoid clashing.")
    return tips

def _color_tips(palette_name: str, survey: Dict[str, Any]) -> List[str]:
    prefs = survey.get("colorPrefs") or []
    tips = []
    if palette_name == "Neutral / Minimalist":
        tips.append("Lean into blacks, whites, greys, navy, and olive.")
    elif palette_name == "Soft / Earthy":
        tips.append("Try tan, camel, cream, sage, and rust for warmth.")
    else:
        tips.append("Lean into saturated hues; keep silhouette clean to avoid noise.")
    if prefs:
        tips.append(f"Incorporate your preferred colors: {', '.join(prefs)}.")
    return tips

def _occasion_list(survey: Dict[str, Any]) -> List[str]:
    raw = survey.get("primaryOccasions") or []
    # normalize
    occ_map = {
        "Work": "work", "School":"school", "Dates":"dates",
        "Nights Out":"nights_out", "Weddings":"weddings",
        "Interviews":"interviews", "Travel":"travel"
    }
    out = []
    for x in raw:
        out.append(occ_map.get(x, x).lower())
    return out

def _goal_list(survey: Dict[str, Any]) -> List[str]:
    raw = survey.get("styleGoals") or []
    goal_map = {
        "Look taller":"look_taller",
        "Look more muscular":"more_muscular",
        "More professional":"professional",
        "Be more expressive":"expressive",
        "Low maintenance":"low_maintenance",
    }
    out = []
    for x in raw:
        out.append(goal_map.get(x, x).lower())
    return out

def generate_style_recommendation(img_stats: Dict[str, Any], survey: Dict[str, Any]) -> Dict[str, Any]:
    palette_name = img_stats.get("palette_name", "Neutral / Minimalist")
    brightness = img_stats.get("brightness", 0.5)
    saturation = img_stats.get("saturation", 0.2)

    occs = _occasion_list(survey)
    goals = _goal_list(survey)

    from_palette = PALETTE_TO_STYLES.get(palette_name, [])
    from_occs = _merge_unique([OCCASION_TO_STYLES.get(o, []) for o in occs])
    from_goals = _merge_unique([GOAL_TO_STYLES.get(g, []) for g in goals])

    # Rank styles by occurrences
    tally = {}
    for s in from_palette + from_occs + from_goals:
        tally[s] = tally.get(s, 0) + 1

    ranked = sorted(tally.items(), key=lambda kv: kv[1], reverse=True)
    top_styles = [s for s,_ in ranked][:5]

    tips = _fit_tips(brightness, saturation) + _color_tips(palette_name, survey)

    # Basic capsule suggestions by palette
    if palette_name == "Neutral / Minimalist":
        capsule = ["White tee", "Black slim jeans", "Navy overshirt", "Grey hoodie", "White sneakers", "Black boots"]
    elif palette_name == "Soft / Earthy":
        capsule = ["Cream knit", "Olive chinos", "Sage overshirt", "Tan chore coat", "Brown leather sneakers"]
    else:
        capsule = ["Bold graphic tee", "Black cargos", "Clean varsity jacket", "Technical windbreaker", "Statement sneakers"]

    return {
        "recommended_styles": top_styles,
        "why": {
            "palette_match": palette_name,
            "occasions": occs,
            "goals": goals
        },
        "fit_tips": tips,
        "starter_capsule": capsule
    }
