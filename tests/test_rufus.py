import os
from dotenv import load_dotenv
from RufusClient.parser import Parser
from RufusClient.synthesizer import Synthesizer
import json

load_dotenv()

sample_content = """
<html>
<head><title>Machine Learning Fundamentals</title></head>
<body>
    <h1>Machine Learning Algorithms Overview</h1>
    <p>Exploring key machine learning concepts and algorithms.</p>
    
    <div class="section">
        <h2>Supervised Learning</h2>
        <p>Supervised learning is a type of machine learning where algorithms are trained on labeled data.</p>
        <p>Key algorithms include:</p>
        <ul>
            <li>Linear Regression</li>
            <li>Logistic Regression</li>
            <li>Support Vector Machines (SVM)</li>
            <li>Decision Trees</li>
        </ul>
        <p>In supervised learning, the model learns from past data to predict future outcomes.</p>
    </div>
    
    <div class="section">
        <h2>Neural Networks</h2>
        <p>Neural networks are computational models inspired by the human brain.</p>
        <p>Key components include:</p>
        <ul>
            <li>Neurons</li>
            <li>Layers (Input, Hidden, Output)</li>
            <li>Activation Functions</li>
            <li>Backpropagation</li>
        </ul>
        <p>Deep learning leverages complex neural network architectures.</p>
    </div>
    
    <div class="section">
        <h2>Model Evaluation</h2>
        <p>Techniques for assessing machine learning model performance:</p>
        <ul>
            <li>Cross-Validation</li>
            <li>Confusion Matrix</li>
            <li>Precision and Recall</li>
            <li>F1 Score</li>
        </ul>
        <p>Proper evaluation prevents overfitting and ensures model generalizability.</p>
    </div>
    
    <div class="section">
        <h2>Emerging Trends</h2>
        <p>Current advancements in machine learning include:</p>
        <ul>
            <li>Transformer Models</li>
            <li>Federated Learning</li>
            <li>Explainable AI</li>
            <li>Reinforcement Learning</li>
        </ul>
    </div>
</body>
</html>
"""



# user prompt focusing on machine learning details
sample_prompt = "Extract comprehensive information about machine learning algorithms, their types, key components, and emerging trends in the field."

api_key = os.getenv('OPENAI_API_KEY')

parser = Parser(content=sample_content, user_prompt=sample_prompt, api_key=api_key)

extracted_data = parser.extract_relevant_sections()
print("Extracted Data:")
print(extracted_data)

synthesizer = Synthesizer(extracted_data=extracted_data, user_prompt=sample_prompt, api_key=api_key)

synthesized_data = synthesizer.synthesize()
print("Synthesized Data:")
print(json.dumps(synthesized_data, indent=4))
