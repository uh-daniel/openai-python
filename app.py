import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]



app = Flask(__name__,
    template_folder='templates'        
)

def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes.
    You should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.

    Q: Convert the following verbal description of a color palette into a list of colors: a beautiful sunset
    A: ["#FE4C40", "#EC9F6D", "#FFA983", "#BE3144", "#69356D", "#E9A8B3","#FFEDD2"]

    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature and earth
    A: ["#587A6F","#A3AF97","#2A5948","#3B8F8F","#8EB9A3","#4F5845","#9DBF98","#6C7E62"]

    Desired Format: a JSON array of hexadecimal color codes

    Text: ocean tones

    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A: 
    """

    response = openai.Completion.create(
        prompt=prompt,
        model="text-davinci-003",
        max_tokens=200,
    )

    colors = json.loads(response["choices"][0]["text"])
    return colors

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
