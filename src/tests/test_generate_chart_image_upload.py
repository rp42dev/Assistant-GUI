import os
import json
from dotenv import load_dotenv
from assistant.tools.chart_generation_tool import ChartGenerationTool

# Load environment variables
load_dotenv()

# Test data for the chart
test_argument = json.dumps({
    "chart_type": "pie",
    "data": [40, 60],
    "labels": ["Aged 25-35", "Aged 36-45"]
})

# Initialize the tool
chart_tool = ChartGenerationTool()

# Run the tool with the test argument
result = chart_tool._run(test_argument)

# Print the result (this should be the image URL)
print(result)