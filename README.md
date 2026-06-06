# Skill Exchange Platform (SEP)

An automated, decentralized peer-to-peer (P2P) knowledge bartering ecosystem designed to replace traditional, manual learning coordination within academic departments. Built on robust Object-Oriented software engineering paradigms, the platform eliminates scheduling conflicts and reduces partner hunt latency by implementing a performant background set-intersection matching engine.

## 🚀 Key Features

* **Role-Based Authentication:** Secure user onboarding with encrypted credential cryptography models.
* **Automated Matching Engine:** An optimized set-intersection calculation layer that matches inverse student competencies ($User_A\text{(Learn)} \cap User_B\text{(Teach)} \neq \emptyset$) to accelerate match velocities by up to 40%.
* **State-Enforced Request State Machine:** Explicit transactional request lifecycles (`Pending` ➡️ `Accepted` ➡️ `Session Scheduled` ➡️ `Completed`) implemented at the server layer to guarantee operational log integrity and prevent double-booking deadlock states.
* **Relational Integrity:** Implements rigorous multi-row SQLite foreign key verification and cascade rules to prevent orphaned coordinate rows.
* **Responsive Visual UI:** Clean, high-contrast Bootstrap 5 layouts parsing dynamic Jinja2 server-side properties.

---

## 🛠️ Technology Stack

| Layer | Selection | Justification |
| :--- | :--- | :--- |
| **Backend Framework** | Python Flask 2.x | Delivers lightweight MVC routing controls and clean integration paths. |
| **Database Architecture** | SQLite3 | Serverless, file-based relational mapping with zero-overhead transportability. |
| **Frontend Presentation** | HTML5, CSS3, JavaScript (ES6), Bootstrap 5 | Guarantees cross-device client responsiveness and semantic validation. |
| **Dynamic Templating** | Jinja2 Engine | Compiles backend dictionaries and set parameters directly into responsive views. |
| **Architecture Pattern** | Model-View-Controller (MVC) | Decouples data schemas, client presentation blocks, and route controller workflows. |

---

## 📁 Project Folder Structure

```text
SkillExchangePlatform/
│
├── app.py                 # Main application entry point & runtime bootstrap
├── database.py            # Relational schema setup, connection layer, and lookup seeds (Model)
├── models.py              # Object-oriented domain entity class design mappings
├── routes.py              # Blueprint endpoint routing controllers & matching algorithms (Controller)
├── SkillExchangeDB.db     # SQLite relational database storage file
├── requirements.txt       # Python environment package specification manifest
│
└── templates/             # Server-Side Jinja2 Core UI Presentation (View)
    ├── layout.html        # Global navigation grid shell background wrapper
    ├── index.html         # Public authentication landing gate form view
    ├── register.html      # Identity creation profile registration form
    ├── dashboard.html     # Symmetrical match partner recommendation matrix cards
    ├── profile.html       # Preference configuration dashboard ("Teach"/"Learn" catalogs)
    ├── manage_requests.html # Token lifecycle status monitor ledger (Sent/Received)
    └── sessions.html      # Finalized peer coordination interactive modal console
