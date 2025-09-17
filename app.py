from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

def find_career_from_csv(user_skill_names): # Changed to skill_names
    try:
        with open('careers.csv', mode='r', encoding='utf-8') as csv_file:
            careers_data = list(csv.DictReader(csv_file))
        
        with open('rules.csv', mode='r', encoding='utf-8') as csv_file:
            rules_data = list(csv.DictReader(csv_file))

    except FileNotFoundError:
        return {"error": "Make sure 'careers.csv' and 'rules.csv' are in the same folder as app.py."}

    career_scores = {}
    
    for rule in rules_data:
        # Changed to check SkillName against user_skill_names
        if rule['SkillName'] in user_skill_names:
            career_id = rule['CareerID']
            career_scores[career_id] = career_scores.get(career_id, 0) + 1
            
    if not career_scores:
        return None 
        
    best_career_id = max(career_scores, key=career_scores.get)
    
    for career in careers_data:
        if career['CareerID'] == best_career_id:
            return career 
            
    return None

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    # Changed to get 'skill_names' from the request
    user_skill_names = data.get('skill_names', [])

    if not user_skill_names:
        return jsonify({"error": "No skill_names provided"}), 400

    matched_career = find_career_from_csv(user_skill_names)
    
    if matched_career and "error" in matched_career:
         return jsonify(matched_career), 500
         
    if matched_career:
        return jsonify(matched_career)
    else:
        return jsonify({"error": "Could not find a matching career"}), 404

@app.route('/')
def hello_world():
    return jsonify({"message": "Server is running!"})

if __name__ == '__main__':
    app.run(debug=True)