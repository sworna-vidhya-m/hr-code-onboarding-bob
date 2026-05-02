**User:**

<task>
@AGENTS.md

Add these rules to AGENTS.md:
1. Never break existing working code
2. After any Python change run:
   python3 -c "from app import main"
3. Use relative URLs in fetch calls
4. Never use curl for testing
5. Keep all 4 tabs working
6. Save files after every change
</task>
<environment_details>
# VSCode Visible Files
bob_sessions/task10_Create_AgentsMD_File_ForCustomInstructions.md

# VSCode Open Tabs
bob_sessions/task10_Create_AgentsMD_File_ForCustomInstructions.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:47:25.955Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (/Users/swornamacair/Documents/IBM_Hackathon/hr-code-onboarding-bob) Files
.gitignore
README.md
requirements.txt
app/
app/__init__.py
app/employee.py
app/leave.py
app/main.py
app/payroll.py
app/performance.py
bob_sessions/
bob_sessions/task1_explain_codebase.md
bob_sessions/task1_explain_codebase.png
bob_sessions/task2_onboarding_doc.md
bob_sessions/task2_onboarding_doc.png
bob_sessions/task3_performance_feature.md
bob_sessions/task3_performance_feature.png
bob_sessions/task4_test_performance_fix.md
bob_sessions/task4_test_performance_fix.png
bob_sessions/task5_fix_employee_show_in_UI_issue.md
bob_sessions/task5_fix_employee_show_in_UI_issue.png
bob_sessions/task6_replace_occurances_localhost_to_slash.md
bob_sessions/task6_replace_occurances_localhost_to_slash.png
bob_sessions/task7_fix_localhost_issue.md
bob_sessions/task7_fix_localhost_issue.png
bob_sessions/task8_fix_JavaScript_SyntaxError_issue.md
bob_sessions/task8_fix_JavaScript_SyntaxError_issue.png
bob_sessions/task9_Fixed_VerifyCode_APP_running.md
bob_sessions/task9_Fixed_VerifyCode_APP_running.png
bob_sessions/task10_Create_AgentsMD_File_ForCustomInstructions.md
bob_sessions/task10_Create_AgentsMD_File_ForCustomInstructions.png
bob_sessions/UI_Screenshots/
bob_sessions/UI_Screenshots/Emplyee_Tab.png
bob_sessions/UI_Screenshots/Leave_Tab.png
bob_sessions/UI_Screenshots/NEW_BOB_Introduced_FEATURE_Performance_TAB.png
bob_sessions/UI_Screenshots/Payroll_Tab_Payslip_Generated.png
bob_sessions/UI_Screenshots/Payroll_Tab_Salary_Details.png
bob_sessions/UI_Screenshots/Payroll_Tab.png
bob_sessions/UI_Screenshots/Performance_TAb_Employee_Details.png
bob_sessions/UI_Screenshots/Performance_Tab_errorhandling.png
bob_sessions/UI_Screenshots/Performance_Tab_Review_submit.png
docs/
docs/ONBOARDING.md
static/
static/index.html
tests/
tests/__init__.py
tests/test_employee.py
tests/test_leave.py
tests/test_payroll.py
tests/test_performance.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll read the current AGENTS.md file to see its contents, then add the requested rules.

<read_file>
<args>
<file>
<path>AGENTS.md</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'AGENTS.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>AGENTS.md</path><error>File not found</error><notice>The file was not found. Consider using list_files to find available files before attempting to read them.</notice></file>
</files>
<environment_details>
# VSCode Visible Files
bob_sessions/task10_Create_AgentsMD_File_ForCustomInstructions.md

# VSCode Open Tabs
bob_sessions/task10_Create_AgentsMD_File_ForCustomInstructions.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:47:28.259Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

The AGENTS.md file doesn't exist yet, so I'll create it with the requested rules.

<write_to_file>
<path>AGENTS.md</path>
<content># Agent Guidelines

## Critical Rules for Code Modifications

1. **Never break existing working code**
   - Always verify functionality before and after changes
   - Test all affected features thoroughly

2. **After any Python change run:**
   ```bash
   python3 -c "from app import main"
   ```
   - This validates that the Python code can be imported without errors
   - Run this check before considering any Python modification complete

3. **Use relative URLs in fetch calls**
   - Always use relative paths (e.g., `/api/endpoint`) instead of absolute URLs
   - Never hardcode `localhost` or specific domains in fetch calls

4. **Never use curl for testing**
   - Use the web interface or Python imports for testing
   - Avoid command-line HTTP testing tools

5. **Keep all 4 tabs working**
   - Employee Tab
   - Leave Tab
   - Payroll Tab
   - Performance Tab
   - Verify all tabs remain functional after any change

6. **Save files after every change**
   - Always save modified files immediately
   - Ensure changes are persisted before moving to the next step
</content>
<line_count>33</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'AGENTS.md'] Result:
<file_write_result>
<path>AGENTS.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
AGENTS.md

# VSCode Open Tabs
AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:48:09.953Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.02

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Created AGENTS.md file with the following critical rules for code modifications:

1. **Never break existing working code** - Always verify functionality before and after changes
2. **After any Python change run:** `python3 -c "from app import main"` - Validates Python code can be imported without errors
3. **Use relative URLs in fetch calls** - Always use relative paths (e.g., `/api/endpoint`) instead of absolute URLs
4. **Never use curl for testing** - Use the web interface or Python imports for testing
5. **Keep all 4 tabs working** - Employee, Leave, Payroll, and Performance tabs must remain functional
6. **Save files after every change** - Always save modified files immediately

The file has been created at the root of the workspace and is ready to be used as a reference for agent guidelines.
</result>
</attempt_completion>

