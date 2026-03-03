from dotenv import load_dotenv

load_dotenv()

import aisuite as ai

# Define the client. You can use this variable inside your graded functions!
CLIENT = ai.Client()

# GRADED FUNCTION: generate_draft

def generate_draft(topic: str, model: str = "openai:gpt-4o") -> str: 
    
    ### START CODE HERE ###

    # Define your prompt here. A multi-line f-string is typically used for this.
    prompt = f"""
    Here is the topic I want you to work on, topic:{topic}
    I want you to write an essay on the topic. the output should be returned in a string format.
    """

    ### END CODE HERE ###
    
    # Get a response from the LLM by creating a chat with the client.
    response = CLIENT.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
    )

    return response.choices[0].message.content
# GRADED FUNCTION: reflect_on_draft

def reflect_on_draft(draft: str, model: str = "openai:o4-mini") -> str:

    ### START CODE HERE ###

    # Define your prompt here. A multi-line f-string is typically used for this.
    prompt = f"""
    Here is the draft of the essay: 
    {draft}
    provide feedbacks on the draft based on following criteria:
    1. The feedback should be critical but constructive.
    2. It should address issues such as structure, clarity, strength of argument, and writing style.
    3. The function should send the draft to the model and return its response.
    """

    ### END CODE HERE ###

    # Get a response from the LLM by creating a chat with the client.
    response = CLIENT.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
    )
    return response.choices[0].message.content

# GRADED FUNCTION: revise_draft

def revise_draft(original_draft: str, reflection: str, model: str = "openai:gpt-4o") -> str:

    ### START CODE HERE ###

    # Define your prompt here. A multi-line f-string is typically used for this.
    prompt = f"""
    We get our original_draft: {original_draft} and our reflection: {reflection} on
    how to improve the original draft. I want you to use the reflection to improve the draft, and make
    a verison 2 for me
    """

    # Get a response from the LLM by creating a chat with the client.
    response = CLIENT.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
    )
    ### END CODE HERE ###

    return response.choices[0].message.content
essay_prompt = "Should social media platforms be regulated by the government?"

# Agent 1 – Draft
draft = generate_draft(essay_prompt)
print("📝 Draft:\n")
print(draft)

# Agent 2 – Reflection
feedback = reflect_on_draft(draft)
print("\n🧠 Feedback:\n")
print(feedback)

# Agent 3 – Revision
revised = revise_draft(draft, feedback)
print("\n✍️ Revised:\n")
print(revised)

from utils import show_output

essay_prompt = "Should social media platforms be regulated by the government?"

show_output("Step 1 – Draft", draft, background="#fff8dc", text_color="#333333")
show_output("Step 2 – Reflection", feedback, background="#e0f7fa", text_color="#222222")
show_output("Step 3 – Revision", revised, background="#f3e5f5", text_color="#222222")