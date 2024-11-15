import os
from dotenv import load_dotenv
from RufusClient.parser import Parser
from RufusClient.synthesizer import Synthesizer
import json

load_dotenv()

sample_content = """
<html>
<head><title>Statistics Overview</title></head>
<body>
    <h1>Statistics Overview</h1>
    <p>This page provides an overview of key statistical concepts.</p>
    <div class="section">
        <h2>Variance</h2>
        <p>Variance measures the dispersion of a set of data points around their mean value.</p>
        <p>The formula for variance (σ²) is: 
           <em>σ² = Σ (xi - μ)² / N</em>, where <em>xi</em> is each value, <em>μ</em> is the mean, and <em>N</em> is the number of values.
        </p>
        <p>Variance is used to determine how much the data varies. A high variance indicates that data points are spread out over a wider range of values.</p>
    </div>
    <div class="section">
        <h2>Standard Deviation</h2>
        <p>The standard deviation is the square root of variance and provides a measure of the average distance of each data point from the mean.</p>
    </div>
    <div class="section">
        <h2>Examples of Variance</h2>
        <p>For example, the variance of a dataset with values [2, 4, 4, 4, 5, 5, 7, 9] is calculated as follows...</p>
    </div>
    <div class="section">
        <h2>Applications of Variance</h2>
        <p>Variance is used in finance to measure the risk of a stock portfolio.</p>
        <p>It is also utilized in machine learning algorithms for model evaluation.</p>
    </div>
</body>
</html>
"""



sample_prompt = "Identify and extract all relevant sections related to standard deviation, including definitions, formulas, examples, and applications."


api_key = os.getenv('OPENAI_API_KEY')

parser = Parser(content=sample_content, user_prompt=sample_prompt, api_key=api_key)

extracted_data = parser.extract_relevant_sections()
print("Extracted Data:")
print(extracted_data)

synthesizer = Synthesizer(extracted_data=extracted_data, user_prompt=sample_prompt, api_key=api_key)

synthesized_data = synthesizer.synthesize()
print("Synthesized Data:")
print(json.dumps(synthesized_data, indent=4))
