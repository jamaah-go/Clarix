"""
Seed Service
============
Database seeding for initial data.
"""
from typing import Dict, List, Any


# Clause category definitions
CLAUSE_CATEGORIES: Dict[str, Dict[str, Any]] = {
    # Obligations
    "OBLIG_001": {"name": "Confidentiality", "group": "obligations", "description": "Restrictions on disclosure of confidential information"},
    "OBLIG_002": {"name": "Non-Compete", "group": "obligations", "description": "Restrictions on competitive activities"},
    "OBLIG_003": {"name": "Non-Solicitation", "group": "obligations", "description": "Restrictions on soliciting employees or customers"},
    "OBLIG_004": {"name": "Non-Assignment", "group": "obligations", "description": "Restrictions on assignment of rights or obligations"},
    "OBLIG_005": {"name": "Performance Obligations", "group": "obligations", "description": "Duties and responsibilities of parties"},
    "OBLIG_006": {"name": "Reporting Requirements", "group": "obligations", "description": "Obligations to provide reports or updates"},
    "OBLIG_007": {"name": "Insurance Requirements", "group": "obligations", "description": "Required insurance coverage"},
    "OBLIG_008": {"name": "Compliance", "group": "obligations", "description": "Compliance with laws and regulations"},

    # Dates & Deadlines
    "DATE_001": {"name": "Effective Date", "group": "dates", "description": "Date when contract becomes binding"},
    "DATE_002": {"name": "Expiration Date", "group": "dates", "description": "Date when contract ends"},
    "DATE_003": {"name": "Renewal Date", "group": "dates", "description": "Date when renewal decision must be made"},
    "DATE_004": {"name": "Notice Period", "group": "dates", "description": "Required notice before termination"},
    "DATE_005": {"name": "Cure Period", "group": "dates", "description": "Period to cure breach"},
    "DATE_006": {"name": "Survival Period", "group": "dates", "description": "Duration of post-termination obligations"},

    # Financial
    "FIN_001": {"name": "Payment Terms", "group": "financial", "description": "Terms and conditions of payment"},
    "FIN_002": {"name": "Pricing", "group": "financial", "description": "Pricing structure and rates"},
    "FIN_003": {"name": "Fees", "group": "financial", "description": "Fees and charges"},
    "FIN_004": {"name": "Expenses", "group": "financial", "description": "Expense reimbursement terms"},
    "FIN_005": {"name": "Taxes", "group": "financial", "description": "Tax obligations and withholding"},
    "FIN_006": {"name": "Revenue Sharing", "group": "financial", "description": "Revenue or profit sharing arrangements"},
    "FIN_007": {"name": "Invoicing", "group": "financial", "description": "Invoicing procedures"},
    "FIN_008": {"name": "Late Payment", "group": "financial", "description": "Late payment penalties"},

    # Termination
    "TERM_001": {"name": "Termination for Cause", "group": "termination", "description": "Termination based on breach"},
    "TERM_002": {"name": "Termination for Convenience", "group": "termination", "description": "Termination without cause"},
    "TERM_003": {"name": "Termination Notice", "group": "termination", "description": "Notice requirements for termination"},
    "TERM_004": {"name": "Termination Effects", "group": "termination", "description": "Consequences of termination"},
    "TERM_005": {"name": "Transition Services", "group": "termination", "description": "Services during transition"},

    # Intellectual Property
    "IP_001": {"name": "IP Ownership", "group": "ip", "description": "Ownership of intellectual property"},
    "IP_002": {"name": "Licensing", "group": "ip", "description": "License grants and restrictions"},
    "IP_003": {"name": "Work-for-Hire", "group": "ip", "description": "Work-for-hire provisions"},
    "IP_004": {"name": "Derivative Works", "group": "ip", "description": "Derivative work ownership"},
    "IP_005": {"name": "Background IP", "group": "ip", "description": "Pre-existing intellectual property"},
    "IP_006": {"name": "Foreground IP", "group": "ip", "description": "Newly created intellectual property"},
    "IP_007": {"name": "IP Assignment", "group": "ip", "description": "IP assignment provisions"},

    # Liability
    "LIAB_001": {"name": "Limitation of Liability", "group": "liability", "description": "Caps on liability"},
    "LIAB_002": {"name": "Indemnification", "group": "liability", "description": "Obligation to indemnify"},
    "LIAB_003": {"name": "Damages", "group": "liability", "description": "Damage types and recovery"},
    "LIAB_004": {"name": "Warranty Disclaimer", "group": "liability", "description": "Disclaimer of warranties"},
    "LIAB_005": {"name": "Consequential Damages", "group": "liability", "description": "Consequential damages exclusions"},
    "LIAB_006": {"name": "Mutual Indemnification", "group": "liability", "description": "Mutual indemnification obligations"},
    "LIAB_007": {"name": "Insurance", "group": "liability", "description": "Insurance requirements"},

    # Regulatory
    "REG_001": {"name": "Data Protection", "group": "regulatory", "description": "Data protection requirements"},
    "REG_002": {"name": "Privacy", "group": "regulatory", "description": "Privacy obligations"},
    "REG_003": {"name": "Security", "group": "regulatory", "description": "Security requirements"},
    "REG_004": {"name": "Audit Rights", "group": "regulatory", "description": "Audit and compliance verification"},
    "REG_005": {"name": "Regulatory Compliance", "group": "regulatory", "description": "Compliance with regulations"},
    "REG_006": {"name": "GDPR", "group": "regulatory", "description": "GDPR compliance provisions"},
    "REG_007": {"name": "CCPA", "group": "regulatory", "description": "CCPA compliance provisions"},

    # General
    "GEN_001": {"name": "Governing Law", "group": "general", "description": "Governing law and jurisdiction"},
    "GEN_002": {"name": "Dispute Resolution", "group": "general", "description": "Dispute resolution mechanisms"},
    "GEN_003": {"name": "Arbitration", "group": "general", "description": "Arbitration provisions"},
    "GEN_004": {"name": "Venue", "group": "general", "description": "Venue for disputes"},
    "GEN_005": {"name": "Entire Agreement", "group": "general", "description": "Entire agreement clause"},
    "GEN_006": {"name": "Amendment", "group": "general", "description": "Amendment procedures"},
    "GEN_007": {"name": "Waiver", "group": "general", "description": "Waiver provisions"},
    "GEN_008": {"name": "Severability", "group": "general", "description": "Severability clause"},
    "GEN_009": {"name": "Counterparts", "group": "general", "description": "Counterparts provision"},
    "GEN_010": {"name": "Assignment", "group": "general", "description": "Assignment provisions"},
    "GEN_011": {"name": "Force Majeure", "group": "general", "description": "Force majeure clause"},
    "GEN_012": {"name": "Notices", "group": "general", "description": "Notice requirements"},
    "GEN_013": {"name": "Relationship of Parties", "group": "general", "description": "Relationship characterization"},
    "GEN_014": {"name": "Third Party Beneficiaries", "group": "general", "description": "Third party beneficiary rights"},
    "GEN_015": {"name": "Headings", "group": "general", "description": "Section headings"},

    # Auto-Renewal
    "RENEW_001": {"name": "Auto-Renewal", "group": "renewal", "description": "Automatic renewal provisions"},
    "RENEW_002": {"name": "Renewal Notice", "group": "renewal", "description": "Notice required for renewal"},
    "RENEW_003": {"name": "Renewal Terms", "group": "renewal", "description": "Terms upon renewal"},

    # Representations
    "REP_001": {"name": "Representations", "group": "representations", "description": "Representations and warranties"},
    "REP_002": {"name": "Warranties", "group": "representations", "description": "Warranty provisions"},

    # Misc
    "MISC_001": {"name": "Definition", "group": "misc", "description": "Definition of terms"},
    "MISC_002": {"name": "Exhibits", "group": "misc", "description": "Exhibit references"},
    "MISC_003": {"name": "Schedules", "group": "misc", "description": "Schedule references"},
    "MISC_004": {"name": "Order of Precedence", "group": "misc", "description": "Document precedence"},
}


async def seed_clause_categories(session_maker) -> None:
    """Seed clause categories into database."""
    from sqlalchemy import text

    async with session_maker() as session:
        # Check if categories already exist
        result = await session.execute(text("SELECT COUNT(*) FROM clause_categories"))
        count = result.scalar()

        if count > 0:
            return  # Already seeded

        # Insert categories
        for code, category in CLAUSE_CATEGORIES.items():
            await session.execute(
                text("""
                    INSERT INTO clause_categories (code, name, group_name, description, created_at)
                    VALUES (:code, :name, :group, :description, NOW())
                """),
                {
                    "code": code,
                    "name": category["name"],
                    "group": category["group"],
                    "description": category["description"],
                },
            )

        await session.commit()


def get_clause_categories() -> Dict[str, Dict[str, str]]:
    """Get all clause categories."""
    return CLAUSE_CATEGORIES


def get_clause_category(code: str) -> Dict[str, str] | None:
    """Get a specific clause category."""
    return CLAUSE_CATEGORIES.get(code)


def get_clause_categories_by_group() -> Dict[str, List[Dict[str, str]]]:
    """Get clause categories grouped by category group."""
    groups: Dict[str, List[Dict[str, str]]] = {}

    for code, category in CLAUSE_CATEGORIES.items():
        group = category["group"]
        if group not in groups:
            groups[group] = []
        groups[group].append({
            "code": code,
            "name": category["name"],
            "description": category["description"],
        })

    return groups
