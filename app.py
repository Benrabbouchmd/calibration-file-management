import os
import re
from flask import Flask, request
from db import db
from models import CalibrationFile
import hashlib

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calibration.db"
db.init_app(app)

# Create the tables in the database for the first time
with app.app_context():
    db.create_all()

# Get the path to the folder containing calibration files
calibration_folder_path = os.path.join(os.path.dirname(__file__), "calibrationfiles")


# API endpoint to read and store calibration files
@app.route("/api/calibration/store", methods=["POST"])
def api_read_and_store_cfs():
    try:
        # Iterate over all files in the calibration folder
        for file in os.listdir(calibration_folder_path):
            # Check if the file is a text file
            if file.endswith(".txt"):
                # Get the full path to the file
                file_path = os.path.join(calibration_folder_path, file)

                # Calculate the hash of the file
                file_hash = hashlib.md5(open(file_path, "rb").read()).hexdigest()

                # Check if the file already exists in the database
                existing_cf = CalibrationFile.query.filter_by(
                    file_hash=file_hash
                ).first()

                # If the file does not exist in the database, add it
                if not existing_cf:
                    with open(file_path, "r") as f:
                        content = f.read()

                        # Extract metadata from the file name
                        match = re.match(r"Pandora(\d+)s(\d+)_CF_v(\d+)d(\d+)", file)
                        if match:
                            pandora_id, spectrometer_id, version, validity_date = (
                                match.groups()
                            )

                            cf = CalibrationFile(
                                pandora_id=pandora_id,
                                spectrometer_id=spectrometer_id,
                                version=version,
                                validity_date=validity_date,
                                content=content,
                                file_hash=file_hash,
                            )

                            db.session.add(cf)

        db.session.commit()

    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return {"exception": f"Failed to read and store CFs: {e}"}, 500

    return {"message": "CFs read and stored successfully"}


# API endpoint to get all calibration files
@app.route("/api/calibration", methods=["GET"])
def get_cfs():
    try:
        # Get the search query and ID from the request arguments
        query = request.args.get("search")
        cf_id = request.args.get("id")

        # If a search query is provided, filter the results
        if query:
            results = CalibrationFile.query.filter(
                CalibrationFile.content.like(f"%{query}%")
            ).all()
            return [
                {
                    "id": result.id,
                    "pandora_id": result.pandora_id,
                    "spectrometer_id": result.spectrometer_id,
                    "version": result.version,
                    "validity_date": result.validity_date,
                    "content": result.content,
                    "created_at": result.created_at,
                    "updated_at": result.updated_at,
                }
                for result in results
            ]

        # If an ID is provided, get the corresponding calibration file
        if cf_id:
            result = CalibrationFile.query.get(cf_id)

            if not result:
                return {"error": "CF not found"}, 404

            return {
                "id": result.id,
                "pandora_id": result.pandora_id,
                "spectrometer_id": result.spectrometer_id,
                "version": result.version,
                "validity_date": result.validity_date,
                "content": result.content,
                "created_at": result.created_at,
                "updated_at": result.updated_at,
            }

        # If no search query or ID is provided, return all calibration files
        results = CalibrationFile.query.all()
        return [
            {
                "id": result.id,
                "pandora_id": result.pandora_id,
                "spectrometer_id": result.spectrometer_id,
                "version": result.version,
                "validity_date": result.validity_date,
                "content": result.content,
                "created_at": result.created_at,
                "updated_at": result.updated_at,
            }
            for result in results
        ]

    except Exception as e:
        return {"exception": f"Failed to get CFs: {e}"}, 500


#  endpoint to query the content of calibration files
@app.route("/api/calibration/content", methods=["GET"])
def query_content():
    try:
        query = request.args.get("query")

        if not query:
            return {"error": "Please provide a query parameter"}, 400

        # Get all calibration files
        results = CalibrationFile.query.all()
        query_results = []

        # Iterate over the calibration files and extract the content
        for result in results:
            content_lines = result.content.splitlines()
            for line in content_lines:
                key_value_pair = line.split("->")
                if len(key_value_pair) == 2:
                    key = key_value_pair[0].strip()
                    value = key_value_pair[1].strip()

                    # If the key matches the query, add the result to the query results
                    if key == query:
                        query_results.append(
                            {
                                "cf_id": result.id,
                                "key": key,
                                "value": value,
                            }
                        )

        return query_results

    except Exception as e:
        return {"exception": f"Failed to get CFs: {e}"}, 500

if __name__ == "__main__":
    app.run(debug=False)
