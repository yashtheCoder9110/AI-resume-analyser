# skills_data.py
# Master list of skills/keywords the system looks for in resumes and job
# descriptions. Grouped by category only for readability -- the matcher
# treats them all as one flat set. Extend this list any time to cover
# more domains (the rest of the app needs zero changes).

SKILLS_DB = {
    # Programming languages
    "python", "java", "c++", "c", "c#", "javascript", "typescript", "go",
    "golang", "rust", "kotlin", "swift", "php", "ruby", "r", "matlab",
    "scala", "perl", "dart", "sql", "bash", "shell scripting",

    # Web development
    "html", "css", "react", "reactjs", "angular", "vue", "vuejs", "next.js",
    "nextjs", "node.js", "nodejs", "express.js", "expressjs", "django",
    "flask", "fastapi", "spring boot", "spring", "bootstrap", "tailwind",
    "jquery", "rest api", "restful api", "graphql", "webpack", "redux",

    # Data / ML / AI
    "machine learning", "deep learning", "artificial intelligence", "nlp",
    "natural language processing", "computer vision", "opencv",
  "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas",
    "numpy", "matplotlib", "seaborn", "data analysis", "data visualization",
    "data science", "data mining", "statistics", "regression",
    "classification", "clustering", "neural networks", "cnn", "rnn", "lstm",
    "transformers", "llm", "generative ai", "feature engineering",
    "model deployment", "mlops", "time series", "anomaly detection",

    # Databases
    "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis",
    "cassandra", "firebase", "dbms", "database design", "nosql",

    # Cloud / DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "jenkins", "ci/cd", "terraform", "linux", "git", "github", "gitlab",
    "devops", "nginx", "microservices", "system design",

    # CS fundamentals
    "data structures", "algorithms", "oop", "object oriented programming",
    "operating systems", "computer networks", "system architecture",
    "software engineering", "design patterns", "agile", "scrum",
    "testing", "unit testing", "debugging",

    # Security
    "cybersecurity", "network security", "cryptography", "penetration testing",
    "ethical hacking", "phishing detection",

    # Other tech
    "blockchain", "solidity", "web3", "android development", "ios development",
    "flutter", "react native", "unity", "game development", "iot",
    "arduino", "raspberry pi", "embedded systems", "ar/vr",

    # Soft / general (kept minimal on purpose -- resumes are ranked mainly
    # on technical overlap for a CSE job-matching use case)
    "communication", "teamwork", "leadership", "problem solving",
    "project management", "time management",
}
