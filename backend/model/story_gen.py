# model/story_gen.py

def generate_story(keywords):
    if not keywords:
        return "No keywords were provided to generate a story."

    joined = ", ".join(keywords)
    return f"Once upon a time, a story began with {joined}. It was a journey filled with wonder, mystery, and surprise. The end."
