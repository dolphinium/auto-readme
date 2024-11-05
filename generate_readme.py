import os
from openai import OpenAI
import nbformat


def summarize_code_files():
    summaries = ""
    generator_script = 'generate_readme.py'  # Name of the script generating README files

    for root, _, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip the README generator script itself
            if file == generator_script:
                continue

            if file.endswith(('.py', '.js', '.java', '.cpp', '.md')) and file != 'README.md':
                summary = summarize_code(file_path)
                summaries += summary + "\n\n"
            elif file.endswith('.ipynb'):
                # Process notebook files
                summary = summarize_notebook(file_path)
                summaries += summary + "\n\n"
    
    return summaries



def summarize_notebook(file_path):
    """Extracts content from a Jupyter Notebook file and returns a summary."""
    with open(file_path, 'r') as file:
        notebook = nbformat.read(file, as_version=4)
    
    summary = f"Notebook: {file_path}\n"
    
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            # Add first few lines of each markdown cell
            summary += "Markdown:\n" + "\n".join(cell.source.splitlines()[:3]) + "\n\n"
        elif cell.cell_type == "code":
            # Add first few lines of each code cell
            code_snippet = "\n".join(cell.source.splitlines()[:3])  # Limit to 3 lines
            summary += f"Code:\n```python\n{code_snippet}\n```\n\n"
            
            # Optionally, add output if available
            if cell.outputs:
                for output in cell.outputs:
                    if 'text' in output:
                        summary += f"Output:\n{output['text'][:100]}...\n\n"  # Truncate long outputs
                    elif 'data' in output and 'text/plain' in output['data']:
                        summary += f"Output:\n{output['data']['text/plain'][:100]}...\n\n"
    
    return summary

def summarize_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    # Truncate code to avoid exceeding token limits
    truncated_code = code[:2000]  # Adjust as needed
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
        max_tokens=3000,
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
