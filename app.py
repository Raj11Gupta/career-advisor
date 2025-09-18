from flask import Flask, jsonify, request
import csv

# 1. Initialize the Flask App
app = Flask(__name__)

# --- LOGIC FOR SCENARIO B: CAREER RECOMMENDATION ---
def find_career_from_csv(user_skill_names):
    try:
        with open('careers.csv', mode='r', encoding='utf-8') as csv_file:
            careers_data = list(csv.DictReader(csv_file))
        
        with open('rules.csv', mode='r', encoding='utf-8') as csv_file:
            rules_data = list(csv.DictReader(csv_file))

    except FileNotFoundError:
        return {"error": "Make sure 'careers.csv' and 'rules.csv' are in the same folder as app.py."}

    career_scores = {}
    
    for rule in rules_data:
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

# --- LOGIC FOR SCENARIO A: CAREER GAP ANALYSIS (NEWLY ADDED) ---
def perform_gap_analysis(chosen_career_id, user_skill_names):
    try:
        with open('rules.csv', mode='r', encoding='utf-8') as csv_file:
            rules_data = list(csv.DictReader(csv_file))
    except FileNotFoundError:
        return {"error": "The rules.csv file was not found."}

    # Find all skills required for the user's chosen career
    required_skills = []
    for rule in rules_data:
        if rule['CareerID'] == chosen_career_id:
            required_skills.append(rule['SkillName'])
    
    if not required_skills:
        return {"error": f"Career ID '{chosen_career_id}' not found in rules.csv."}
        
    # Compare lists to find what the user has and what they need to learn
    skills_you_have = list(set(required_skills) & set(user_skill_names))
    skills_to_learn = list(set(required_skills) - set(user_skill_names))
    
    # Reuse our other function to find career paths based on the user's current skills
    skill_based_recommendation = find_career_from_csv(user_skill_names)
    
    return {
        "chosenCareerId": chosen_career_id,
        "skillsYouHave": skills_you_have,
        "skillsToLearn": skills_to_learn,
        "skillBasedPaths": [skill_based_recommendation] if skill_based_recommendation else []
    }

# --- API ENDPOINTS ---

# Endpoint for Scenario B (Suggest a career) - NO CHANGES
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
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

# Endpoint for Scenario A (Gap analysis) - NEWLY ADDED
@app.route('/gap-analysis', methods=['POST'])
def gap_analysis_endpoint():
    data = request.get_json()
    user_skill_names = data.get('skill_names', [])
    chosen_career_id = data.get('career_id', None)

    if not user_skill_names or not chosen_career_id:
        return jsonify({"error": "Both 'skill_names' and 'career_id' are required"}), 400

    analysis_result = perform_gap_analysis(chosen_career_id, user_skill_names)
    
    if "error" in analysis_result:
        return jsonify(analysis_result), 404
        
    return jsonify(analysis_result)

# --- Test Route and App Start ---

@app.route('/')
def hello_world():
    return jsonify({"message": "Server is running!"})

if __name__ == '__main__':
    app.run(debug=True)