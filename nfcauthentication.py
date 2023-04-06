import nfc
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Predefined hash values for authorized NFC tags
AUTHORIZED_TAGS = {
    "tag1": "Example1",
    "tag2": "Example2",
    "tag3": "Example3",
    # Add more authorized tags here
}

def authenticate(tag_id):

    hashed_id = hashlib.sha256(tag_id.encode()).hexdigest()
    if hashed_id in AUTHORIZED_TAGS.values():
        return True
    return False

@app.route("/api/authenticate", methods=["POST"])
def api_authenticate():
    try:
        tag_id = request.json["tag_id"]
        if authenticate(tag_id):
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Authentication failed, unauthorised."})
    except:
        return jsonify({"success": False, "message": "Invalid request."})

def on_connect(tag):
    try:
        tag_id = tag.identifier.hex()
        if authenticate(tag_id):
            print("Authentication successful!")
        else:
            print("Authentication failed.")
    except Exception as e:
        print(e)


clf = nfc.ContactlessFrontend()


clf.connect(rdwr={'on-connect': on_connect})

if __name__ == "__main__":
    app.run(debug=True)