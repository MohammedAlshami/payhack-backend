from flask import Flask, jsonify, request
import json
from urllib.parse import unquote  # Import to decode URL-encoded strings
from flask_cors import CORS  # Import Flask-Cors

app = Flask(__name__)
CORS(app)


# Endpoint to fetch all P2P companies
@app.route('/api/get-all-p2p', methods=['GET'])
def get_all_p2p():
    with open('loans.json', 'r') as file:
        data = json.load(file)

    # Filter out records where type is 'bank'
    filtered_data = [record for record in data if record.get('type') != 'bank']

    return jsonify(filtered_data)

# Endpoint to fetch all banks
@app.route('/api/get-all-banks', methods=['GET'])
def get_all_banks():
    with open('loans.json', 'r') as file:
        data = json.load(file)

    # Filter out records where type is 'bank'
    filtered_data = [record for record in data if record.get('type') == 'bank']

    return jsonify(filtered_data)
# Endpoint to fetch a specific P2P company by name
@app.route('/api/get-p2p-company', methods=['GET'])
def get_p2p_company():
    company_name = request.args.get('name').strip('"')
    print(company_name)
    if company_name:
        company_name = unquote(company_name)  # Decode the URL-encoded company name
    with open('p2p_companies.json', 'r') as file:
        data = json.load(file)
        # Filter the data to find the matching company (case-insensitive)
        company = next((item for item in data if item["companyName"].lower() == company_name.lower()), None)
    if company:
        return jsonify(company)
    else:
        return jsonify({"error": "Company not found"}), 404

# Endpoint to fetch a specific bank by name
@app.route('/api/get-bank', methods=['GET'])
def get_bank():
    company_name = request.args.get('name')
    if company_name:
        company_name = unquote(company_name).strip('"')  # Decode the URL-encoded company name
    print(company_name)
    with open('banks.json', 'r') as file:
        data = json.load(file)
        # Filter the data to find the matching company (case-insensitive)
        company = next((item for item in data if item["companyName"].lower() == company_name.lower()), None)
    if company:
        return jsonify(company)
    else:
        return jsonify({"error": "Company not found"}), 404


@app.route('/api/get-loan-data', methods=['GET'])
def get_loan_data():
    with open('loans.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/api/get-loan-details', methods=['GET'])
def get_loan_details():
    company_name = request.args.get('name')
    if company_name:
        company_name = unquote(company_name).strip("'")  # Decode URL and strip quotes if needed

    with open('loans.json', 'r') as file:
        data = json.load(file)

    # Search for the company by name (case-insensitive)
    company = next((item for item in data if item["companyName"].lower() == company_name.lower()), None)

    if company:
        return jsonify(company)
    else:
        return jsonify({"error": "Company not found"}), 404
    
    

@app.route('/api/get-requests', methods=['GET'])
def get_loan_requests():
    # Load the loan data from the JSON file
    try:
        with open('requests.json', 'r') as file:
            loan_data = json.load(file)
        return jsonify(loan_data)
    except FileNotFoundError:
        return jsonify({"error": "Loan data not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error reading loan data"}), 500
     
# Endpoint to add a new loan request
# Endpoint to add a new loan request
@app.route('/api/add-request', methods=['POST'])
def add_loan_request():
    try:
        # Get the JSON data from the request
        new_request = request.get_json()

        # Validate the incoming data (ensure company and details are provided)
        if 'company' not in new_request or 'details' not in new_request:
            return jsonify({"error": "Missing field: company or details"}), 400

        company_name = new_request['company']
        details = new_request['details']

        # Load P2P companies data
        with open('p2p_companies.json', 'r') as file:
            companies_data = json.load(file)

        # Find the company by companyName (case-insensitive)
        company = next((item for item in companies_data if item["companyName"].lower() == company_name.lower()), None)

        if not company:
            return jsonify({"error": f"Company '{company_name}' not found"}), 404

        # Add the details to the company data
        company['details'] = details

        # Load existing loan requests from the JSON file
        with open('requests.json', 'r') as file:
            data = json.load(file)

        # Append the updated company data (with the new details) to the requests
        data.append(company)

        # Save the updated data back to the JSON file
        with open('requests.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Return a success response
        return jsonify({"message": "Loan request added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to add a new loan record to loans.json
@app.route('/api/add-loan', methods=['POST'])
def add_loan():
    try:
        # Get the JSON data from the request
        new_loan = request.get_json()
        print(new_loan)

        # Load existing loan data from loans.json
        with open('loans.json', 'r') as file:
            loans_data = json.load(file)

        # Append the new loan to the data
        loans_data.append(new_loan)

        # Save the updated data back to loans.json
        with open('loans.json', 'w') as file:
            json.dump(loans_data, file, indent=4)

        # Return a success response
        return jsonify({"message": "Loan record added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
