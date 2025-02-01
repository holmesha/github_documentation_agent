from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

README_SECTIONS = [
    ("project_name", "Project Name"),
    ("description", "Short Description"),
    ("features", "Key Features"),
    ("installation", "Installation Steps"),
    ("usage", "Usage Examples"),
    ("tech_stack", "Technology Stack"),
    ("contributing", "Contributing Guidelines"),
    ("license", "License Information"),
    ("screenshots", "Screenshot URLs"),
    ("tests", "Test Instructions"),
    ("code_overview", "Main Code Reference")  # New section
]

SECTION_TEMPLATES = {
    "installation": "```bash\npip install your-package\n```",
    "usage": "```python\nimport your_module\n\n# Example usage\nresult = your_module.run()\n```",
    "contributing": "1. Fork the repository\n2. Create your feature branch\n3. Commit changes\n4. Open a pull request",
    "tech_stack": "Python, JavaScript, Flask, OpenAI API",
    "license": "MIT | Apache 2.0 | GPL-3.0",
    "tests": "```bash\npytest tests/\n```",
    "code_overview": "# Paste your main code snippets here\n\ndef main():\n    print('Hello World')\n\nif __name__ == '__main__':\n    main()"
}

@app.route('/')
def index():
    return render_template('index.html', sections=README_SECTIONS)

@app.route('/get_template/<section>')
def get_template(section):
    return jsonify({"template": SECTION_TEMPLATES.get(section, "")})

def create_readme_prompt(user_inputs):
    """Construct prompt with code context"""
    prompt = "Generate professional README.md using GitHub Markdown with these guidelines:\n"
    
    # Handle code reference
    if code := user_inputs.get("code_overview", "").strip():
        prompt += f"CODE CONTEXT (use for examples but don't mention this section):\n{code}\n\n"
    
    # Handle other sections
    for key, label in README_SECTIONS:
        if key != "code_overview" and (content := user_inputs.get(key, '').strip()):
            prompt += f"## {label}\n{content}\n\n"
    
    return prompt + """Formatting rules:
1. Use code context for accurate examples
2. Keep examples consistent with provided code
3. Use proper Markdown with emojis in headings
4. Never include the code context section"""

@app.route('/generate', methods=['POST'])
def generate_readme():
    try:
        user_inputs = request.form.to_dict()
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a documentation expert that creates READMEs matching provided code."},
                {"role": "user", "content": create_readme_prompt(user_inputs)}
            ],
            temperature=0.7,
            max_tokens=1200
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return jsonify({"error": f"API Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999, debug=True)
