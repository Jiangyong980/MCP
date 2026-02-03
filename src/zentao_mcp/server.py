"""Zentao MCP Server

A Model Context Protocol server that provides access to Zentao PM system.
"""
import asyncio
import logging
import json
from typing import Sequence

from mcp.server import Server
from mcp.types import Tool, TextContent, Resource

from .client import ZentaoClient
from .config import ZentaoConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("zentao-mcp-server")

# Global client instance
_client: ZentaoClient = None


def get_client() -> ZentaoClient:
    """Get or create Zentao client"""
    global _client
    if _client is None:
        config = ZentaoConfig.from_env()
        if not config.is_valid():
            raise ValueError(
                "Zentao configuration is incomplete. "
                "Please set ZENTAO_BASE_URL, ZENTAO_USERNAME, and ZENTAO_PASSWORD environment variables."
            )
        _client = ZentaoClient(config)
    return _client


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        # ==================== Programs ====================
        Tool(
            name="list_programs",
            description="Get list of all programs (项目集)",
            inputSchema={
                "type": "object",
                "properties": {
                    "order": {
                        "type": "string",
                        "description": "Sort order, e.g., 'order_asc' or 'order_desc'"
                    }
                }
            }
        ),
        Tool(
            name="get_program",
            description="Get details of a specific program",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_id": {
                        "type": "integer",
                        "description": "Program ID"
                    }
                },
                "required": ["program_id"]
            }
        ),
        
        # ==================== Products ====================
        Tool(
            name="list_products",
            description="Get list of all products (产品)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_product",
            description="Get details of a specific product",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "Product ID"
                    }
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="create_product",
            description="Create a new product",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Product name"
                    },
                    "code": {
                        "type": "string",
                        "description": "Product code"
                    },
                    "program": {
                        "type": "integer",
                        "description": "Program ID"
                    },
                    "PO": {
                        "type": "string",
                        "description": "Product owner account"
                    },
                    "desc": {
                        "type": "string",
                        "description": "Product description"
                    }
                },
                "required": ["name", "code"]
            }
        ),
        
        # ==================== Projects ====================
        Tool(
            name="list_projects",
            description="Get list of all projects (项目)",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "Page number (default: 1)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Items per page (default: 20)"
                    }
                }
            }
        ),
        Tool(
            name="get_project",
            description="Get details of a specific project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="create_project",
            description="Create a new project",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Project name"
                    },
                    "code": {
                        "type": "string",
                        "description": "Project code"
                    },
                    "begin": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD)"
                    },
                    "end": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD)"
                    },
                    "products": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Associated product IDs"
                    }
                },
                "required": ["name", "code", "begin", "end", "products"]
            }
        ),
        Tool(
            name="get_project_executions",
            description="Get executions (sprints) for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        # ==================== Executions ====================
        Tool(
            name="list_executions",
            description="Get list of all executions (iterations/sprints)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_execution",
            description="Get details of a specific execution",
            inputSchema={
                "type": "object",
                "properties": {
                    "execution_id": {
                        "type": "integer",
                        "description": "Execution ID"
                    }
                },
                "required": ["execution_id"]
            }
        ),
        Tool(
            name="get_execution_tasks",
            description="Get tasks for an execution",
            inputSchema={
                "type": "object",
                "properties": {
                    "execution_id": {
                        "type": "integer",
                        "description": "Execution ID"
                    }
                },
                "required": ["execution_id"]
            }
        ),
        
        # ==================== Stories ====================
        Tool(
            name="get_story",
            description="Get details of a specific story (需求)",
            inputSchema={
                "type": "object",
                "properties": {
                    "story_id": {
                        "type": "integer",
                        "description": "Story ID"
                    }
                },
                "required": ["story_id"]
            }
        ),
        Tool(
            name="create_story",
            description="Create a new story",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Story title"
                    },
                    "product": {
                        "type": "integer",
                        "description": "Product ID"
                    },
                    "pri": {
                        "type": "integer",
                        "description": "Priority (1-4)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Category: feature, interface, performance, safe, experience, improve, other"
                    },
                    "spec": {
                        "type": "string",
                        "description": "Story specification/description"
                    },
                    "verify": {
                        "type": "string",
                        "description": "Acceptance criteria"
                    }
                },
                "required": ["title", "product", "pri", "category"]
            }
        ),
        
        # ==================== Tasks ====================
        Tool(
            name="get_task",
            description="Get details of a specific task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="create_task",
            description="Create a new task in an execution",
            inputSchema={
                "type": "object",
                "properties": {
                    "execution_id": {
                        "type": "integer",
                        "description": "Execution ID (sprint/iteration)"
                    },
                    "name": {
                        "type": "string",
                        "description": "Task name"
                    },
                    "type": {
                        "type": "string",
                        "description": "Task type: design, devel, request, test, study, discuss, ui, affair, misc"
                    },
                    "assignedTo": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Assigned user accounts"
                    },
                    "estStarted": {
                        "type": "string",
                        "description": "Estimated start date (YYYY-MM-DD)"
                    },
                    "deadline": {
                        "type": "string",
                        "description": "Deadline (YYYY-MM-DD)"
                    },
                    "pri": {
                        "type": "integer",
                        "description": "Priority (1-4)"
                    },
                    "estimate": {
                        "type": "number",
                        "description": "Estimated hours"
                    }
                },
                "required": ["execution_id", "name", "type", "assignedTo", "estStarted", "deadline"]
            }
        ),
        
        # ==================== Bugs ====================
        Tool(
            name="get_bug",
            description="Get details of a specific bug",
            inputSchema={
                "type": "object",
                "properties": {
                    "bug_id": {
                        "type": "integer",
                        "description": "Bug ID"
                    }
                },
                "required": ["bug_id"]
            }
        ),
        
        # ==================== Users ====================
        Tool(
            name="list_users",
            description="Get list of all users",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_my_info",
            description="Get current user information",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # ==================== Test Cases ====================
        Tool(
            name="get_product_testcases",
            description="Get test cases for a product (获取产品测试用例列表)",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "Product ID"
                    }
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="get_testcase",
            description="Get test case details (获取测试用例详情，包含步骤和预期结果)",
            inputSchema={
                "type": "object",
                "properties": {
                    "testcase_id": {
                        "type": "integer",
                        "description": "Test case ID"
                    }
                },
                "required": ["testcase_id"]
            }
        ),
        Tool(
            name="create_testcase",
            description="Create a new test case (创建测试用例)",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "Product ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "Test case title"
                    },
                    "type": {
                        "type": "string",
                        "description": "Test case type: feature, performance, config, install, security, interface, unit, other"
                    },
                    "pri": {
                        "type": "integer",
                        "description": "Priority (1-4)"
                    },
                    "precondition": {
                        "type": "string",
                        "description": "Precondition for the test"
                    },
                    "steps": {
                        "type": "array",
                        "description": "Test steps",
                        "items": {
                            "type": "object",
                            "properties": {
                                "desc": {"type": "string", "description": "Step description"},
                                "expect": {"type": "string", "description": "Expected result"}
                            }
                        }
                    },
                    "keywords": {
                        "type": "string",
                        "description": "Keywords"
                    }
                },
                "required": ["product_id", "title", "type"]
            }
        ),
        
        # ==================== Test Tasks ====================
        Tool(
            name="list_testtasks",
            description="Get list of test tasks (获取测试单列表)",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "Page number (default: 1)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Items per page (default: 20)"
                    }
                }
            }
        ),
        Tool(
            name="get_testtask",
            description="Get test task details (获取测试单详情)",
            inputSchema={
                "type": "object",
                "properties": {
                    "testtask_id": {
                        "type": "integer",
                        "description": "Test task ID"
                    }
                },
                "required": ["testtask_id"]
            }
        ),
        Tool(
            name="get_project_testtasks",
            description="Get test tasks for a project (获取项目的测试单列表)",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        # ==================== Product Plans ====================
        Tool(
            name="get_product_plans",
            description="Get plans for a product (获取产品计划列表)",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "Product ID"
                    }
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="get_plan",
            description="Get plan details (获取计划详情，包含关联的需求和Bug)",
            inputSchema={
                "type": "object",
                "properties": {
                    "plan_id": {
                        "type": "integer",
                        "description": "Plan ID"
                    }
                },
                "required": ["plan_id"]
            }
        ),
        
        # ==================== Builds ====================
        Tool(
            name="get_project_builds",
            description="Get builds for a project (获取项目版本列表)",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="get_execution_builds",
            description="Get builds for an execution (获取迭代版本列表)",
            inputSchema={
                "type": "object",
                "properties": {
                    "execution_id": {
                        "type": "integer",
                        "description": "Execution ID"
                    }
                },
                "required": ["execution_id"]
            }
        ),
        Tool(
            name="get_build",
            description="Get build details (获取版本详情)",
            inputSchema={
                "type": "object",
                "properties": {
                    "build_id": {
                        "type": "integer",
                        "description": "Build ID"
                    }
                },
                "required": ["build_id"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    """Handle tool calls"""
    client = get_client()
    
    try:
        # ==================== Programs ====================
        if name == "list_programs":
            result = client.list_programs(order=arguments.get("order"))
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_program":
            result = client.get_program(arguments["program_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Products ====================
        elif name == "list_products":
            result = client.list_products()
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_product":
            result = client.get_product(arguments["product_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "create_product":
            data = {
                "name": arguments["name"],
                "code": arguments["code"],
            }
            if "program" in arguments:
                data["program"] = arguments["program"]
            if "PO" in arguments:
                data["PO"] = arguments["PO"]
            if "desc" in arguments:
                data["desc"] = arguments["desc"]
            result = client.create_product(data)
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Projects ====================
        elif name == "list_projects":
            result = client.list_projects(
                page=arguments.get("page", 1),
                limit=arguments.get("limit", 20)
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_project":
            result = client.get_project(arguments["project_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "create_project":
            data = {
                "name": arguments["name"],
                "code": arguments["code"],
                "begin": arguments["begin"],
                "end": arguments["end"],
                "products": arguments["products"],
            }
            result = client.create_project(data)
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_project_executions":
            result = client.get_project_executions(arguments["project_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Executions ====================
        elif name == "list_executions":
            result = client.list_executions()
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_execution":
            result = client.get_execution(arguments["execution_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_execution_tasks":
            result = client.get_execution_tasks(arguments["execution_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Stories ====================
        elif name == "get_story":
            result = client.get_story(arguments["story_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "create_story":
            data = {
                "title": arguments["title"],
                "product": arguments["product"],
                "pri": arguments["pri"],
                "category": arguments["category"],
            }
            if "spec" in arguments:
                data["spec"] = arguments["spec"]
            if "verify" in arguments:
                data["verify"] = arguments["verify"]
            result = client.create_story(data)
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Tasks ====================
        elif name == "get_task":
            result = client.get_task(arguments["task_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "create_task":
            data = {
                "name": arguments["name"],
                "type": arguments["type"],
                "assignedTo": arguments["assignedTo"],
                "estStarted": arguments["estStarted"],
                "deadline": arguments["deadline"],
            }
            if "pri" in arguments:
                data["pri"] = arguments["pri"]
            if "estimate" in arguments:
                data["estimate"] = arguments["estimate"]
            result = client.create_task(arguments["execution_id"], data)
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Bugs ====================
        elif name == "get_bug":
            result = client.get_bug(arguments["bug_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Users ====================
        elif name == "list_users":
            result = client.list_users()
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_my_info":
            result = client.get_my_info()
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Test Cases ====================
        elif name == "get_product_testcases":
            result = client.get_product_testcases(arguments["product_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_testcase":
            result = client.get_testcase(arguments["testcase_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "create_testcase":
            data = {
                "title": arguments["title"],
                "type": arguments["type"],
            }
            if "pri" in arguments:
                data["pri"] = arguments["pri"]
            if "precondition" in arguments:
                data["precondition"] = arguments["precondition"]
            if "steps" in arguments:
                data["steps"] = arguments["steps"]
            if "keywords" in arguments:
                data["keywords"] = arguments["keywords"]
            result = client.create_testcase(arguments["product_id"], data)
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Test Tasks ====================
        elif name == "list_testtasks":
            result = client.list_testtasks(
                page=arguments.get("page", 1),
                limit=arguments.get("limit", 20)
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_testtask":
            result = client.get_testtask(arguments["testtask_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_project_testtasks":
            result = client.get_project_testtasks(arguments["project_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Product Plans ====================
        elif name == "get_product_plans":
            result = client.get_product_plans(arguments["product_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_plan":
            result = client.get_plan(arguments["plan_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        # ==================== Builds ====================
        elif name == "get_project_builds":
            result = client.get_project_builds(arguments["project_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_execution_builds":
            result = client.get_execution_builds(arguments["execution_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_build":
            result = client.get_build(arguments["build_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="zentao://products",
            name="Products",
            description="List of all products in Zentao",
            mimeType="application/json"
        ),
        Resource(
            uri="zentao://projects",
            name="Projects",
            description="List of all projects in Zentao",
            mimeType="application/json"
        ),
        Resource(
            uri="zentao://users",
            name="Users",
            description="List of all users in Zentao",
            mimeType="application/json"
        ),
    ]


async def main():
    """Run the server"""
    # Import required for stdio server
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
