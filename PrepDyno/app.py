from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

Syllabus = {
    "JEE": {
        "Physics": [
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
        "Chemistry": [
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
        "Mathematics": [
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
    "IAT": {
        "Physics": [
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
        "Chemistry": [
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
        "Mathematics": [
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
        "Biology": [
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
    "UGEE": {
        "Mathematics": [
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
        "Physics": [
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
        "Research Aptitude": [
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
    "NEET": {
        "Physics": [
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
        "Chemistry": [
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
        "Biology": [
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
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        exam = request.form["exam"]
        return render_template("tracker.html", exam=exam, data=Syllabus[exam])
    return render_template("index.html", syllabus=Syllabus)
    


@app.route("/save", methods=["POST"])
def save():
    exam = request.form["exam"]
    progress = {}

    for key in request.form:
        if key == "exam":
            continue

        # key format will be like Physics__Kinematics__Theory
        try:
            subject, chapter, category = key.split("__")
        except ValueError:
            continue  # in case of malformed keys

        status = request.form[key]

        if subject not in progress:
            progress[subject] = {}
        if chapter not in progress[subject]:
            progress[subject][chapter] = {}
        
        progress[subject][chapter][category] = status

    # Save to JSON
    filename = f"{exam}_progress.json"
    try:
        with open(filename, "w") as f:
            json.dump(progress, f, indent=2)
    except Exception as e:
        print(f"Error saving file: {e}")

    return render_template("save.html", exam=exam, progress=progress)


@app.route("/load_progress/<exam>")
def load_progress(exam):
    filename = f"{exam}_progress.json"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                progress = json.load(f)
            return jsonify(progress)
        except Exception as e:
            print(f"Error loading file: {e}")
            return jsonify({})
    return jsonify({})




if __name__ == "__main__":
    app.run(debug=True)