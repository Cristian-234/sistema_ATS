import re
from collections import OrderedDict


TECH_TAXONOMY = OrderedDict(
    {
        "Programming Languages": {
            "python": ["python"],
            "java": ["java"],
            "javascript": ["javascript", "js"],
            "typescript": ["typescript", "ts"],
            "c++": ["c++", "cpp"],
            "c#": ["c#", "c sharp"],
            "php": ["php"],
            "sql": ["sql"],
        },
        "Backend and APIs": {
            "rest api": ["api rest", "apis rest", "rest api", "restful api", "restful apis"],
            "django": ["django"],
            "flask": ["flask"],
            "fastapi": ["fastapi", "fast api"],
            "spring boot": ["spring boot", "springboot"],
            "node.js": ["node.js", "nodejs", "node js"],
            "microservices": ["microservicios", "microservices"],
        },
        "Data and AI": {
            "machine learning": ["machine learning", "aprendizaje automatico"],
            "nlp": ["nlp", "procesamiento de lenguaje natural", "natural language processing"],
            "pandas": ["pandas"],
            "numpy": ["numpy"],
            "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
            "tensorflow": ["tensorflow"],
            "pytorch": ["pytorch", "torch"],
            "power bi": ["power bi", "powerbi"],
        },
        "Databases": {
            "postgresql": ["postgresql", "postgres"],
            "mysql": ["mysql"],
            "sql server": ["sql server", "mssql"],
            "mongodb": ["mongodb", "mongo db"],
            "redis": ["redis"],
            "chromadb": ["chromadb", "chroma db"],
        },
        "Cloud and DevOps": {
            "aws": ["aws", "amazon web services"],
            "azure": ["azure", "microsoft azure"],
            "gcp": ["gcp", "google cloud"],
            "docker": ["docker"],
            "kubernetes": ["kubernetes", "k8s"],
            "git": ["git", "github", "gitlab"],
            "ci/cd": ["ci/cd", "cicd", "continuous integration", "continuous delivery"],
        },
        "Frontend": {
            "react": ["react", "react.js", "reactjs"],
            "angular": ["angular"],
            "vue": ["vue", "vue.js", "vuejs"],
            "html": ["html", "html5"],
            "css": ["css", "css3"],
            "streamlit": ["streamlit"],
        },
        "Methodologies": {
            "scrum": ["scrum"],
            "agile": ["agile", "agil", "metodologias agiles"],
            "kanban": ["kanban"],
        },
        "Languages": {
            "english": ["ingles", "english"],
            "spanish": ["espanol", "spanish"],
        },
    }
)


ACCOUNTING_TAXONOMY = OrderedDict(
    {
        "Accounting Core": {
            "general ledger": ["general ledger", "libro mayor", "mayor contable"],
            "journal entries": ["journal entries", "asientos contables", "asiento contable"],
            "account reconciliation": ["account reconciliation", "reconciliacion de cuentas", "conciliacion de cuentas"],
            "bank reconciliation": ["bank reconciliation", "conciliacion bancaria", "reconciliaciones bancarias"],
            "accounts payable": ["accounts payable", "cuentas por pagar", "proveedores"],
            "accounts receivable": ["accounts receivable", "cuentas por cobrar", "cobranzas"],
            "fixed assets": ["fixed assets", "activos fijos", "depreciacion"],
            "closing process": ["closing process", "cierre contable", "monthly close", "cierre mensual"],
        },
        "Financial Reporting": {
            "financial statements": ["financial statements", "estados financieros"],
            "balance sheet": ["balance sheet", "estado de situacion financiera", "balance general"],
            "income statement": ["income statement", "estado de resultados", "profit and loss", "p&l"],
            "cash flow": ["cash flow", "flujo de caja", "flujo de efectivo"],
            "management reports": ["management reports", "reportes de gestion", "informes de gestion"],
            "budgeting": ["budgeting", "presupuesto", "presupuestos"],
            "forecasting": ["forecasting", "proyecciones", "forecast"],
        },
        "Tax and Compliance": {
            "tax returns": ["tax returns", "declaraciones juradas", "declaracion de impuestos"],
            "vat": ["vat", "igv", "iva"],
            "income tax": ["income tax", "impuesto a la renta", "renta anual"],
            "payroll taxes": ["payroll taxes", "impuestos de planilla", "tributos laborales"],
            "withholding tax": ["withholding tax", "retenciones", "percepciones"],
            "tax compliance": ["tax compliance", "cumplimiento tributario", "obligaciones tributarias"],
            "audit support": ["audit support", "soporte de auditoria", "atencion de auditoria"],
        },
        "Audit and Controls": {
            "internal audit": ["internal audit", "auditoria interna"],
            "external audit": ["external audit", "auditoria externa"],
            "internal controls": ["internal controls", "controles internos", "control interno"],
            "risk assessment": ["risk assessment", "evaluacion de riesgos"],
            "sox": ["sox", "sarbanes oxley"],
            "compliance": ["compliance", "cumplimiento normativo"],
        },
        "ERP and Tools": {
            "sap": ["sap", "sap fi", "sap fico"],
            "oracle": ["oracle", "oracle erp", "oracle financials"],
            "quickbooks": ["quickbooks"],
            "excel": ["excel", "microsoft excel", "tablas dinamicas", "pivot tables"],
            "power bi": ["power bi", "powerbi"],
            "sunat": ["sunat"],
            "concar": ["concar"],
            "siscont": ["siscont"],
            "netsuite": ["netsuite", "net suite"],
        },
        "Standards": {
            "ifrs": ["ifrs", "niif", "normas internacionales de informacion financiera"],
            "gaap": ["gaap", "us gaap", "principios de contabilidad generalmente aceptados"],
            "ias": ["ias", "nic", "normas internacionales de contabilidad"],
        },
        "Languages": {
            "english": ["ingles", "english"],
            "spanish": ["espanol", "spanish"],
        },
    }
)


HEALTHCARE_TAXONOMY = OrderedDict(
    {
        "Clinical Care": {
            "patient care": ["patient care", "atencion al paciente", "cuidado del paciente"],
            "vital signs": ["vital signs", "signos vitales"],
            "triage": ["triage", "triaje"],
            "medical records": ["medical records", "historias clinicas", "historia clinica"],
            "clinical assessment": ["clinical assessment", "evaluacion clinica"],
            "medication administration": ["medication administration", "administracion de medicamentos"],
            "wound care": ["wound care", "curacion de heridas"],
            "infection control": ["infection control", "control de infecciones"],
        },
        "Specialties": {
            "emergency care": ["emergency care", "emergencias", "urgencias"],
            "primary care": ["primary care", "atencion primaria"],
            "pediatrics": ["pediatrics", "pediatria"],
            "geriatrics": ["geriatrics", "geriatria"],
            "intensive care": ["intensive care", "uci", "icu", "cuidados intensivos"],
            "surgery": ["surgery", "cirugia", "surgical"],
        },
        "Healthcare Administration": {
            "appointment scheduling": ["appointment scheduling", "programacion de citas", "citas medicas"],
            "insurance verification": ["insurance verification", "verificacion de seguros"],
            "billing": ["billing", "facturacion medica", "medical billing"],
            "patient admission": ["patient admission", "admision de pacientes"],
            "healthcare compliance": ["healthcare compliance", "cumplimiento sanitario"],
        },
        "Tools and Standards": {
            "ehr": ["ehr", "emr", "electronic health record", "historia clinica electronica"],
            "hipaa": ["hipaa"],
            "hl7": ["hl7"],
            "excel": ["excel", "microsoft excel"],
            "power bi": ["power bi", "powerbi"],
        },
        "Languages": {
            "english": ["ingles", "english"],
            "spanish": ["espanol", "spanish"],
        },
    }
)


EDUCATION_TAXONOMY = OrderedDict(
    {
        "Teaching and Learning": {
            "lesson planning": ["lesson planning", "planificacion de clases", "sesiones de aprendizaje"],
            "curriculum design": ["curriculum design", "diseno curricular", "curriculo"],
            "classroom management": ["classroom management", "gestion de aula", "manejo de aula"],
            "student assessment": ["student assessment", "evaluacion de estudiantes", "evaluacion formativa"],
            "differentiated instruction": ["differentiated instruction", "ensenanza diferenciada"],
            "tutoring": ["tutoring", "tutoria", "asesoria academica"],
            "special education": ["special education", "educacion especial"],
        },
        "Educational Technology": {
            "lms": ["lms", "learning management system", "plataforma educativa"],
            "moodle": ["moodle"],
            "google classroom": ["google classroom"],
            "canvas": ["canvas lms"],
            "virtual learning": ["virtual learning", "educacion virtual", "clases virtuales"],
            "digital resources": ["digital resources", "recursos digitales"],
        },
        "Academic Administration": {
            "academic coordination": ["academic coordination", "coordinacion academica"],
            "student records": ["student records", "registros academicos"],
            "parent communication": ["parent communication", "comunicacion con padres"],
            "school projects": ["school projects", "proyectos educativos"],
        },
        "Languages": {
            "english": ["ingles", "english"],
            "spanish": ["espanol", "spanish"],
        },
    }
)


MARKETING_SALES_TAXONOMY = OrderedDict(
    {
        "Marketing": {
            "digital marketing": ["digital marketing", "marketing digital"],
            "seo": ["seo", "search engine optimization"],
            "sem": ["sem", "google ads", "paid search"],
            "content marketing": ["content marketing", "marketing de contenidos"],
            "social media": ["social media", "redes sociales"],
            "email marketing": ["email marketing"],
            "brand management": ["brand management", "gestion de marca"],
            "market research": ["market research", "investigacion de mercado"],
        },
        "Sales": {
            "lead generation": ["lead generation", "generacion de leads", "prospecting"],
            "crm": ["crm", "salesforce", "hubspot"],
            "sales pipeline": ["sales pipeline", "pipeline de ventas"],
            "negotiation": ["negotiation", "negociacion"],
            "account management": ["account management", "gestion de cuentas"],
            "customer service": ["customer service", "servicio al cliente"],
            "b2b sales": ["b2b sales", "ventas b2b"],
        },
        "Analytics and Tools": {
            "google analytics": ["google analytics", "ga4"],
            "meta ads": ["meta ads", "facebook ads", "instagram ads"],
            "excel": ["excel", "microsoft excel"],
            "power bi": ["power bi", "powerbi"],
            "tableau": ["tableau"],
        },
        "Languages": {
            "english": ["ingles", "english"],
            "spanish": ["espanol", "spanish"],
        },
    }
)


HR_TAXONOMY = OrderedDict(
    {
        "Talent Acquisition": {
            "recruitment": ["recruitment", "reclutamiento"],
            "selection": ["selection", "seleccion de personal"],
            "interviewing": ["interviewing", "entrevistas"],
            "onboarding": ["onboarding", "induccion"],
            "job descriptions": ["job descriptions", "descripciones de puesto"],
            "ats": ["ats", "applicant tracking system"],
        },
        "HR Operations": {
            "payroll": ["payroll", "planilla", "nomina"],
            "employee records": ["employee records", "legajos", "expedientes laborales"],
            "labor law": ["labor law", "legislacion laboral", "derecho laboral"],
            "benefits administration": ["benefits administration", "beneficios laborales"],
            "hr policies": ["hr policies", "politicas de recursos humanos"],
        },
        "People Development": {
            "training": ["training", "capacitacion"],
            "performance management": ["performance management", "evaluacion de desempeno"],
            "organizational climate": ["organizational climate", "clima laboral"],
            "employee engagement": ["employee engagement", "compromiso laboral"],
        },
        "Tools": {
            "excel": ["excel", "microsoft excel"],
            "sap successfactors": ["sap successfactors", "successfactors"],
            "workday": ["workday"],
            "power bi": ["power bi", "powerbi"],
        },
        "Languages": {
            "english": ["ingles", "english"],
            "spanish": ["espanol", "spanish"],
        },
    }
)


OPERATIONS_LOGISTICS_TAXONOMY = OrderedDict(
    {
        "Operations": {
            "process improvement": ["process improvement", "mejora de procesos"],
            "kpi management": ["kpi management", "indicadores", "kpis"],
            "quality control": ["quality control", "control de calidad"],
            "lean": ["lean", "lean manufacturing"],
            "six sigma": ["six sigma", "six-sigma"],
            "production planning": ["production planning", "planificacion de produccion"],
        },
        "Logistics": {
            "inventory management": ["inventory management", "gestion de inventarios", "inventarios"],
            "warehouse management": ["warehouse management", "gestion de almacenes", "almacen"],
            "supply chain": ["supply chain", "cadena de suministro"],
            "procurement": ["procurement", "compras", "abastecimiento"],
            "transportation": ["transportation", "transporte", "distribucion"],
            "demand planning": ["demand planning", "planificacion de demanda"],
        },
        "Tools": {
            "sap": ["sap", "sap mm", "sap sd"],
            "erp": ["erp"],
            "excel": ["excel", "microsoft excel"],
            "power bi": ["power bi", "powerbi"],
            "wms": ["wms", "warehouse management system"],
        },
        "Languages": {
            "english": ["ingles", "english"],
            "spanish": ["espanol", "spanish"],
        },
    }
)


SKILL_TAXONOMIES = OrderedDict(
    {
        "Technology / Software": TECH_TAXONOMY,
        "Accounting / Finance": ACCOUNTING_TAXONOMY,
        "Healthcare": HEALTHCARE_TAXONOMY,
        "Education": EDUCATION_TAXONOMY,
        "Marketing / Sales": MARKETING_SALES_TAXONOMY,
        "Human Resources": HR_TAXONOMY,
        "Operations / Logistics": OPERATIONS_LOGISTICS_TAXONOMY,
    }
)


SECTION_PATTERNS = OrderedDict(
    {
        "experience": [
            "experiencia",
            "experience",
            "work experience",
            "employment",
            "work history",
            "historial laboral",
            "professional experience",
        ],
        "skills": [
            "habilidades",
            "skills",
            "accounting skills",
            "technical skills",
            "competencias",
            "competencias tecnicas",
            "core competencies",
        ],
        "education": [
            "educacion",
            "education",
            "formacion",
            "academic background",
            "academic",
        ],
        "certifications": [
            "certificaciones",
            "certifications",
            "certificates",
            "cursos",
            "courses",
            "training",
        ],
        "languages": [
            "idiomas",
            "languages",
        ],
    }
)


SECTION_WEIGHTS = {
    "experience": 0.35,
    "skills": 0.35,
    "education": 0.15,
    "certifications": 0.10,
    "languages": 0.05,
}


def _normalize_text(text):
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ñ": "n",
    }
    text = text.lower()
    for source, target in replacements.items():
        text = text.replace(source, target)
    return re.sub(r"\s+", " ", text).strip()


def _alias_found(text, alias):
    escaped = re.escape(_normalize_text(alias))
    pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
    return re.search(pattern, text) is not None


def get_available_domains():
    return list(SKILL_TAXONOMIES.keys())


def extract_skills(text, domain="Technology / Software"):
    """
    Detects skills using the selected domain taxonomy.
    Returns matches by category and a flat canonical list.
    """
    taxonomy = SKILL_TAXONOMIES.get(domain, TECH_TAXONOMY)
    normalized = _normalize_text(text)
    by_category = OrderedDict()
    flat = []

    for category, skills in taxonomy.items():
        matches = []
        for canonical, aliases in skills.items():
            if any(_alias_found(normalized, alias) for alias in aliases):
                matches.append(canonical)
                flat.append(canonical)
        by_category[category] = matches

    return {"by_category": by_category, "flat": sorted(set(flat))}


def extract_resume_sections(text):
    """
    Splits a resume into approximate sections using common headings.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections = {name: "" for name in SECTION_PATTERNS}
    current = None

    for line in lines:
        normalized_line = _normalize_text(line).strip(":.- ")
        detected = None
        for section, aliases in SECTION_PATTERNS.items():
            if any(normalized_line == _normalize_text(alias) for alias in aliases):
                detected = section
                break

        if detected:
            current = detected
            continue

        if current:
            sections[current] = f"{sections[current]} {line}".strip()

    return sections


def calculate_skill_match(job_skills, resume_skills):
    required = set(job_skills)
    candidate = set(resume_skills)

    if not required:
        return {
            "score": None,
            "matched": [],
            "missing": [],
            "extra": sorted(candidate),
        }

    matched = sorted(required.intersection(candidate))
    missing = sorted(required.difference(candidate))
    score = round((len(matched) / len(required)) * 100, 2)

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "extra": sorted(candidate.difference(required)),
    }
