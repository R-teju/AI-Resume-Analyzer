def generate_suggestions(score):

    suggestions = []

    if score < 40:
        suggestions.append("Add more technical skills relevant to the job")
        suggestions.append("Include projects related to the role")
        suggestions.append("Improve resume keyword optimization")

    elif score < 70:
        suggestions.append("Add more measurable achievements")
        suggestions.append("Include advanced technical tools")

    else:
        suggestions.append("Resume is strong for this job role")

    return suggestions