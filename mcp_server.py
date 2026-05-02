import sys
import json

def handle_request(request):
    method = request.get("method", "")
    req_id = request.get("id", 1)
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "hr-onboarding",
                    "version": "1.0.0"
                }
            }
        }
    
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "get_all_employees",
                        "description": "Get all HR employees",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "get_leave_balance",
                        "description": "Get leave balance for employee",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "emp_id": {
                                    "type": "number",
                                    "description": "Employee ID"
                                }
                            },
                            "required": ["emp_id"]
                        }
                    },
                    {
                        "name": "get_payroll",
                        "description": "Get payroll for employee",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "emp_id": {
                                    "type": "number",
                                    "description": "Employee ID"
                                }
                            },
                            "required": ["emp_id"]
                        }
                    },
                    {
                        "name": "get_performance",
                        "description": "Get performance review",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "emp_id": {
                                    "type": "number",
                                    "description": "Employee ID"
                                }
                            },
                            "required": ["emp_id"]
                        }
                    }
                ]
            }
        }
    
    elif method == "tools/call":
        from app import employee, leave, payroll, performance
        tool_name = request.get("params", {}).get("name", "")
        args = request.get("params", {}).get("arguments", {})
        
        try:
            if tool_name == "get_all_employees":
                result = employee.list_employees()
            elif tool_name == "get_leave_balance":
                result = leave.get_leave_balance(int(args["emp_id"]))
            elif tool_name == "get_payroll":
                result = payroll.calculate_monthly_salary(int(args["emp_id"]))
            elif tool_name == "get_performance":
                result = performance.get_latest_review(int(args["emp_id"]))
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result)
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }
    
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32601,
            "message": f"Method not found: {method}"
        }
    }

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response), flush=True)
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "error": {"code": -32700, "message": str(e)}
            }), flush=True)

# Made with Bob
