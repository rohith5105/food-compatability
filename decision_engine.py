FOOD_NUTRIENTS = {
    "rice": {"carbs": 28},
    "egg": {"protein": 13},
    "curd": {"protein": 3, "calcium": 120},
    "spinach": {"fiber": 2.2, "iron": 2.7},
    "banana": {"carbs": 23},
    "lentils": {"protein": 9, "fiber": 8},
    "vegetables": {"fiber": 3},
    "soup": {"water": 200}
}

DAILY_NEEDS = {
    "protein": 50,
    "fiber": 25
}


def calculate_nutrients(meal):
    total = {}
    for food in meal["foods"]:
        if food in FOOD_NUTRIENTS:
            for nutrient, value in FOOD_NUTRIENTS[food].items():
                total[nutrient] = total.get(nutrient, 0) + value
    return total


def detect_nutrient_gaps(total_nutrients):
    missing = []
    for nutrient, required in DAILY_NEEDS.items():
        if total_nutrients.get(nutrient, 0) < required:
            missing.append(nutrient)
    return missing


def suggest_foods(missing_nutrients, user):
    suggestions = []

    if "fiber" in missing_nutrients:
        suggestions.append("vegetables")

    if "protein" in missing_nutrients:
        suggestions.append("lentils")

    if user["time"] == "night":
        suggestions = [s for s in suggestions if s != "banana"]

    return suggestions[:3]


def short_term_effects(user, risk_type):
    if user["time"] == "night" and risk_type == "heavy":
        return "Heaviness, bloating, or disturbed sleep"
    if user["digestion"] == "low" and risk_type == "fermented":
        return "Acidity or stomach discomfort"
    return "Normal digestion"


def long_term_effects(risk_type):
    if risk_type == "fermented":
        return "May worsen digestive imbalance if eaten frequently"
    if risk_type == "heavy":
        return "May contribute to metabolic stress over time"
    return "No known long-term issues if eaten in moderation"


def can_i_eat(user, meal):

    if user["season"] == "winter" and "watermelon" in meal["foods"]:
        return {
            "decision": "EAT_WITH_CAUTION",
            "why": "Cooling foods are not ideal in winter",
            "short_term": short_term_effects(user, "fermented"),
            "long_term": long_term_effects("fermented"),
            "alternative": "Warm fruits or cooked vegetables"
        }

    if user["time"] == "night" and "curd" in meal["foods"]:
        return {
            "decision": "EAT_WITH_CAUTION",
            "why": "Fermented foods digest slowly at night",
            "short_term": short_term_effects(user, "fermented"),
            "long_term": long_term_effects("fermented"),
            "alternative": "Light warm food or soup"
        }

    if "acidity" in user["conditions"] and "curd" in meal["foods"]:
        return {
            "decision": "EAT_WITH_CAUTION",
            "why": "Fermented food may increase acidity",
            "short_term": short_term_effects(user, "fermented"),
            "long_term": long_term_effects("fermented"),
            "alternative": "Warm cooked vegetables"
        }

    if "curd" in meal["foods"] and "egg" in meal["foods"]:
        return {
            "decision": "EAT_WITH_CAUTION",
            "why": "Protein and fermented dairy digest at different speeds",
            "short_term": short_term_effects(user, "heavy"),
            "long_term": long_term_effects("heavy"),
            "alternative": "Egg with vegetables"
        }

    total_nutrients = calculate_nutrients(meal)
    missing = detect_nutrient_gaps(total_nutrients)
    suggested = suggest_foods(missing, user)

    return {
        "decision": "EAT",
        "why": "No major risk detected for your profile",
        "short_term": "Normal digestion",
        "long_term": "No known long-term issues if eaten in moderation",
        "alternative": ", ".join(suggested)
    }


# -------- TEST --------
user = {
    "conditions": ["acidity"],
    "season": "summer",
    "time": "morning",
    "digestion": "low"
}

meal = {
    "foods": ["rice"]
}

print(can_i_eat(user, meal))
