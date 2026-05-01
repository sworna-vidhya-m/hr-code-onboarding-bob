**User:**

<task>
@static/index.html

Fix all API fetch URLs in index.html.
Replace all occurrences of:
http://localhost:8000
with just:
/
(use relative URLs for all API calls)

For example:
fetch('http://localhost:8000/employees')
becomes:
fetch('/employees')

Do this for ALL fetch calls in the file.
Every single API call must use relative URL.
</task>
<environment_details>
# VSCode Visible Files
bob_sessions/task4_test_performance_fix.md

# VSCode Open Tabs
app/main.py,bob_sessions/task4_test_performance_fix.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-01T18:56:48.886Z
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

I'll help you fix all API fetch URLs in the index.html file to use relative URLs instead of absolute localhost URLs. Let me start by reading the file to see all the fetch calls.

<read_file>
<args>
<file>
<path>static/index.html</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'static/index.html'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>static/index.html</path>
<content lines="1-504">
  1 | <!DOCTYPE html>
  2 | <html lang="en">
  3 | <head>
  4 | <meta charset="UTF-8">
  5 | <meta name="viewport" content="width=device-width, initial-scale=1.0">
  6 | <title>HR Employee Management System</title>
  7 | <style>
  8 |   * { box-sizing: border-box; margin: 0; padding: 0; }
  9 |   body { font-family: 'Segoe UI', Arial, sans-serif; background: #f0f4f8; color: #1a2b42; }
 10 |   header { background: #1565c0; color: #fff; padding: 18px 32px; display: flex; align-items: center; gap: 14px; box-shadow: 0 2px 8px rgba(0,0,0,.18); }
 11 |   header h1 { font-size: 1.5rem; font-weight: 700; letter-spacing: .5px; }
 12 |   header span { font-size: .9rem; opacity: .75; }
 13 |   .tabs { display: flex; background: #fff; border-bottom: 2px solid #e3eaf5; padding: 0 32px; }
 14 |   .tab { padding: 14px 28px; cursor: pointer; font-size: .97rem; font-weight: 600; color: #546e8a; border-bottom: 3px solid transparent; transition: all .2s; }
 15 |   .tab:hover { color: #1565c0; }
 16 |   .tab.active { color: #1565c0; border-bottom-color: #1565c0; }
 17 |   .content { padding: 28px 32px; max-width: 1100px; margin: 0 auto; }
 18 |   .section { display: none; }
 19 |   .section.active { display: block; }
 20 |   .card { background: #fff; border-radius: 10px; box-shadow: 0 2px 10px rgba(21,101,192,.07); padding: 24px; margin-bottom: 22px; }
 21 |   .card h2 { font-size: 1.1rem; color: #1565c0; margin-bottom: 16px; border-bottom: 1px solid #e3eaf5; padding-bottom: 10px; }
 22 |   table { width: 100%; border-collapse: collapse; font-size: .93rem; }
 23 |   th { background: #e8f0fe; color: #1565c0; text-align: left; padding: 10px 12px; font-weight: 600; }
 24 |   td { padding: 9px 12px; border-bottom: 1px solid #f0f4f8; }
 25 |   tr:last-child td { border-bottom: none; }
 26 |   tr:hover td { background: #f5f9ff; }
 27 |   .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; }
 28 |   label { display: block; font-size: .85rem; font-weight: 600; color: #546e8a; margin-bottom: 5px; }
 29 |   input, select, textarea { width: 100%; padding: 9px 12px; border: 1.5px solid #ccd9ea; border-radius: 6px; font-size: .93rem; transition: border .2s; outline: none; }
 30 |   input:focus, select:focus, textarea:focus { border-color: #1565c0; }
 31 |   textarea { resize: vertical; min-height: 70px; }
 32 |   .btn { background: #1565c0; color: #fff; border: none; padding: 10px 22px; border-radius: 6px; cursor: pointer; font-size: .93rem; font-weight: 600; transition: background .2s; }
 33 |   .btn:hover { background: #0d47a1; }
 34 |   .btn-sm { padding: 6px 14px; font-size: .85rem; }
 35 |   .btn-group { margin-top: 16px; }
 36 |   .msg { padding: 10px 16px; border-radius: 6px; margin: 12px 0; font-size: .9rem; font-weight: 500; }
 37 |   .msg.success { background: #e8f5e9; color: #2e7d32; border-left: 4px solid #43a047; }
 38 |   .msg.error { background: #fdecea; color: #c62828; border-left: 4px solid #e53935; }
 39 |   .spinner { display: inline-block; width: 22px; height: 22px; border: 3px solid #e3eaf5; border-top-color: #1565c0; border-radius: 50%; animation: spin .7s linear infinite; margin: 20px auto; }
 40 |   @keyframes spin { to { transform: rotate(360deg); } }
 41 |   .loader { text-align: center; padding: 20px; }
 42 |   .balance-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 14px; margin-bottom: 18px; }
 43 |   .balance-card { background: linear-gradient(135deg, #1565c0, #1e88e5); color: #fff; border-radius: 10px; padding: 16px; text-align: center; }
 44 |   .balance-card .val { font-size: 2rem; font-weight: 700; }
 45 |   .balance-card .lbl { font-size: .8rem; opacity: .85; margin-top: 4px; text-transform: uppercase; letter-spacing: .5px; }
 46 |   .badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: .78rem; font-weight: 600; }
 47 |   .badge.pending { background: #fff8e1; color: #f57f17; }
 48 |   .badge.approved { background: #e8f5e9; color: #2e7d32; }
 49 |   .badge.rejected { background: #fdecea; color: #c62828; }
 50 |   .badge.Excellent { background: #e8f5e9; color: #2e7d32; }
 51 |   .badge.Good { background: #e3f2fd; color: #1565c0; }
 52 |   .badge.Average { background: #fff8e1; color: #f57f17; }
 53 |   .badge.needs-improvement { background: #fdecea; color: #c62828; }
 54 |   .stars { display: inline-flex; gap: 3px; font-size: 1.2rem; }
 55 |   .star { color: #ddd; }
 56 |   .star.filled { color: #ffc107; }
 57 |   .payroll-row { display: flex; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid #f0f4f8; font-size: .95rem; }
 58 |   .payroll-row:last-child { border-bottom: none; font-weight: 700; color: #1565c0; }
 59 |   .emp-id-input { display: flex; gap: 10px; align-items: flex-end; margin-bottom: 16px; }
 60 |   .emp-id-input > div { flex: 1; }
 61 | </style>
 62 | </head>
 63 | <body>
 64 | 
 65 | <header>
 66 |   <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="16" fill="#1e88e5"/><path d="M10 22c0-3.314 2.686-6 6-6s6 2.686 6 6" stroke="#fff" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="12" r="3.5" stroke="#fff" stroke-width="2"/></svg>
 67 |   <div><h1>HR Employee Management</h1><span>Internal HR Portal</span></div>
 68 | </header>
 69 | 
 70 | <div class="tabs">
 71 |   <div class="tab active" onclick="switchTab('employees')">Employees</div>
 72 |   <div class="tab" onclick="switchTab('leave')">Leave</div>
 73 |   <div class="tab" onclick="switchTab('payroll')">Payroll</div>
 74 |   <div class="tab" onclick="switchTab('performance')">Performance Review</div>
 75 | </div>
 76 | 
 77 | <div class="content">
 78 | 
 79 |   <!-- EMPLOYEES -->
 80 |   <div id="tab-employees" class="section active">
 81 |     <div class="card">
 82 |       <h2>Employee List</h2>
 83 |       <div id="emp-loader" class="loader"><div class="spinner"></div></div>
 84 |       <div id="emp-msg"></div>
 85 |       <div id="emp-table-wrap" style="overflow-x:auto;"></div>
 86 |     </div>
 87 |     <div class="card">
 88 |       <h2>Add New Employee</h2>
 89 |       <div id="add-emp-msg"></div>
 90 |       <div class="form-grid">
 91 |         <div><label>Full Name</label><input id="new-name" placeholder="e.g. Kavya Nair"></div>
 92 |         <div><label>Department</label>
 93 |           <select id="new-dept">
 94 |             <option value="Engineering">Engineering</option>
 95 |             <option value="HR">HR</option>
 96 |             <option value="Finance">Finance</option>
 97 |             <option value="Operations">Operations</option>
 98 |             <option value="Marketing">Marketing</option>
 99 |           </select>
100 |         </div>
101 |         <div><label>Annual Salary (₹)</label><input id="new-salary" type="number" placeholder="e.g. 70000"></div>
102 |         <div><label>Manager ID (optional)</label><input id="new-manager" type="number" placeholder="e.g. 1"></div>
103 |       </div>
104 |       <div class="btn-group"><button class="btn" onclick="addEmployee()">Add Employee</button></div>
105 |     </div>
106 |   </div>
107 | 
108 |   <!-- LEAVE -->
109 |   <div id="tab-leave" class="section">
110 |     <div class="card">
111 |       <h2>Leave Balance</h2>
112 |       <div class="emp-id-input">
113 |         <div><label>Employee ID</label><input id="leave-emp-id" type="number" placeholder="Enter employee ID" value="1"></div>
114 |         <button class="btn" onclick="loadLeave()">Load</button>
115 |       </div>
116 |       <div id="leave-loader" class="loader" style="display:none"><div class="spinner"></div></div>
117 |       <div id="leave-msg"></div>
118 |       <div id="leave-balance-cards" class="balance-grid"></div>
119 |       <div id="leave-history-wrap" style="overflow-x:auto;"></div>
120 |     </div>
121 |     <div class="card">
122 |       <h2>Apply for Leave</h2>
123 |       <div id="apply-leave-msg"></div>
124 |       <div class="form-grid">
125 |         <div><label>Employee ID</label><input id="al-emp-id" type="number" placeholder="Employee ID" value="1"></div>
126 |         <div><label>Leave Type</label>
127 |           <select id="al-type">
128 |             <option value="annual">Annual (18 days)</option>
129 |             <option value="sick">Sick (10 days)</option>
130 |             <option value="maternity">Maternity (182 days)</option>
131 |             <option value="paternity">Paternity (5 days)</option>
132 |           </select>
133 |         </div>
134 |         <div><label>Number of Days</label><input id="al-days" type="number" placeholder="e.g. 2" min="1"></div>
135 |         <div><label>Reason</label><textarea id="al-reason" placeholder="Reason for leave..."></textarea></div>
136 |       </div>
137 |       <div class="btn-group"><button class="btn" onclick="applyLeave()">Apply Leave</button></div>
138 |     </div>
139 |     <div class="card">
140 |       <h2>Approve Leave</h2>
141 |       <div id="approve-leave-msg"></div>
142 |       <div class="form-grid">
143 |         <div><label>Leave ID</label><input id="apr-leave-id" type="number" placeholder="Leave ID"></div>
144 |         <div><label>Approved By (Employee ID)</label><input id="apr-by" type="number" placeholder="Manager ID"></div>
145 |       </div>
146 |       <div class="btn-group"><button class="btn" onclick="approveLeave()">Approve Leave</button></div>
147 |     </div>
148 |   </div>
149 | 
150 |   <!-- PAYROLL -->
151 |   <div id="tab-payroll" class="section">
152 |     <div class="card">
153 |       <h2>Salary Details</h2>
154 |       <div class="emp-id-input">
155 |         <div><label>Employee ID</label><input id="pay-emp-id" type="number" placeholder="Enter employee ID" value="1"></div>
156 |         <button class="btn" onclick="loadPayroll()">Load</button>
157 |       </div>
158 |       <div id="payroll-loader" class="loader" style="display:none"><div class="spinner"></div></div>
159 |       <div id="payroll-msg"></div>
160 |       <div id="payroll-detail"></div>
161 |     </div>
162 |     <div class="card">
163 |       <h2>Generate Payslip</h2>
164 |       <div class="form-grid">
165 |         <div><label>Employee ID</label><input id="ps-emp-id" type="number" placeholder="Employee ID" value="1"></div>
166 |         <div><label>Month</label>
167 |           <select id="ps-month">
168 |             <option value="1">January</option><option value="2">February</option>
169 |             <option value="3">March</option><option value="4">April</option>
170 |             <option value="5">May</option><option value="6">June</option>
171 |             <option value="7">July</option><option value="8">August</option>
172 |             <option value="9">September</option><option value="10">October</option>
173 |             <option value="11">November</option><option value="12">December</option>
174 | 
175 |   <!-- PERFORMANCE REVIEW -->
176 |   <div id="tab-performance" class="section">
177 |     <div class="card">
178 |       <h2>Performance Review</h2>
179 |       <div class="emp-id-input">
180 |         <div><label>Employee ID</label><input id="perf-emp-id" type="number" placeholder="Enter employee ID" value="1"></div>
181 |         <button class="btn" onclick="loadPerformance()">Load</button>
182 |       </div>
183 |       <div id="perf-loader" class="loader" style="display:none"><div class="spinner"></div></div>
184 |       <div id="perf-msg"></div>
185 |       <div id="perf-detail"></div>
186 |     </div>
187 |     <div class="card">
188 |       <h2>Add Performance Review</h2>
189 |       <div id="add-review-msg"></div>
190 |       <div class="form-grid">
191 |         <div><label>Employee ID</label><input id="rev-emp-id" type="number" placeholder="Employee ID" value="1"></div>
192 |         <div><label>Rating (1-5)</label>
193 |           <select id="rev-rating">
194 |             <option value="5">5 - Excellent</option>
195 |             <option value="4">4 - Good</option>
196 |             <option value="3">3 - Average</option>
197 |             <option value="2">2 - Needs Improvement</option>
198 |             <option value="1">1 - Poor</option>
199 |           </select>
200 |         </div>
201 |         <div><label>Reviewer ID</label><input id="rev-reviewer" type="number" placeholder="Reviewer ID" value="1"></div>
202 |         <div><label>Comments</label><textarea id="rev-comments" placeholder="Performance review comments..."></textarea></div>
203 |       </div>
204 |       <div class="btn-group"><button class="btn" onclick="addReview()">Submit Review</button></div>
205 |     </div>
206 |   </div>
207 | 
208 |           </select>
209 |         </div>
210 |         <div><label>Year</label><input id="ps-year" type="number" placeholder="e.g. 2026" value="2026"></div>
211 |       </div>
212 |       <div class="btn-group"><button class="btn" onclick="generatePayslip()">Generate Payslip</button></div>
213 |       <div id="payslip-msg"></div>
214 |       <div id="payslip-detail"></div>
215 |     </div>
216 |   </div>
217 | 
218 | </div>
219 | 
220 | <script>
221 | const API = '';
222 | 
223 | function switchTab(tab) {
224 |   document.querySelectorAll('.tab').forEach((t, i) => {
225 |     const names = ['employees','leave','payroll','performance'];
226 |     t.classList.toggle('active', names[i] === tab);
227 |   });
228 |   document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
229 |   document.getElementById('tab-' + tab).classList.add('active');
230 |   if (tab === 'employees') loadEmployees();
231 | }
232 | 
233 | function showMsg(id, text, type) {
234 |   const el = document.getElementById(id);
235 |   el.innerHTML = `<div class="msg ${type}">${text}</div>`;
236 |   setTimeout(() => { el.innerHTML = ''; }, 4000);
237 | }
238 | 
239 | function fmt(n) { return '₹' + Number(n).toLocaleString('en-IN', {maximumFractionDigits: 2}); }
240 | 
241 | async function loadEmployees() {
242 |   document.getElementById('emp-loader').style.display = 'block';
243 |   document.getElementById('emp-table-wrap').innerHTML = '';
244 |   try {
245 |     const res = await fetch(API + '/employees');
246 |     const data = await res.json();
247 |     document.getElementById('emp-loader').style.display = 'none';
248 |     if (!data.length) { document.getElementById('emp-table-wrap').innerHTML = '<p style="color:#546e8a">No employees found.</p>'; return; }
249 |     let html = '<table><thead><tr><th>ID</th><th>Name</th><th>Department</th><th>Join Date</th><th>Annual Salary</th><th>Manager ID</th></tr></thead><tbody>';
250 |     data.forEach(e => {
251 |       html += `<tr><td>${e.id}</td><td>${e.name}</td><td>${e.department}</td><td>${e.join_date}</td><td>${fmt(e.salary)}</td><td>${e.manager ?? '—'}</td></tr>`;
252 |     });
253 |     html += '</tbody></table>';
254 |     document.getElementById('emp-table-wrap').innerHTML = html;
255 |   } catch(err) {
256 |     document.getElementById('emp-loader').style.display = 'none';
257 |     showMsg('emp-msg', 'Failed to load employees.', 'error');
258 |   }
259 | }
260 | 
261 | async function addEmployee() {
262 |   const name = document.getElementById('new-name').value.trim();
263 |   const dept = document.getElementById('new-dept').value;
264 |   const salary = parseFloat(document.getElementById('new-salary').value);
265 |   const mgr = document.getElementById('new-manager').value;
266 |   if (!name || !salary) { showMsg('add-emp-msg', 'Name and salary are required.', 'error'); return; }
267 |   try {
268 |     const res = await fetch(API + '/employees', {
269 |       method: 'POST', headers: {'Content-Type': 'application/json'},
270 |       body: JSON.stringify({ name, department: dept, salary, manager: mgr ? parseInt(mgr) : null })
271 |     });
272 |     const data = await res.json();
273 |     if (!res.ok) { showMsg('add-emp-msg', data.detail || 'Error adding employee.', 'error'); return; }
274 |     showMsg('add-emp-msg', `Employee "${data.name}" added with ID ${data.id}.`, 'success');
275 |     document.getElementById('new-name').value = '';
276 |     document.getElementById('new-salary').value = '';
277 |     document.getElementById('new-manager').value = '';
278 |     loadEmployees();
279 |   } catch(e) { showMsg('add-emp-msg', 'Network error.', 'error'); }
280 | }
281 | 
282 | async function loadLeave() {
283 |   const empId = document.getElementById('leave-emp-id').value;
284 |   if (!empId) { showMsg('leave-msg', 'Enter an employee ID.', 'error'); return; }
285 |   document.getElementById('leave-loader').style.display = 'block';
286 |   document.getElementById('leave-balance-cards').innerHTML = '';
287 |   document.getElementById('leave-history-wrap').innerHTML = '';
288 |   try {
289 |     const res = await fetch(API + '/leave/' + empId);
290 |     const data = await res.json();
291 |     document.getElementById('leave-loader').style.display = 'none';
292 |     if (!res.ok) { showMsg('leave-msg', data.detail || 'Employee not found.', 'error'); return; }
293 |     const labels = { annual: 'Annual', sick: 'Sick', maternity: 'Maternity', paternity: 'Paternity' };
294 |     let cards = '';
295 |     for (const [k, v] of Object.entries(data.balances)) {
296 |       cards += `<div class="balance-card"><div class="val">${v}</div><div class="lbl">${labels[k] || k} Days</div></div>`;
297 |     }
298 |     document.getElementById('leave-balance-cards').innerHTML = cards;
299 | 
300 |     if (data.history && data.history.length) {
301 |       let h = '<h3 style="margin:16px 0 10px;font-size:.97rem;color:#1565c0">Leave History</h3><table><thead><tr><th>ID</th><th>Type</th><th>Days</th><th>Reason</th><th>Status</th><th>Applied On</th></tr></thead><tbody>';
302 |       data.history.forEach(r => {
303 |         h += `<tr><td>${r.leave_id}</td><td>${r.leave_type}</td><td>${r.days}</td><td>${r.reason}</td><td><span class="badge ${r.status}">${r.status}</span></td><td>${r.applied_on}</td></tr>`;
304 |       });
305 |       h += '</tbody></table>';
306 |       document.getElementById('leave-history-wrap').innerHTML = h;
307 |     }
308 |   } catch(e) {
309 |     document.getElementById('leave-loader').style.display = 'none';
310 |     showMsg('leave-msg', 'Network error.', 'error');
311 |   }
312 | }
313 | 
314 | async function applyLeave() {
315 |   const emp_id = parseInt(document.getElementById('al-emp-id').value);
316 |   const leave_type = document.getElementById('al-type').value;
317 |   const days = parseInt(document.getElementById('al-days').value);
318 |   const reason = document.getElementById('al-reason').value.trim();
319 |   if (!emp_id || !days || !reason) { showMsg('apply-leave-msg', 'All fields are required.', 'error'); return; }
320 |   try {
321 |     const res = await fetch(API + '/leave/apply', {
322 |       method: 'POST', headers: {'Content-Type': 'application/json'},
323 |       body: JSON.stringify({ emp_id, leave_type, days, reason })
324 |     });
325 |     const data = await res.json();
326 |     if (!res.ok) { showMsg('apply-leave-msg', data.detail || 'Error applying leave.', 'error'); return; }
327 |     showMsg('apply-leave-msg', `Leave applied. Leave ID: ${data.leave_id}`, 'success');
328 |     document.getElementById('al-days').value = '';
329 |     document.getElementById('al-reason').value = '';
330 |   } catch(e) { showMsg('apply-leave-msg', 'Network error.', 'error'); }
331 | }
332 | 
333 | async function approveLeave() {
334 |   const leave_id = parseInt(document.getElementById('apr-leave-id').value);
335 |   const approved_by = parseInt(document.getElementById('apr-by').value);
336 |   if (!leave_id || !approved_by) { showMsg('approve-leave-msg', 'Leave ID and approver ID are required.', 'error'); return; }
337 |   try {
338 |     const res = await fetch(API + '/leave/approve', {
339 |       method: 'POST', headers: {'Content-Type': 'application/json'},
340 |       body: JSON.stringify({ leave_id, approved_by })
341 |     });
342 |     const data = await res.json();
343 |     if (!res.ok) { showMsg('approve-leave-msg', data.detail || 'Error approving leave.', 'error'); return; }
344 |     showMsg('approve-leave-msg', `Leave ${leave_id} approved successfully.`, 'success');
345 |   } catch(e) { showMsg('approve-leave-msg', 'Network error.', 'error'); }
346 | }
347 | 
348 | async function loadPayroll() {
349 |   const empId = document.getElementById('pay-emp-id').value;
350 |   if (!empId) { showMsg('payroll-msg', 'Enter an employee ID.', 'error'); return; }
351 |   document.getElementById('payroll-loader').style.display = 'block';
352 |   document.getElementById('payroll-detail').innerHTML = '';
353 |   try {
354 |     const res = await fetch(API + '/payroll/' + empId);
355 |     const d = await res.json();
356 |     document.getElementById('payroll-loader').style.display = 'none';
357 |     if (!res.ok) { showMsg('payroll-msg', d.detail || 'Employee not found.', 'error'); return; }
358 |     document.getElementById('payroll-detail').innerHTML = `
359 |       <div style="margin-bottom:8px;font-weight:600;font-size:1.05rem">${d.name} — ${d.department}</div>
360 |       <div class="payroll-row"><span>Annual Salary</span><span>${fmt(d.annual_salary)}</span></div>
361 |       <div class="payroll-row"><span>Monthly Gross</span><span>${fmt(d.monthly_gross)}</span></div>
362 |       <div class="payroll-row"><span>Monthly Tax</span><span style="color:#c62828">- ${fmt(d.monthly_tax)}</span></div>
363 |       <div class="payroll-row"><span>PF Deduction (12%)</span><span style="color:#c62828">- ${fmt(d.monthly_pf)}</span></div>
364 |       <div class="payroll-row"><span>Net Monthly Pay</span><span>${fmt(d.monthly_net)}</span></div>
365 |       <div class="payroll-row" style="border-top:1.5px solid #e3eaf5;margin-top:6px;padding-top:12px"><span>Experience</span><span>${d.experience_years} year(s)</span></div>
366 |     `;
367 |   } catch(e) {
368 |     document.getElementById('payroll-loader').style.display = 'none';
369 |     showMsg('payroll-msg', 'Network error.', 'error');
370 |   }
371 | }
372 | 
373 | async function generatePayslip() {
374 |   const empId = document.getElementById('ps-emp-id').value;
375 |   const month = document.getElementById('ps-month').value;
376 |   const year = document.getElementById('ps-year').value;
377 |   if (!empId || !month || !year) { showMsg('payslip-msg', 'All fields are required.', 'error'); return; }
378 |   try {
379 |     const res = await fetch(`${API}/payroll/${empId}/payslip?month=${month}&year=${year}`);
380 |     const d = await res.json();
381 |     if (!res.ok) { showMsg('payslip-msg', d.detail || 'Error generating payslip.', 'error'); return; }
382 |     const months = ['','January','February','March','April','May','June','July','August','September','October','November','December'];
383 |     document.getElementById('payslip-detail').innerHTML = `
384 |       <div style="margin-top:18px;border:1.5px solid #e3eaf5;border-radius:8px;padding:18px;">
385 | 
386 | function renderStars(rating) {
387 |   let stars = '<div class="stars">';
388 |   for (let i = 1; i <= 5; i++) {
389 |     stars += `<span class="star ${i <= rating ? 'filled' : ''}">★</span>`;
390 |   }
391 |   stars += '</div>';
392 |   return stars;
393 | }
394 | 
395 | function getBadgeClass(badge) {
396 |   if (badge === 'Needs Improvement') return 'needs-improvement';
397 |   return badge;
398 | }
399 | 
400 | async function loadPerformance() {
401 |   const empId = document.getElementById('perf-emp-id').value;
402 |   if (!empId) { showMsg('perf-msg', 'Enter an employee ID.', 'error'); return; }
403 |   document.getElementById('perf-loader').style.display = 'block';
404 |   document.getElementById('perf-detail').innerHTML = '';
405 |   try {
406 |     const res = await fetch(API + '/performance/' + empId);
407 |     const d = await res.json();
408 |     document.getElementById('perf-loader').style.display = 'none';
409 |     if (!res.ok) { showMsg('perf-msg', d.detail || 'Employee not found.', 'error'); return; }
410 |     
411 |     // Get employee info
412 |     const empRes = await fetch(API + '/employees/' + empId);
413 |     const emp = await empRes.json();
414 |     
415 |     let html = `<div style="margin-bottom:16px;font-weight:600;font-size:1.05rem">${emp.name} — ${emp.department}</div>`;
416 |     
417 |     // Performance badge and rating
418 |     if (d.latest_review && d.latest_review.rating) {
419 |       html += `<div style="display:flex;gap:16px;align-items:center;margin-bottom:16px;">`;
420 |       html += `<div>${renderStars(d.latest_review.rating)}</div>`;
421 |       html += `<span class="badge ${getBadgeClass(d.badge)}">${d.badge}</span>`;
422 |       html += `</div>`;
423 |       
424 |       // Bonus information
425 |       html += `<div class="payroll-row"><span>Performance Bonus</span><span style="color:#2e7d32;font-weight:700">${d.bonus_percentage}%</span></div>`;
426 |       
427 |       const bonusRes = await fetch(API + '/performance/' + empId + '/bonus');
428 |       const bonusData = await bonusRes.json();
429 |       html += `<div class="payroll-row"><span>Bonus Amount</span><span style="color:#2e7d32;font-weight:700">${fmt(bonusData.bonus_amount)}</span></div>`;
430 |     } else {
431 |       html += `<p style="color:#546e8a;margin-bottom:16px">No performance reviews yet.</p>`;
432 |     }
433 |     
434 |     // Review history
435 |     if (d.reviews && d.reviews.length) {
436 |       html += '<h3 style="margin:20px 0 10px;font-size:.97rem;color:#1565c0">Review History</h3>';
437 |       html += '<table><thead><tr><th>Date</th><th>Rating</th><th>Comments</th><th>Reviewer ID</th></tr></thead><tbody>';
438 |       d.reviews.forEach(r => {
439 |         html += `<tr><td>${r.review_date}</td><td>${renderStars(r.rating)}</td><td>${r.comments}</td><td>${r.reviewer_id}</td></tr>`;
440 |       });
441 |       html += '</tbody></table>';
442 |     }
443 |     
444 |     document.getElementById('perf-detail').innerHTML = html;
445 |   } catch(e) {
446 |     document.getElementById('perf-loader').style.display = 'none';
447 |     showMsg('perf-msg', 'Network error.', 'error');
448 |   }
449 | }
450 | 
451 | async function addReview() {
452 |   const emp_id = parseInt(document.getElementById('rev-emp-id').value);
453 |   const rating = parseInt(document.getElementById('rev-rating').value);
454 |   const comments = document.getElementById('rev-comments').value.trim();
455 |   const reviewer_id = parseInt(document.getElementById('rev-reviewer').value);
456 |   
457 |   if (!emp_id || !rating || !comments || !reviewer_id) {
458 |     showMsg('add-review-msg', 'All fields are required.', 'error');
459 |     return;
460 |   }
461 |   
462 |   try {
463 |     const res = await fetch(API + '/performance/review', {
464 |       method: 'POST',
465 |       headers: {'Content-Type': 'application/json'},
466 |       body: JSON.stringify({ emp_id, rating, comments, reviewer_id })
467 |     });
468 |     const data = await res.json();
469 |     if (!res.ok) {
470 |       showMsg('add-review-msg', data.detail || 'Error adding review.', 'error');
471 |       return;
472 |     }
473 |     showMsg('add-review-msg', `Review added successfully. Review ID: ${data.review_id}`, 'success');
474 |     document.getElementById('rev-comments').value = '';
475 |     
476 |     // Reload performance if viewing the same employee
477 |     if (document.getElementById('perf-emp-id').value == emp_id) {
478 |       loadPerformance();
479 |     }
480 |   } catch(e) {
481 |     showMsg('add-review-msg', 'Network error.', 'error');
482 |   }
483 | }
484 | 
485 |         <div style="font-size:1.1rem;font-weight:700;color:#1565c0;margin-bottom:12px">Payslip — ${months[d.month]} ${d.year}</div>
486 |         <div style="margin-bottom:6px"><b>${d.name}</b> | ${d.department}</div>
487 |         <div class="payroll-row"><span>Gross Salary</span><span>${fmt(d.gross_salary)}</span></div>
488 |         <div class="payroll-row"><span>Tax</span><span style="color:#c62828">- ${fmt(d.deductions.tax)}</span></div>
489 |         <div class="payroll-row"><span>PF</span><span style="color:#c62828">- ${fmt(d.deductions.pf)}</span></div>
490 |         <div class="payroll-row"><span>Net Pay</span><span>${fmt(d.net_salary)}</span></div>
491 |       </div>
492 |     `;
493 |     showMsg('payslip-msg', 'Payslip generated successfully.', 'success');
494 |   } catch(e) { showMsg('payslip-msg', 'Network error.', 'error'); }
495 | }
496 | 
497 | // Set default month for payslip
498 | (function() {
499 |   document.getElementById('ps-month').value = new Date().getMonth() + 1;
500 |   loadEmployees();
501 | })();
502 | </script>
503 | </body>
504 | </html>
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
bob_sessions/task4_test_performance_fix.md

# VSCode Open Tabs
app/main.py,bob_sessions/task4_test_performance_fix.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-01T18:57:05.796Z
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

I can see the file has already been partially fixed - the `API` constant on line 221 is set to an empty string `''`, which means it's already using relative URLs. However, I need to check if there are any remaining absolute URLs with `http://localhost:8000` in the fetch calls.

Looking through the file, I can see that all fetch calls are using `API + '/endpoint'` pattern, which means they're already using relative URLs since `API = ''`. The file appears to already be correctly configured for relative URLs.

Let me verify there are no hardcoded `http://localhost:8000` URLs anywhere in the file by searching for them:

<search_files>
<path>static/index.html</path>
<regex>http://localhost:8000</regex>
</search_files>

---

**User:**

[search_files for 'http://localhost:8000'] Result:
Found 0 results.
<environment_details>
# VSCode Visible Files
bob_sessions/task4_test_performance_fix.md

# VSCode Open Tabs
app/main.py,bob_sessions/task4_test_performance_fix.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-01T18:57:13.511Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.04

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

Perfect! The search confirms that there are no occurrences of `http://localhost:8000` in the file. 

Looking at the code, I can see that:
1. Line 221 defines `const API = '';` (empty string for relative URLs)
2. All fetch calls use the pattern `API + '/endpoint'` which results in relative URLs like `/employees`, `/leave/1`, etc.

The file is already correctly configured to use relative URLs for all API calls. The task has already been completed - all API fetch URLs are using relative paths.

<attempt_completion>
<result>
The index.html file is already correctly configured with relative URLs for all API calls.

Current configuration:
- Line 221: `const API = '';` (empty string)
- All fetch calls use `API + '/endpoint'` pattern
- This results in relative URLs like `/employees`, `/leave/1`, `/payroll/1`, etc.

No changes were needed - the file contains zero occurrences of `http://localhost:8000` and all API calls are already using relative URLs as requested.
</result>
</attempt_completion>

