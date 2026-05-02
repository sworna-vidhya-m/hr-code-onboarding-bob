# Agent Guidelines

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