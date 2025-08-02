from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import os
from datetime import datetime
from database import db

app = Flask(__name__)
app.secret_key = 'exam_tracker_secret_key_2024'

def get_exam_syllabi():
    """Return comprehensive syllabi for all exams (copied from PrepDyno with improvements)"""
    return {
        'JEE': {
            'Physics': [
                "Units and Dimensions",
                "Vectors and Kinematics",
                "Laws of Motion",
                "Work, Energy and Power",
                "Centre of Mass and Momentum",
                "Rotational Motion and Torque",
                "Gravitation",
                "Properties of Solids and Fluids",
                "Thermal Properties and Expansion",
                "Thermodynamics and Heat Transfer",
                "Kinetic Theory of Gases",
                "Oscillations and Simple Harmonic Motion",
                "Waves and Sound",
                "Electrostatics and Electric Field",
                "Potential and Capacitance",
                "Current Electricity and Circuits",
                "Magnetic Effects of Current",
                "Magnetism and Matter",
                "Electromagnetic Induction",
                "Alternating Current",
                "Ray Optics and Optical Instruments",
                "Wave Optics",
                "Dual Nature of Matter and Radiation",
                "Atoms and Nuclei",
                "Semiconductors and Communication"
            ],
            'Chemistry': [
                "Some Basic Concepts of Chemistry",
                "Structure of Atom",
                "Periodic Table and Periodicity",
                "Chemical Bonding and Molecular Structure",
                "States of Matter: Gases and Liquids",
                "Thermodynamics",
                "Equilibrium (Chemical + Ionic)",
                "Redox Reactions",
                "Hydrogen and its Properties",
                "The s-Block and p-Block Elements",
                "The d-Block and f-Block Elements",
                "Coordination Compounds",
                "Environmental Chemistry",
                "Solid State and Solutions",
                "Electrochemistry",
                "Chemical Kinetics",
                "Surface Chemistry",
                "General Organic Chemistry",
                "Hydrocarbons",
                "Haloalkanes and Haloarenes",
                "Alcohols, Phenols and Ethers",
                "Aldehydes, Ketones and Carboxylic Acids",
                "Organic Compounds Containing Nitrogen",
                "Polymers",
                "Biomolecules",
                "Chemistry in Everyday Life",
                "Practical Chemistry"
            ],
            'Mathematics': [
                "Sets, Relations and Functions",
                "Complex Numbers and Quadratic Equations",
                "Sequences and Series",
                "Permutations and Combinations",
                "Binomial Theorem",
                "Matrices and Determinants",
                "Mathematical Induction",
                "Trigonometric Ratios and Identities",
                "Inverse Trigonometric Functions",
                "Limits and Continuity",
                "Differentiation and its Applications",
                "Integration and its Applications",
                "Differential Equations",
                "Coordinate Geometry: Lines and Circles",
                "Conic Sections: Parabola, Ellipse, Hyperbola",
                "Three Dimensional Geometry",
                "Vector Algebra",
                "Probability",
                "Statistics",
                "Mathematical Reasoning"
            ]
        },
        'IAT': {
            'Physics': [
                "Units and Dimensions",
                "Vectors and Scalars",
                "Kinematics in One and Two Dimensions",
                "Laws of Motion and Friction",
                "Work, Power and Energy",
                "Circular Motion",
                "Center of Mass and Linear Momentum",
                "Rotation and Moment of Inertia",
                "Gravitation",
                "Mechanical Properties of Solids and Fluids",
                "Simple Harmonic Motion",
                "Waves and Sound",
                "Thermal Expansion and Calorimetry",
                "Laws of Thermodynamics",
                "Kinetic Theory of Gases",
                "Electric Charge and Electric Field",
                "Gauss's Law and Potential",
                "Capacitance and Capacitors",
                "Current Electricity and Resistances",
                "Kirchhoff's Laws and Wheatstone Bridge",
                "Magnetic Effects of Current and Magnetism",
                "Electromagnetic Induction",
                "Alternating Current",
                "Ray Optics and Optical Instruments",
                "Wave Optics and Interference",
                "Dual Nature of Matter",
                "Atoms, Nuclei and Radioactivity",
                "Semiconductors and Logic Gates",
                "Experimental and Measurement-Based Questions"
            ],
            'Chemistry': [
                "Basic Concepts of Chemistry",
                "Atomic Structure and Quantum Numbers",
                "Classification of Elements and Periodicity",
                "Chemical Bonding and Molecular Structure",
                "States of Matter – Gases and Liquids",
                "Thermodynamics and Enthalpy",
                "Chemical and Ionic Equilibrium",
                "Redox Reactions",
                "Hydrogen and its Compounds",
                "The s- and p-Block Elements",
                "The d- and f-Block Elements",
                "Coordination Compounds",
                "Environmental Chemistry",
                "Basic Organic Chemistry and IUPAC Naming",
                "Hydrocarbons",
                "Haloalkanes and Haloarenes",
                "Alcohols, Phenols, and Ethers",
                "Aldehydes, Ketones and Carboxylic Acids",
                "Amines and Diazonium Salts",
                "Biomolecules (Proteins, Carbs, Nucleic Acids)",
                "Polymers",
                "Chemistry in Everyday Life",
                "Surface Chemistry",
                "Chemical Kinetics",
                "Electrochemistry",
                "Qualitative and Quantitative Analysis"
            ],
            'Mathematics': [
                "Sets, Relations and Functions",
                "Complex Numbers and Quadratic Equations",
                "Matrices and Determinants",
                "Permutations and Combinations",
                "Mathematical Induction",
                "Binomial Theorem",
                "Sequences and Series",
                "Limits, Continuity and Differentiability",
                "Differentiation and its Applications",
                "Integration and its Applications",
                "Differential Equations",
                "Coordinate Geometry: Straight Lines and Circles",
                "Conic Sections: Parabola, Ellipse and Hyperbola",
                "Three Dimensional Geometry",
                "Vector Algebra",
                "Statistics and Probability",
                "Trigonometric Functions and Identities",
                "Mathematical Reasoning and Logic"
            ],
            'Biology': [
                "Cell Structure and Function",
                "Biomolecules and Enzymes",
                "Genetics and Molecular Biology",
                "Diversity of Life Forms",
                "Plant Morphology and Anatomy",
                "Plant Physiology: Photosynthesis, Respiration",
                "Animal Physiology: Nutrition, Circulation, Excretion",
                "Human Reproduction and Reproductive Health",
                "Biotechnology: Principles and Applications",
                "Ecology and Ecosystems",
                "Biodiversity and Environmental Issues",
                "Evolution and Origin of Life",
                "Microbes in Human Welfare",
                "Health and Disease",
                "Immunology (Basic Concepts)",
                "Experimental Biology: Observation and Inference Skills"
            ]
        },
        'UGEE': {
            'Mathematics': [
                "Number Theory and Divisibility",
                "Polynomials and Remainder Theorem",
                "Functions and Graphs",
                "Complex Numbers and Geometry",
                "Trigonometry and Identities",
                "Inequalities and AM-GM",
                "Sequences, Series and Induction",
                "Binomial Theorem and Pascal's Triangle",
                "Matrices and Determinants",
                "Permutations and Combinations",
                "Probability and Counting",
                "Limits and Continuity",
                "Differentiation and its Applications",
                "Integration and its Applications",
                "Coordinate Geometry (Straight Lines, Circles)",
                "Conic Sections",
                "Vectors and 3D Geometry",
                "Linear Algebra (Basic)",
                "Logic, Proof and Reasoning",
                "Graph Theory (Basics)"
            ],
            'Physics': [
                "Units and Dimensions",
                "Vectors and Motion",
                "Newton's Laws and Applications",
                "Work, Energy and Power",
                "Circular and Rotational Motion",
                "Gravitation and Orbits",
                "Properties of Matter and Elasticity",
                "Fluid Mechanics and Buoyancy",
                "Thermal Expansion and Heat Transfer",
                "Thermodynamics and Kinetic Theory",
                "Simple Harmonic Motion and Oscillations",
                "Sound Waves and Doppler Effect",
                "Electric Field and Gauss's Law",
                "Potential and Capacitors",
                "Current and Resistance",
                "Magnetic Effects and Induction",
                "Alternating Current",
                "Ray Optics and Wave Optics",
                "Dual Nature, Atoms and Nuclei",
                "Semiconductors and Logic Gates"
            ],
            'Research Aptitude': [
                "Data Interpretation (Tables, Graphs, Charts)",
                "Pattern Recognition",
                "Logical Reasoning and Deduction",
                "Analytical Puzzles and Series",
                "Basic Programming Logic (Loops, Conditions)",
                "Number Patterns and Visual Sequences",
                "Algorithmic Thinking (Pseudocode)",
                "Problem Solving with Constraints",
                "Reading and Understanding Scientific Passages",
                "Forming and Testing Hypotheses"
            ]
        },
        'NEET': {
            'Physics': [
                "Units and Measurements",
                "Kinematics in One and Two Dimensions",
                "Laws of Motion and Friction",
                "Work, Energy and Power",
                "Rotational Motion and Moment of Inertia",
                "Gravitation and Satellite Motion",
                "Mechanical Properties of Solids",
                "Mechanical Properties of Fluids",
                "Thermal Properties of Matter",
                "Thermodynamics",
                "Kinetic Theory of Gases",
                "Oscillations and Simple Harmonic Motion",
                "Waves and Sound",
                "Electric Charges and Fields",
                "Electrostatic Potential and Capacitance",
                "Current Electricity",
                "Magnetic Effects of Current and Magnetism",
                "Electromagnetic Induction",
                "Alternating Current",
                "Ray Optics and Optical Instruments",
                "Wave Optics",
                "Dual Nature of Matter and Radiation",
                "Atoms and Nuclei",
                "Semiconductors and Communication Systems"
            ],
            'Chemistry': [
                "Some Basic Concepts of Chemistry",
                "Structure of Atom",
                "Classification of Elements and Periodicity in Properties",
                "Chemical Bonding and Molecular Structure",
                "States of Matter: Gases and Liquids",
                "Thermodynamics",
                "Equilibrium",
                "Redox Reactions",
                "Hydrogen and its Compounds",
                "The s-Block Element",
                "The p-Block Element (Group 13 and 14)",
                "Organic Chemistry - Some Basic Principles and Techniques",
                "Hydrocarbons",
                "Environmental Chemistry",
                "The Solid State",
                "Solutions",
                "Electrochemistry",
                "Chemical Kinetics",
                "Surface Chemistry",
                "The p-Block Element (Group 15, 16, 17 and 18)",
                "The d- and f-Block Elements",
                "Coordination Compounds",
                "Haloalkanes and Haloarenes",
                "Alcohols, Phenols and Ethers",
                "Aldehydes, Ketones and Carboxylic Acids",
                "Organic Compounds Containing Nitrogen",
                "Biomolecules",
                "Polymers",
                "Chemistry in Everyday Life"
            ],
            'Biology': [
                "Diversity of Living Organisms",
                "The Living World",
                "Biological Classification",
                "Plant Kingdom",
                "Animal Kingdom",
                "Structural Organisation in Animals and Plants",
                "Morphology of Flowering Plants",
                "Anatomy of Flowering Plants",
                "Structural Organisation in Animals",
                "Cell Structure and Function",
                "Cell - The Unit of Life",
                "Biomolecules",
                "Cell Cycle and Cell Division",
                "Plant Physiology",
                "Transport in Plants",
                "Mineral Nutrition",
                "Photosynthesis in Higher Plants",
                "Respiration in Plants",
                "Plant Growth and Development",
                "Human Physiology",
                "Digestion and Absorption",
                "Breathing and Exchange of Gases",
                "Body Fluids and Circulation",
                "Excretory Products and Their Elimination",
                "Locomotion and Movement",
                "Neural Control and Coordination",
                "Chemical Coordination and Integration",
                "Reproduction",
                "Reproduction in Organisms",
                "Sexual Reproduction in Flowering Plants",
                "Human Reproduction",
                "Reproductive Health",
                "Genetics and Evolution",
                "Principles of Inheritance and Variation",
                "Molecular Basis of Inheritance",
                "Evolution",
                "Biology and Human Welfare",
                "Human Health and Disease",
                "Strategies for Enhancement in Food Production",
                "Microbes in Human Welfare",
                "Biotechnology and Its Applications",
                "Biotechnology: Principles and Processes",
                "Ecology and Environment",
                "Organisms and Populations",
                "Ecosystem",
                "Biodiversity and Conservation",
                "Environmental Issues"
            ]
        }
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main landing page - Auto-redirect logged-in users to dashboard"""
    # Check if this is a logged-in user by checking for user data in session
    # Since we use localStorage on frontend, we'll let the frontend handle the redirect
    # But we can also check server-side session if available
    if session.get('user_id'):
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route("/stats")
def stats():
    # Authentication required for stats page
    return render_template("stats.html", auth_required=True)

@app.route("/dashboard")
def dashboard():
    """User dashboard - exam selection and progress overview"""
    # Authentication required for dashboard page
    return render_template("dashboard.html", auth_required=True)

@app.route('/start-journey')
def start_journey():
    """Start Your Journey button redirects here, then to dashboard"""
    return redirect(url_for('dashboard'))

@app.route('/select-exam', methods=['POST'])
def select_exam():
    """Handle exam selection from dashboard"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        # Handle both single exam and multiple exams
        exam = data.get('exam')
        selected_exams = data.get('selected_exams', [])
        
        # If selected_exams is provided, use it; otherwise use single exam
        if selected_exams:
            exams_to_process = selected_exams
        elif exam:
            exams_to_process = [exam]
        else:
            return jsonify({'success': False, 'error': 'Missing exam selection'})
        
        if not user_id:
            return jsonify({'success': False, 'error': 'Missing user_id'})
        
        # Save selected exams to database
        user_data = {
            'selected_exams': exams_to_process,
            'selected_exam': exams_to_process[0],  # Keep backward compatibility
            'exam_selected_at': datetime.now().isoformat()
        }
        
        db.save_user_data(user_id, user_data)
        
        # Initialize progress for all selected exams in database
        syllabi = get_exam_syllabi()
        existing_progress = db.get_user_progress(user_id)
        
        for exam_name in exams_to_process:
            if exam_name not in existing_progress:
                if exam_name in syllabi:
                    for subject, topics in syllabi[exam_name].items():
                        for topic in topics:
                            progress_data = {
                                'theory': False,
                                'practice': False,
                                'revision': False,
                                'completed_at': None
                            }
                            db.save_user_progress(user_id, exam_name, subject, topic, progress_data)
        
        exam_names = ', '.join(exams_to_process)
        return jsonify({
            'success': True, 
            'message': f'Exam(s) {exam_names} selected successfully!',
            'redirect_url': f'/tracker/{exams_to_process[0]}',
            'selected_exams': exams_to_process
        })
        
    except Exception as e:
        print(f"Error in select_exam: {str(e)}")  # Debug logging
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-user-exam', methods=['POST'])
def get_user_exam():
    """Get user's selected exam for dashboard redirect logic"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'Missing user_id'})
        
        # Get user data from database
        user_data = db.get_user_data(user_id)
        
        if user_data:
            # Check for multiple exams first, then fallback to single exam
            selected_exams = user_data.get('selected_exams', [])
            selected_exam = user_data.get('selected_exam')
            
            if selected_exams:
                return jsonify({
                    'success': True,
                    'has_selected_exam': True,
                    'selected_exam': selected_exams[0],  # Primary exam for redirect
                    'selected_exams': selected_exams,    # All selected exams
                    'redirect_url': f'/tracker/{selected_exams[0]}'
                })
            elif selected_exam:
                return jsonify({
                    'success': True,
                    'has_selected_exam': True,
                    'selected_exam': selected_exam,
                    'selected_exams': [selected_exam],
                    'redirect_url': f'/tracker/{selected_exam}'
                })
        
        return jsonify({
            'success': True,
            'has_selected_exam': False
        })
        
    except Exception as e:
        print(f"Error in get_user_exam: {str(e)}")  # Debug logging
        return jsonify({'success': False, 'message': str(e)})

@app.route('/login')
def login():
    """Firebase login page"""
    return render_template('login.html')

@app.route('/profile')
def profile():
    """User profile page - requires login"""
    # In a real implementation, you would check Firebase auth token here
    # For now, we'll use a simple check
    return render_template('profile.html')

@app.route('/save_confirmation')
def save_confirmation():
    """Progress save confirmation page"""
    return render_template('save_confirmation.html')

@app.route('/tracker/<exam>')
def tracker(exam):
    """Exam tracker interface - requires authentication"""
    syllabi = get_exam_syllabi()
    if exam not in syllabi:
        return redirect(url_for('index'))
    
    exam_data = syllabi[exam]
    # Pass a flag to indicate authentication is required
    return render_template('tracker.html', exam=exam, data=exam_data, auth_required=True)

@app.route('/api/syllabi')
def get_syllabi():
    """API endpoint to get all exam syllabi"""
    return jsonify(get_exam_syllabi())

@app.route('/api/progress/<exam>')
def get_progress(exam):
    """Get progress for a specific exam"""
    try:
        # Get user_id from request or session
        user_id = request.args.get('user_id') or session.get('user_id', 'default_user')
        
        # Get progress from database
        all_progress = db.get_user_progress(user_id, exam)
        exam_progress = all_progress.get(exam, {})
        
        return jsonify(exam_progress)
    except Exception as e:
        print(f"Error in get_progress: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress/<exam>', methods=['POST'])
def update_progress(exam):
    """Update progress for a specific exam"""
    user_id = session.get('user_id', 'default_user')
    data = request.get_json()
    
    progress_data = load_user_progress()
    if user_id not in progress_data:
        progress_data[user_id] = {}
    
    if exam not in progress_data[user_id]:
        progress_data[user_id][exam] = {}
    
    progress_data[user_id][exam].update(data)

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    """Save user progress for exam tracking with Firebase user data
    Handles both JSON (AJAX) and form POSTs (tracker.html form)."""
    import datetime
    try:
        # Check content type
        if request.is_json:
            data = request.get_json()
            exam = data.get('exam')
            user_id = data.get('userId')
            progress_data = data.get('progress', {})
        else:
            # Handle form POST (application/x-www-form-urlencoded)
            exam = request.form.get('exam')
            user_id = session.get('user_id') or request.form.get('user_id')
            # Build progress_data from form fields
            progress_data = {}
            # Expecting fields like 'Physics__Units and Dimensions__Theory' etc.
            for key, value in request.form.items():
                if key in ['exam', 'user_id']:
                    continue
                try:
                    subject, chapter, status_type = key.split('__')
                except ValueError:
                    continue
                if subject not in progress_data:
                    progress_data[subject] = {}
                if chapter not in progress_data[subject]:
                    progress_data[subject][chapter] = {}
                progress_data[subject][chapter][status_type] = value
        
        # Validate
        if not exam or not user_id:
            return jsonify({'error': 'Missing exam or userId'}), 400
        
        # Save progress to database
        for subject, chapters in progress_data.items():
            for chapter, statuses in chapters.items():
                # Convert status values to boolean
                progress_entry = {
                    'theory': statuses.get('Theory', 'false').lower() == 'true',
                    'practice': statuses.get('Practice', 'false').lower() == 'true', 
                    'revision': statuses.get('Revision', 'false').lower() == 'true',
                    'completed_at': datetime.datetime.now().isoformat() if any([
                        statuses.get('Theory', 'false').lower() == 'true',
                        statuses.get('Practice', 'false').lower() == 'true',
                        statuses.get('Revision', 'false').lower() == 'true'
                    ]) else None
                }
                
                db.save_user_progress(user_id, exam, subject, chapter, progress_entry)
        
        # Get updated progress for statistics
        all_progress = db.get_user_progress(user_id)
        completed_topics = calculate_completed_topics(all_progress)
        
        # Create user progress summary for response
        user_progress = {
            'statistics': {
                'totalExams': len(all_progress),
                'completedTopics': completed_topics,
                'studyStreak': 0,  # TODO: Implement streak calculation
                'totalStudyHours': 0,  # TODO: Implement study hours tracking
                'lastStudyDate': datetime.datetime.now().isoformat()
            }
        }
        # Return appropriate response
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Progress saved successfully',
                'statistics': user_progress['statistics']
            })
        else:
            # Form POST: redirect to confirmation page or back to tracker
            return redirect(url_for('save_confirmation'))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

        return jsonify({'error': str(e)}), 500

def calculate_completed_topics(progress_data):
    """Calculate total completed topics across all exams from database structure"""
    total_completed = 0
    for exam_name, exam_data in progress_data.items():
        for subject_name, subject_data in exam_data.items():
            for topic_name, topic_data in subject_data.items():
                # Count as completed if all three statuses are True
                if (topic_data.get('theory') and 
                    topic_data.get('practice') and 
                    topic_data.get('revision')):
                    total_completed += 1
    return total_completed

@app.route('/api/stats/<exam>')
def get_exam_stats(exam):
    """Get completion statistics for an exam"""
    user_id = session.get('user_id', 'default_user')
    progress_data = load_user_progress()
    user_progress = progress_data.get(user_id, {}).get(exam, {})
    
    syllabi = get_exam_syllabi()
    exam_data = syllabi.get(exam, {})
    
    total_topics = 0
    completed_topics = 0
    
    for subject, subject_data in exam_data.get('subjects', {}).items():
        for topic in subject_data.get('topics', []):
            total_topics += 1
            if (subject in user_progress and 
                topic in user_progress[subject] and 
                user_progress[subject][topic].get('completed', False)):
                completed_topics += 1
    
    completion_percentage = (completed_topics / total_topics * 100) if total_topics > 0 else 0
    
    return jsonify({
        'total_topics': total_topics,
        'completed_topics': completed_topics,
        'completion_percentage': round(completion_percentage, 1)
    })

if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
