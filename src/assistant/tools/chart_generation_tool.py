import requests
import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
import matplotlib.pyplot as plt
import numpy as np
import json

# Load environment variables
load_dotenv()

class ChartGenerationTool(BaseTool):
    name: str = "Chart Generation Tool"
    description: str = (
        "This tool generates and uploads charts based on the specified chart type, data, labels, and additional chart properties. "
        "Supported chart types: bar, line, pie. "
        "The chart is saved as an image and uploaded to an external hosting service, returning the hosted image URL."
        "The input argument should be a JSON object with the following parameters: "
        "{"
        "   'chart_type': 'bar', 'line', or 'pie',"
        "   'data': [list of data values],"
        "   'labels': [list of labels],"
        "   'title': 'Chart title',"
        "   'xlabel': 'X-axis label',"
        "   'ylabel': 'Y-axis label'"
        "}"
    )

    def _run(self, argument: str) -> str:
        """Parses input, generates a chart, uploads it, and returns the URL."""
        chart_data = self._parse_argument(argument)
        if "error" in chart_data:
            return chart_data["error"]

        chart_type = chart_data.get("chart_type")
        title = chart_data.get("title")
        xlabel = chart_data.get("xlabel")
        ylabel = chart_data.get("ylabel")
        data = chart_data.get("data")
        labels = chart_data.get("labels")

        # Validate input
        if not chart_type or not data or not labels:
            return "Error: Missing required parameters (chart_type, data, or labels)."

        if not isinstance(data, list) or not isinstance(labels, list):
            return "Error: Data and labels must be provided as lists."

        # Generate the chart
        image_path = self.generate_chart(chart_type, data, labels, title, xlabel, ylabel)

        # Upload the chart and return the URL
        return self.upload_image(image_path)

    def _parse_argument(self, argument: str):
        """Parses the argument string as JSON and returns a dictionary."""
        try:
            return json.loads(argument)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format"}

    def generate_chart(self, chart_type, data, labels, title, xlabel, ylabel, output_dir="output/charts"):
        """Generates and saves a chart based on the provided parameters."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        plt.figure()

        if chart_type == "bar":
            plt.bar(labels, data)
        elif chart_type == "line":
            plt.plot(labels, data)
        elif chart_type == "pie":
            plt.pie(data, labels=labels, autopct='%1.1f%%')
        else:
            return "Error: Unsupported chart type."

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        image_name = f"chart_{np.random.randint(1000, 9999)}.png"
        image_path = os.path.join(output_dir, image_name)
        plt.savefig(image_path)
        plt.close()

        return image_path

    def upload_image(self, image_path: str) -> str:
        """Uploads the generated chart to an image hosting service and returns the URL."""
        api_url = "https://freeimage.host/api/1/upload"
        api_key = os.getenv('FREEIMAGE_HOST_API_KEY')

        if not api_key:
            return "Error: API key not found. Please set it in the .env file."

        if not os.path.exists(image_path):
            return f"Error: Image file not found at path {image_path}"

        with open(image_path, 'rb') as image_file:
            response = requests.post(api_url, files={'source': image_file}, data={'key': api_key})

        if response.status_code == 200:
            json_response = response.json()
            return json_response.get('image', {}).get('url', "Error: URL not found in response.")
        else:
            return f"Error: Unable to upload image. Status code: {response.status_code}, {response.text}"
