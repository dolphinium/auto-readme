import os
from openai import OpenAI

def summarize_code_files():
    summaries = ""
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith(('.py', '.js', '.java', '.cpp', '.md')) and file != 'README.md':
                file_path = os.path.join(root, file)
                summary = summarize_code(file_path)
                summaries += summary + "\n\n"
    return summaries

def summarize_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    # Truncate code to avoid exceeding token limits
    truncated_code = code[:1000]  # Adjust as needed
    return f"File: {file_path}\n```{truncated_code}```"

def get_dependencies():
    dependencies = ""
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as file:
            dependencies = file.read()
    elif os.path.exists('package.json'):
        # For Node.js projects
        import json
        with open('package.json', 'r') as file:
            package_json = json.load(file)
            dependencies = json.dumps(package_json.get('dependencies', {}), indent=2)
    return dependencies


def create_prompt(project_name, code_summaries, dependencies):
    prompt = f"""
You are an assistant tasked with generating a README.md file for a project called "{project_name}".

**Project Overview:**
{code_summaries}

**Dependencies:**
{dependencies}

Please generate a comprehensive README.md that includes:

- A project title and description.
- Usage examples.

Do NOT add licence part or contributing part or any exclusive part that doesn't mentioned. Also do NOT add summary what you did at the end of your response.

Ensure the README is well-formatted in Markdown and provides clear instructions to users.

"""
    return prompt


def generate_readme(prompt):
    client = OpenAI(
        api_key= os.getenv('OPENAI_API_KEY')
    )
    
    response = client.chat.completions.create(
        model='gpt-4o',  # Use 'gpt-4' if you have access
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.7,
    )
    return response.choices[0].message.content

def save_readme(content):
    with open('README.md', 'w') as file:
        file.write(content)

def main():
    #openai.api_key = os.getenv('OPENAI_API_KEY')
    
    project_name = os.path.basename(os.getcwd())
    code_summaries = summarize_code_files()
    dependencies = get_dependencies()
    prompt = create_prompt(project_name, code_summaries, dependencies)
    readme_content = generate_readme(prompt)
    save_readme(readme_content)
    print("README.md has been generated successfully.")

if __name__ == "__main__":
    main()
