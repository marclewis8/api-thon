from flask import Flask, render_template, request
from requests import get
from api import grab_url
from random import choice

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "POST":    # True if index.html grabbed info from user via form or button

        # Here is where we can set variables used by both random and dropdown methods
        is_planet: bool = True
        object_name: str = str(request.form['object_name'])

        # TODO: if object is chosen via randomness, pick a random name!
        if object_name == "I'm feeling lucky":
            space_res = get("https://api.le-systeme-solaire.net/rest/bodies/")
            object_name = (choice(space_res.json()['bodies']))['name']
            is_planet = False

        # TODO: make your api request for the object (either specified by user or random)
        refined_res = get(f"https://api.le-systeme-solaire.net/rest/bodies/{object_name}")
        data = refined_res.json()

        # TODO: populate args to send to result.html (object_name, moons, temp, discovered_by, discovery_date, and url)
        temp: float = data["avgTemp"]
        discovered_by: str = data["discoveredBy"]
        discovery_date: str = data["discoveryDate"]
        moons: list[str] = []
        url: str = grab_url(object_name, is_planet)

        if data["moons"] != None:
            for entry in data["moons"]:
                moons.append(entry['moon'])

        # helps with error handling
        if object_name == '':
            return render_template("index.html")

        # rendering result template with all of our fields generated by our API call!
        return render_template("result.html", object_name=object_name, moons=moons, temp=temp, discovered_by=discovered_by, discovery_date=discovery_date, url=url)

    # if request method != post, render original page
    return render_template('index.html')


# flask idiom
if __name__ == '__main__':
    app.run(debug=True)