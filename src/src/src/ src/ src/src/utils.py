def get_confidence_color(c):
    if c >= 0.8: return "green"
    if c >= 0.6: return "orange"
    return "red"

def parse_confidence_level(c):
    if c >= 0.8: return "High"
    if c >= 0.6: return "Medium"
    return "Low"
