from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

#BONUS: Added query search for minEpisodes (COMPLETED)
@app.route("/shows", defaults = {"minEpisodes": None}, methods=['GET'])
@app.route("/shows?minEpisodes=<num>")
def min_or_all(minEpisodes):

    #Get all shows due to removed get_all_shows() function
    allShows = create_response({"shows": db.get('shows')})

    #showList: List used to store shows that match query
    showList = []

    #If url has to query results, show all shows
    if request.args.get("minEpisodes") == None:
        return allShows
    
    #If url has query results for minEpisodes
    else:

        #Retrieve minEpisodes value
        minEpisodes = request.args.get("minEpisodes")

        #If minEpisodes = 0, show all shows
        if int(minEpisodes) == 0:
            return allShows

        #Iterate through each show in 'shows' and check if episodes_seen match query
        id = 1
        show = db.getById("shows", id)
        while show:
            episodes = int(show["episodes_seen"])
            if episodes >= int(minEpisodes):
                showList.append(show)
            id += 1
            show = db.getById("shows", id)
        
        #Check if list is empty
        if len(showList) == 0:
            #Return error message
            return create_response(status=404, message="There are no shows with more that {} episodes seen".format(minEpisodes))
        else:
            #Return showList with query results
            return create_response({"shows":showList})

#Removed get_all_shows() to test for query search
#def get_all_shows():
    #return create_response({"shows": db.get('shows')})

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!
@app.route("/shows/<id>", methods=['GET'])
def get_show(id):

    #If requested id is not found
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="The requested URL was not found.")
    
    #Return requested show 
    return create_response(data = db.getById("shows", int(id)))

@app.route("/shows", methods=['POST'])
def post_show():

    #Get data from Postman
    payload = request.json

    #Retrieve name and episodes_seen from payload
    name = payload["name"]
    episodes_seen = payload["episodes_seen"]
    
    #If name or episodes_seen variables are not set correctly
    if name == "":
        return create_response(status=422, message="The name field is empty, enter a show name.")
    elif episodes_seen == "":
        return create_response(status=422, message="The episodes_seen field is empty, enter episodes seen.")
    
    #Format new show parameters to match mock_db
    newShow = {"id": 0, "name": name, "episodes_seen": episodes_seen}

    #Assign new id for new show
    newShowId = db.create('shows', newShow)

    #Print new show
    return jsonify(newShowId)

@app.route("/shows/<id>", methods=['PUT'])
def put_show(id):

    #If requested id is not found
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="The requested URL was not found.")

    #Get data from Postman
    payload = request.json

    #Store original show data if only 1 variable is to be updated
    originalShow = db.getById("shows", int(id))
    originalName = originalShow["name"]
    originalEp = str(originalShow["episodes_seen"])

    #Check if name or episodes_seen is to be updated
    if "name" in payload:
        name = payload["name"]
    else:
        name = originalName
    if "episodes_seen" in payload:
        episodes_seen = payload["episodes_seen"]
    else:
        episodes_seen = originalEp
    
    #Format data into dict
    updateShow = {"id": int(id), "name": name, "episodes_seen": episodes_seen}

    #Update show
    updatedShow = db.updateById('shows', int(id), updateShow)
    
    #Return updated show
    return jsonify(updatedShow)
    
"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
