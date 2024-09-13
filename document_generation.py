# document_generation.py
from agents import converse_with_retry

def write_document_section(section_prompt, context, previous_sections="", system_prompt="", model_id=""):
    """Write a specific section of the document"""
    full_context = f"Context:\n{context}\n\nPrevious sections:\n{previous_sections}\n\n" if previous_sections else f"Context:\n{context}\n\n"
    messages = [
        {
            "role": "user",
            "content": [{"text": f"{full_context}{section_prompt}"}]
        }
    ]
    return converse_with_retry(messages, system=system_prompt, model_id=model_id)

def critique_section(section_content, section_title, system_prompt="", model_id=""):
    """Critique a specific section of the document"""
    messages = [
        {
            "role": "user",
            "content": [{"text": f"Analyze the following section of a technical document titled '{section_title}' and provide a detailed critique. Identify areas for improvement in terms of content, structure, clarity, and overall effectiveness. Be specific in your feedback and provide actionable suggestions. Ensure that the content adheres to the given title and doesn't deviate from the intended topic.\n\nSection Content:\n{section_content}\n\nCritique:"}]
        }
    ]
    return converse_with_retry(messages, system=system_prompt, model_id=model_id)

def improve_section(section_content, critique, section_title, context, system_prompt="", model_id=""):
    """Improve a specific section based on the given critique"""
    messages = [
        {
            "role": "user",
            "content": [{"text": f"Context:\n{context}\n\nRewrite and improve the following section of a technical document titled '{section_title}' based on the provided critique. Address all the issues raised and enhance the overall quality of the content. Ensure you maintain technical accuracy while improving clarity and structure. Provide the improved section in Markdown format. Make sure the improved content stays true to the original section title and doesn't introduce unrelated information.\n\nOriginal Section:\n{section_content}\n\nCritique:\n{critique}\n\nImproved Section:"}]
        }
    ]
    return converse_with_retry(messages, system=system_prompt, model_id=model_id)
