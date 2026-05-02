---
name: hr-onboarding
description: >
  HR Employee Management System skill.
  Helps Bob understand and extend this 
  HR codebase efficiently.

instructions: |
  This is a FastAPI Python HR system.
  
  Project modules:
  - app/employee.py: Employee CRUD operations
  - app/leave.py: Leave management and eligibility
  - app/payroll.py: Payroll and tax calculation
  - app/performance.py: Performance reviews
  - app/main.py: All FastAPI API endpoints
  - static/index.html: Frontend with 4 tabs
  - tests/: All pytest test files
  - docs/ONBOARDING.md: Developer guide
  - AGENTS.md: Custom rules for Bob
  
  When adding new features:
  - Follow existing patterns in employee.py
  - Add new endpoints in main.py only
  - Create test file in tests/ folder
  - Update docs/ONBOARDING.md
  - Verify with: python3 -c "from app import main"
  - Never use curl for testing
  - Use relative URLs in index.html
  
  Sample data has 5 employees:
  Raj Kumar, Priya Sharma, Arun Patel,
  Meena Iyer, Suresh Babu

examples:
  - task: Explain codebase
    mode: Ask
    prompt: >
      @app/main.py @app/employee.py
      Explain the architecture and
      key business rules

  - task: Add new HR feature
    mode: Code
    prompt: >
      Follow employee.py pattern.
      Create new module in app/ folder.
      Add endpoints in main.py.
      Add tests in tests/ folder.

  - task: Generate documentation
    mode: Plan
    prompt: >
      Read all app files and update
      docs/ONBOARDING.md with latest
      architecture and function reference.
---