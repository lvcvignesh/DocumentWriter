# app.py
import streamlit as st
import os
from agents import converse_with_retry, WRITER_MODEL_ID, CRITIC_MODEL_ID
from document_generation import write_document_section, critique_section, improve_section

def main():
    st.title("Document Generator")

    # Input for topic context
    topic_context = st.text_area("Enter the topic context:", height=200)

    # Input for sections
    st.subheader("Document Sections")
    num_sections = st.number_input("Number of sections:", min_value=1, max_value=10, value=3)
    sections = []
    for i in range(num_sections):
        section_title = st.text_input(f"Section {i+1} title:")
        section_description = st.text_area(f"Section {i+1} description:", height=100)
        sections.append({"title": section_title, "description": section_description})

    # Configuration for agents
    st.subheader("Agent Configuration")
    writer_model_id = st.text_input("Writer Model ID:", value=WRITER_MODEL_ID)
    critic_model_id = st.text_input("Critic Model ID:", value=CRITIC_MODEL_ID)

    writer_system_prompt = st.text_area("Writer System Prompt:", value="""
    You are an expert technical writer with over 25 years of experience at top tech companies. Your task is to write clear, concise, and informative technical documents. Follow these key principles:

    1. Use active voice: Avoid passive constructions to improve clarity and reduce cognitive load.
    2. Be specific and concrete: Provide clear examples and avoid vague language.
    3. Structure your content: Use headings, bullet points, and short paragraphs to improve readability.
    4. Explain technical concepts: Break down complex ideas for a broader audience without losing accuracy.
    5. Focus on the reader: Anticipate questions and provide relevant information.
    6. Stick strictly to the provided section structure and descriptions.

    Remember to tailor your writing style and content to the intended audience, whether they are beginners or experts in the field.
    Do not add any additional sections or deviate from the given structure.
    """, height=200)

    critic_system_prompt = st.text_area("Critic System Prompt:", value="""
    You are a senior technical editor with decades of experience in reviewing and improving technical documents. Your role is to provide constructive feedback and suggestions for improvement. Follow these guidelines:

    1. Assess clarity: Ensure the document is easy to understand for the intended audience.
    2. Check for active voice: Identify and suggest improvements for passive constructions.
    3. Evaluate structure: Analyze the organization of ideas and suggest improvements if needed.
    4. Verify technical accuracy: Ensure all technical information is correct and up-to-date.
    5. Consider completeness: Identify any missing information or areas that need expansion.
    6. Suggest improvements: Provide specific, actionable suggestions for enhancing the document.
    7. Ensure the document strictly adheres to the given section structure and descriptions.

    Be thorough in your critique, but also highlight the strengths of the document. Your goal is to help create the best possible version of the technical document while maintaining its intended structure.
    """, height=200)

    max_iterations_per_section = st.number_input("Max iterations per section:", min_value=1, max_value=5, value=2)

    if st.button("Generate Document"):
        output_text = "# Document\n\n"
        output_text += "This document contains the following sections:\n\n"
        for section in sections:
            output_text += f"- {section['title']}\n"
        output_text += "\n\n"

        output_area = st.empty()
        output_area.markdown(output_text)

        previous_sections = ""
        for section in sections:
            st.write(f"Writing section: {section['title']}")
            section_prompt = f"Write the following section of the technical document in Markdown format:\n\nTitle: {section['title']}\nDescription: {section['description']}\n\nEnsure that the content strictly adheres to the given title and description."
            section_content = write_document_section(section_prompt, topic_context, previous_sections, writer_system_prompt, writer_model_id)

            for i in range(max_iterations_per_section):
                st.write(f"Iteration {i + 1} for section: {section['title']}")

                critique = critique_section(section_content, section['title'], critic_system_prompt, critic_model_id)
                improved_section = improve_section(section_content, critique, section['title'], topic_context, writer_system_prompt, writer_model_id)

                # Update the section content for the next iteration
                section_content = improved_section

            output_text += f"## {section['title']}\n\n{section_content}\n\n"
            output_area.markdown(output_text)

            # Update previous_sections for context in the next section
            previous_sections += f"{section['title']}:\n{section_content}\n\n"

        st.success("Document generation complete!")

        # Add save button
        if st.button("Save Document"):
            save_path = "generated_document.md"
            with open(save_path, "w") as f:
                f.write(output_text)
            st.success(f"Document saved as {save_path}")

if __name__ == "__main__":
    main()
