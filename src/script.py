import sys
import spacy
import numpy as np
import matplotlib.pyplot as plt

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Plot Templates
plot_templates = {
    "line": """import numpy as np\nimport matplotlib.pyplot as plt\nx = np.linspace(-10, 10, 100)\ny = {y}\nplt.plot(x, y)\nplt.xlabel('x')\nplt.ylabel('y')\nplt.title('Line Graph')\nplt.show()""",
    "scatter": """import numpy as np\nimport matplotlib.pyplot as plt\nx = np.linspace(-10, 10, 100)\ny = {y}\nplt.scatter(x, y)\nplt.xlabel('x')\nplt.ylabel('y')\nplt.title('Scatter Plot')\nplt.show()""",
    "bar": """import numpy as np\nimport matplotlib.pyplot as plt\nx = np.arange(len({y}))\ny = {y}\nplt.bar(x, y)\nplt.xlabel('x')\nplt.ylabel('y')\nplt.title('Bar Chart')\nplt.show()"""
}

def identify_plot_type_and_features(description):
    doc = nlp(description.lower())
    plot_type = None
    features = {"x": "x", "y": "x**2"}  # Default values for the example provided

    # Simple NLP to identify plot type and features
    for token in doc:
        if token.text in plot_templates:
            plot_type = token.text
        elif token.dep_ in ["pobj", "dobj"]:  # Depending on your NLP logic
            if "x" not in features:
                features["x"] = token.text
            else:
                features["y"] = token.text
    
    return plot_type, features

def generate_code(description):
    plot_type, features = identify_plot_type_and_features(description)
    if plot_type in plot_templates:
        # Transform the 'y' expression into a format that Python understands
        y_expression = features['y'].replace('^', '**')  # Replace '^' with '**' for exponentiation
        code = plot_templates[plot_type].format(y=y_expression)
        return code
    else:
        return "Plot type not supported."

if __name__ == "__main__":
    description = sys.argv[1] if len(sys.argv) > 1 else "Plot a line graph of y=x^2"
    generated_code = generate_code(description)
    print(generated_code)
